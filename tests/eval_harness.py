import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from main import extract_details, check_facts, clean, is_valid


TEST_CASES = [
    {
        "id": "E01",
        "entry": "Name: Rahul K, phone 9840012345, email rahul@gmail.com, 2nd year CSE",
        "expected_status": "valid",
        "expected_phone": "9840012345"
    },
    {
        "id": "E02",
        "entry": "Name: Arun Kumar, phone +91 98765 43210, email arun@gmail.com, III year ECE",
        "expected_status": "valid",
        "expected_phone": "9876543210"
    },
    {
        "id": "E03",
        "entry": "Name: Kavya R, phone 12345, email kavya@gmail.com, 1st year IT",
        "expected_status": "needs_fix",
        "expected_phone": None
    },
    {
        "id": "E04",
        "entry": "Name: Manoj K, phone 9876543211, email manoj at gmail dot com, 2nd year CSE",
        "expected_status": "needs_fix",
        "expected_phone": "9876543211"
    },
    {
        "id": "E05",
        "entry": "Name: Aishwarya S, phone 9876543212, email aishwarya@gmail.com, 5th year BBA",
        "expected_status": "needs_fix",
        "expected_phone": "9876543212"
    }
]


def run_evaluation():

    passed = 0

    print("\nSCOOBYDO AI - EVALUATION TEST")
    print("=============================\n")

    for case in TEST_CASES:

        print("Testing:", case["id"])

        try:
            extracted = extract_details(case["entry"])

            extracted = check_facts(
                extracted,
                case["entry"]
            )

            cleaned = clean(extracted)

            problems = is_valid(cleaned)

            actual_status = "needs_fix" if problems else "valid"
            actual_phone = cleaned["phone"]

            status_correct = actual_status == case["expected_status"]
            phone_correct = actual_phone == case["expected_phone"]

            if status_correct and phone_correct:
                result = "PASS"
                passed += 1
            else:
                result = "FAIL"

            print("Expected status:", case["expected_status"])
            print("Actual status:", actual_status)

            print("Expected phone:", case["expected_phone"])
            print("Actual phone:", actual_phone)

            print("Result:", result)
            print("-----------------------------")

        except Exception as error:
            print("ERROR:", error)
            print("Result: NOT COMPLETED")
            print("-----------------------------")

        time.sleep(5)

    print("\nEVALUATION SUMMARY")
    print("==================")
    print("Total tests:", len(TEST_CASES))
    print("Passed:", passed)
    print("Failed:", len(TEST_CASES) - passed)

    accuracy = (passed / len(TEST_CASES)) * 100

    print("Accuracy:", round(accuracy, 2), "%")


if __name__ == "__main__":
    run_evaluation()