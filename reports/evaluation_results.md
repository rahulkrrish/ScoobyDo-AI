# ScoobyDo AI – Evaluation Harness Results

## Latest recorded run

The user ran `python tests/eval_harness.py` in the project environment and shared the terminal result on 26 November 2026.

| Metric | Result |
|---|---:|
| Total test cases | 5 |
| Passed | 5 |
| Failed | 0 |
| Accuracy | 100.0% |
| Overall result | PASS |

## Test coverage

The harness contains five predefined cases:

1. Normal valid registration.
2. Phone number with +91 country code.
3. Invalid short phone number.
4. Email written using words such as “at” and “dot”.
5. Invalid academic year and unrecognised branch.

## Interpretation

All five test cases passed in the reported run. This result applies to the five cases in the harness and is not a guarantee of correctness for every possible registration format.
