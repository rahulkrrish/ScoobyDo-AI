# SCOOBYDO AI
### AI-Powered Event Registration Cleaner and Verification System

**Student:** Rahul Krishna R  
**Programme:** MSc Software Systems  
**Institution:** Coimbatore Institute of Technology

## 1. Problem Statement and Objective

Event registration details are often collected through forms and informal messages. These entries may contain inconsistent formatting, missing information, invalid phone numbers, incorrect email formats and duplicate registrations. Manually checking these details takes time and can lead to mistakes.

ScoobyDo AI is a Python-based tool that uses Google Gemini AI to extract participant information and Python to clean, validate and identify duplicate registrations. It helps event organisers prepare accurate registration lists.

## 2. Input

The system accepts a CSV file named `registrations.csv` containing at least 20 registration entries.

The CSV contains two columns:

- `id` – Unique registration ID.
- `entry` – Original registration text provided by the participant.

## 3. AI Extraction and JSON Rules

Google Gemini extracts five fields from each registration:

- Name
- Phone
- Email
- Year
- Branch

The AI returns structured JSON. It must extract only information explicitly present in the original entry.

Rules:
- Name: Text or null, as written.
- Phone: Digits only; remove spaces, dashes and plus signs without changing digits.
- Email: Preserve as written; do not complete or correct it. Return null if written using words such as "at" or "dot".
- Year: Integer from 1 to 4. Final year means 4; Roman numerals I–IV represent years 1–4.
- Branch: CSE, IT, AIDS, ECE, EEE, MECH, CIVIL, other or null.

The AI must never invent or correct missing information.

## 4. Python Fact-Checking and Cleaning

Python verifies the extracted information against the original registration entry.

It applies the following rules:

- Names are converted to title case with single spaces.
- Phone numbers are cleaned and must contain exactly 10 digits, starting with 6, 7, 8 or 9.
- Email addresses are converted to lowercase and checked for one @ symbol, no spaces and a dot after @.
- Academic year must be between 1 and 4.
- Missing or invalid fields are flagged for correction.
- Missing or unrecognised branches are treated as problems.

All cleaning, validation and counting are performed using Python, not the AI model.

## 5. Duplicate Detection and Status

Duplicate detection takes place after cleaning.

If a cleaned phone number or email address matches an earlier registration, the entry is marked as a duplicate of the first matching registration.

Each registration receives one of three statuses:

- **Valid:** All required fields pass validation.
- **Needs Fix:** One or more required fields are missing or invalid.
- **Duplicate:** The cleaned phone number or email matches an earlier registration.

Duplicate status takes priority.

## 6. Output Files and Human Review

The system generates three output files:

- `clean_list.csv` – Contains valid registrations with cleaned details.
- `problems.csv` – Contains registrations requiring correction and duplicate entries, including reasons and original entries.
- `summary.txt` – Contains total counts by status and valid registration counts by branch and year.

The event team reviews every entry in `problems.csv` and contacts participants to confirm incorrect or missing information. The system does not automatically invent or correct participant details.

## 7. Technology Used

- Python – Cleaning, validation, duplicate detection and report generation.
- Google Gemini API – AI-based information extraction.
- CSV and JSON – Data storage and structured information exchange.

**Expected Outcome:** A reliable registration-cleaning tool that reduces manual checking, identifies invalid and duplicate entries, and helps event organisers maintain accurate participant records.