import sys
from pathlib import Path

# Import functions from main.py
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from main import clean_phone, clean_email, clean, is_valid


# --------------------------------
# TEST 1: PHONE CLEANING
# --------------------------------

print("\nPHONE NUMBER TESTS")
print("------------------")

phone_tests = [
    ("+91 98400 12345", "9840012345"),
    ("09876543210", "9876543210"),
    ("9876543210", "9876543210"),
    ("1234567890", None),
    ("98765", None),
    (None, None)
]

for phone, expected in phone_tests:

    result = clean_phone(phone)

    status = "PASS" if result == expected else "FAIL"

    print(phone, "=>", result, "|", status)


# --------------------------------
# TEST 2: EMAIL CLEANING
# --------------------------------

print("\nEMAIL TESTS")
print("-----------")

email_tests = [
    ("RAHUL@gmail.com", "rahul@gmail.com"),
    ("student@example.com", "student@example.com"),
    ("wrongemail.com", None),
    ("abc@gmail", None),
    ("abc at gmail dot com", None),
    (None, None)
]

for email, expected in email_tests:

    result = clean_email(email)

    status = "PASS" if result == expected else "FAIL"

    print(email, "=>", result, "|", status)


# --------------------------------
# TEST 3: REGISTRATION VALIDATION
# --------------------------------

print("\nREGISTRATION VALIDATION")
print("-----------------------")

registration = {
    "name": "Rahul Krishna",
    "phone": "9876543210",
    "email": "rahul@gmail.com",
    "year": 2,
    "branch": "CSE"
}

cleaned = clean(registration)

problems = is_valid(cleaned)

if not problems:
    print("PASS: Registration is valid")
else:
    print("FAIL:", problems)


# --------------------------------
# TEST 4: INVALID REGISTRATION
# --------------------------------

print("\nINVALID REGISTRATION")
print("--------------------")

registration = {
    "name": "Rahul",
    "phone": None,
    "email": "wrongemail",
    "year": 5,
    "branch": "other"
}

cleaned = clean(registration)

problems = is_valid(cleaned)

print("Problems detected:")

for problem in problems:
    print("-", problem)


print("\nTESTING COMPLETED")
