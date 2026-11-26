import csv
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai


# ============================================================
# 1. PROJECT SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "registrations.csv"
PROMPT_PATH = BASE_DIR / "src" / "system_prompt.txt"
REPORTS_DIR = BASE_DIR / "reports"

load_dotenv(BASE_DIR / ".env")

MODEL = "gemini-3.5-flash-lite"
MAX_API_ATTEMPTS = 3
API_CALL_INTERVAL_SECONDS = 5.2  # 12 requests/minute, below a 15 RPM limit

_client = None
_system_prompt = None
_last_api_call_time = 0.0


# ============================================================
# 2. LOAD API CLIENT AND SYSTEM PROMPT
# ============================================================

def get_client():
    """Create the Gemini client only when an API call is needed."""
    global _client

    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "Gemini API key not found. Add GEMINI_API_KEY=your_key "
                "to the .env file in the main ScoobyDo_AI folder."
            )
        _client = genai.Client(api_key=api_key)

    return _client


def load_system_prompt():
    """Read the system prompt once and cache it."""
    global _system_prompt

    if _system_prompt is None:
        if not PROMPT_PATH.exists():
            raise FileNotFoundError(f"System prompt not found: {PROMPT_PATH}")
        _system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    return _system_prompt


# ============================================================
# 3. READ REGISTRATION CSV
# ============================================================

def read_entry():
    """Read registrations.csv and return its rows as dictionaries."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Input CSV not found: {DATA_PATH}")

    registrations = []
    with open(DATA_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not {"id", "entry"}.issubset(reader.fieldnames):
            raise ValueError("registrations.csv must contain 'id' and 'entry' columns.")

        for row in reader:
            registrations.append({
                "id": (row.get("id") or "").strip(),
                "entry": (row.get("entry") or "").strip(),
            })

    return registrations


# ============================================================
# 4. GEMINI EXTRACTION WITH THROTTLING AND RETRIES
# ============================================================

def wait_for_api_slot():
    """Keep requests at least 5.2 seconds apart."""
    global _last_api_call_time

    elapsed = time.monotonic() - _last_api_call_time
    remaining = API_CALL_INTERVAL_SECONDS - elapsed

    if remaining > 0:
        time.sleep(remaining)

    _last_api_call_time = time.monotonic()


def get_retry_delay(error, attempt):
    """Use Gemini's suggested retry time when present; otherwise back off."""
    message = str(error)
    match = re.search(r"retry in\s+([0-9]+(?:\.[0-9]+)?)\s*s", message, re.IGNORECASE)

    if match:
        # Add a small buffer so we do not retry before the suggested time.
        return max(5.0, float(match.group(1)) + 2.0)

    # Exponential backoff for temporary server/rate-limit errors.
    return min(10.0 * (2 ** attempt), 40.0)


def is_retryable_error(error):
    message = str(error).lower()
    retryable_markers = (
        "429", "503", "500", "502", "504",
        "resource_exhausted", "unavailable", "deadline exceeded",
        "temporarily", "timeout", "timed out",
    )
    return any(marker in message for marker in retryable_markers)


def extract_details(entry):
    """Ask Gemini to copy the registration fields into the required JSON."""
    prompt = load_system_prompt()
    client = get_client()
    required_keys = {"name", "phone", "email", "year", "branch"}

    last_error = None

    for attempt in range(MAX_API_ATTEMPTS):
        try:
            wait_for_api_slot()
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt + "\n\nRegistration entry:\n" + entry,
            )

            response_text = (response.text or "").strip()
            # Tolerate a model response wrapped in Markdown code fences.
            response_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", response_text,
                                   flags=re.IGNORECASE).strip()
            result = json.loads(response_text)

            if not isinstance(result, dict) or set(result.keys()) != required_keys:
                raise ValueError("Gemini returned an invalid JSON structure.")

            return result

        except Exception as error:
            last_error = error

            if not is_retryable_error(error) or attempt == MAX_API_ATTEMPTS - 1:
                raise

            delay = get_retry_delay(error, attempt)
            print(
                f"Temporary Gemini error on attempt {attempt + 1}/"
                f"{MAX_API_ATTEMPTS}: {error}"
            )
            print(f"Waiting {delay:.1f} seconds before retrying...")
            time.sleep(delay)

    raise last_error


# ============================================================
# 5. FACT CHECKING
# ============================================================

def check_facts(result, entry):
    """Reject phone/email values that are not present in the original entry."""
    checked = dict(result)

    phone = checked.get("phone")
    if phone is not None:
        if not isinstance(phone, str) or not phone.isdigit():
            checked["phone"] = None
        else:
            original_digits = "".join(ch for ch in entry if ch.isdigit())
            if phone not in original_digits:
                checked["phone"] = None

    email = checked.get("email")
    if email is not None:
        if not isinstance(email, str):
            checked["email"] = None
        elif re.search(r"\bat\b|\bdot\b", email, re.IGNORECASE):
            checked["email"] = None
        elif email.lower() not in entry.lower():
            checked["email"] = None

    return checked


# ============================================================
# 6. CLEAN PHONE NUMBER
# ============================================================

def clean_phone(phone):
    if phone is None or not isinstance(phone, str):
        return None

    # Remove only formatting characters; do not invent or change digits.
    phone = re.sub(r"[\s+\-]", "", phone)

    # Remove a leading country code 91 only when there are 12 digits.
    if len(phone) == 12 and phone.startswith("91"):
        phone = phone[2:]
    # Remove a leading 0 only when there are 11 digits.
    elif len(phone) == 11 and phone.startswith("0"):
        phone = phone[1:]

    if len(phone) != 10 or not phone.isdigit():
        return None

    if phone[0] not in "6789":
        return None

    return phone


# ============================================================
# 7. CLEAN EMAIL
# ============================================================

def clean_email(email):
    if email is None or not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not email or " " in email:
        return None
    if email.count("@") != 1:
        return None
    if "." not in email.split("@", 1)[1]:
        return None

    return email


# ============================================================
# 8. CLEAN ALL FIELDS
# ============================================================

def clean(result):
    cleaned = {}

    name = result.get("name")
    cleaned["name"] = " ".join(name.split()).title() if isinstance(name, str) and name.strip() else None

    cleaned["phone"] = clean_phone(result.get("phone"))
    cleaned["email"] = clean_email(result.get("email"))

    year = result.get("year")
    if isinstance(year, int) and not isinstance(year, bool):
        cleaned["year"] = year
    else:
        cleaned["year"] = None

    allowed_branches = {"CSE", "IT", "AIDS", "ECE", "EEE", "MECH", "CIVIL"}
    branch = result.get("branch")

    if isinstance(branch, str):
        branch = branch.strip().upper()
        if branch in allowed_branches:
            cleaned["branch"] = branch
        elif branch.lower() == "other":
            cleaned["branch"] = "other"
        else:
            cleaned["branch"] = "other"
    else:
        cleaned["branch"] = None

    return cleaned


# ============================================================
# 9. VALIDATE REGISTRATION
# ============================================================

def is_valid(result):
    problems = []

    if not result.get("name"):
        problems.append("Missing name")
    if not result.get("phone"):
        problems.append("Missing or invalid phone")
    if not result.get("email"):
        problems.append("Missing or invalid email")
    if result.get("year") not in (1, 2, 3, 4):
        problems.append("Missing or invalid year")
    if result.get("branch") in (None, "other"):
        problems.append("Missing or invalid branch")

    return problems


# ============================================================
# 10. PROCESS REGISTRATIONS AND FIND DUPLICATES
# ============================================================

def process():
    registrations = read_entry()

    seen_phones = {}
    seen_emails = {}
    seen_original_entries = {}

    valid_entries = []
    problem_entries = []

    print(f"Loaded {len(registrations)} registrations.")

    for registration in registrations:
        reg_id = registration["id"]
        original_entry = registration["entry"]
        print(f"\nProcessing: {reg_id}")

        # Exact/near-exact duplicate check works even if Gemini is unavailable.
        normalized_entry = " ".join(original_entry.casefold().split())
        if normalized_entry and normalized_entry in seen_original_entries:
            first_id = seen_original_entries[normalized_entry]
            problem_entries.append({
                "id": reg_id,
                "original_entry": original_entry,
                "name": "",
                "phone": "",
                "email": "",
                "year": "",
                "branch": "",
                "status": "duplicate",
                "reasons": f"Duplicate of {first_id} (identical original entry)",
            })
            print(f"Status: duplicate of {first_id} (identical original entry)")
            continue

        if normalized_entry:
            seen_original_entries[normalized_entry] = reg_id

        try:
            extracted = extract_details(original_entry)
            extracted = check_facts(extracted, original_entry)
            cleaned = clean(extracted)
            reasons = is_valid(cleaned)

            phone = cleaned["phone"]
            email = cleaned["email"]
            duplicate_of = None

            # Duplicate detection happens after cleaning, as required by the spec.
            if phone and phone in seen_phones:
                duplicate_of = seen_phones[phone]
            if email and email in seen_emails and duplicate_of is None:
                duplicate_of = seen_emails[email]

            # Keep the first occurrence as the reference for later registrations.
            if phone and phone not in seen_phones:
                seen_phones[phone] = reg_id
            if email and email not in seen_emails:
                seen_emails[email] = reg_id

            record = {
                "id": reg_id,
                "name": cleaned["name"],
                "phone": cleaned["phone"],
                "email": cleaned["email"],
                "year": cleaned["year"],
                "branch": cleaned["branch"],
            }

            if duplicate_of:
                status = "duplicate"
                reasons.append(f"Duplicate of {duplicate_of}")
            elif reasons:
                status = "needs_fix"
            else:
                status = "valid"

            if status == "valid":
                valid_entries.append(record)
            else:
                problem_entries.append({
                    "id": reg_id,
                    "original_entry": original_entry,
                    "name": cleaned["name"] or "",
                    "phone": cleaned["phone"] or "",
                    "email": cleaned["email"] or "",
                    "year": cleaned["year"] if cleaned["year"] is not None else "",
                    "branch": cleaned["branch"] or "",
                    "status": status,
                    "reasons": "; ".join(reasons),
                })

            print(f"Status: {status}")

        except Exception as error:
            # API/network failures are processing problems, not proof of bad data.
            print(f"Processing error for {reg_id}: {error}")
            problem_entries.append({
                "id": reg_id,
                "original_entry": original_entry,
                "name": "",
                "phone": "",
                "email": "",
                "year": "",
                "branch": "",
                "status": "needs_fix",
                "reasons": f"Processing error (retry manually): {error}",
            })

    return valid_entries, problem_entries


# ============================================================
# 11. WRITE THREE REQUIRED REPORTS
# ============================================================

def write_reports(valid_entries, problem_entries):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # clean_list.csv
    clean_fields = ["id", "name", "phone", "email", "year", "branch"]
    with open(REPORTS_DIR / "clean_list.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=clean_fields)
        writer.writeheader()
        writer.writerows(valid_entries)

    # problems.csv
    problem_fields = [
        "id", "original_entry", "name", "phone", "email",
        "year", "branch", "status", "reasons",
    ]
    with open(REPORTS_DIR / "problems.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=problem_fields)
        writer.writeheader()
        writer.writerows(problem_entries)

    # summary.txt
    all_count = len(valid_entries) + len(problem_entries)
    duplicate_count = sum(item["status"] == "duplicate" for item in problem_entries)
    needs_fix_count = sum(item["status"] == "needs_fix" for item in problem_entries)

    branches = {}
    years = {}
    for item in valid_entries:
        branches[item["branch"]] = branches.get(item["branch"], 0) + 1
        years[item["year"]] = years.get(item["year"], 0) + 1

    with open(REPORTS_DIR / "summary.txt", "w", encoding="utf-8") as file:
        file.write("SCOOBYDO AI - REGISTRATION SUMMARY\n")
        file.write("==================================\n\n")
        file.write(f"Total registrations: {all_count}\n")
        file.write(f"Valid registrations: {len(valid_entries)}\n")
        file.write(f"Needs fixing: {needs_fix_count}\n")
        file.write(f"Duplicates: {duplicate_count}\n\n")

        file.write("VALID REGISTRATIONS BY BRANCH\n")
        file.write("-----------------------------\n")
        for branch, count in sorted(branches.items()):
            file.write(f"{branch}: {count}\n")

        file.write("\nVALID REGISTRATIONS BY YEAR\n")
        file.write("---------------------------\n")
        for year, count in sorted(years.items()):
            file.write(f"Year {year}: {count}\n")

    print("\nAll three reports generated successfully!")
    print(f"Reports folder: {REPORTS_DIR}")


# ============================================================
# 12. MAIN FUNCTION
# ============================================================

def main():
    print("\nWELCOME TO SCOOBYDO AI")
    print("======================")

    # Fail early with a clear message if the key or prompt is missing.
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError(
            "Gemini API key not found. Check the .env file in the main project folder."
        )
    load_system_prompt()

    valid_entries, problem_entries = process()
    write_reports(valid_entries, problem_entries)

    print("\nPROJECT COMPLETED!")
    print("Valid:", len(valid_entries))
    print("Problems:", len(problem_entries))


if __name__ == "__main__":
    main()
