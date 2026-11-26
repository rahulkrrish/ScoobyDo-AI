# ScoobyDo AI – Test Execution Record

**Date of reported execution:** 26 November 2026  
**Execution environment:** User's Windows 11 / VS Code project environment  
**Evidence basis:** Terminal screenshots shared by the user in the project conversation.

| Test group | Tests | Passed | Failed | Result |
|---|---:|---:|---:|---|
| Evaluation harness | 5 | 5 | 0 | PASS |
| Red-team script | 3 | 3 | 0 | PASS |
| **Combined** | **8** | **8** | **0** | **PASS** |

## Application output summary

The user's latest generated report showed:

| Classification | Count |
|---|---:|
| Valid registrations | 8 |
| Needs fixing | 8 |
| Duplicates | 9 |
| **Total** | **25** |

The branch and academic-year breakdowns in `summary.txt` each reconcile to the 8 valid registrations.

## Scope and limitations

The results were reported from the user's local execution; this package records those results and does not claim that a new Gemini API run was performed while packaging. The test suite is small and covers only the listed scenarios. The 100% evaluation score means 5 of 5 predefined cases passed, not that the system is 100% accurate for all real-world inputs.
