# SCOOBYDO AI
## Judgment Framework

### Purpose

This framework explains which parts of ScoobyDo AI can be automated, what risks may arise, and where human judgment is required. The guiding principle is that Gemini extracts information, Python applies fixed rules, and the event team resolves uncertain registrations.

### Three judgment questions

For every stage of the system, the following questions are considered:

1. **What is being decided or automated?** Identify the task performed by the AI or Python.
2. **What could go wrong, and who could be affected?** Identify the possible error and its impact on a participant or the event team.
3. **Who checks it, and what is the human checkpoint?** State how the result is verified and who is responsible for action.

### Judgment framework table

| System part | 1. What is automated or decided? | 2. What could go wrong / who is affected? | 3. Human check and responsibility |
|---|---|---|---|
| Reading the input CSV | Python reads each registration ID and its original entry. | A malformed or missing row could be skipped or fail to process. The participant's registration may be missed. | The event team should check the source CSV and the processing-error entries in `problems.csv`. |
| LLM information extraction | Gemini extracts name, phone, email, year and branch into the required JSON fields. It is not allowed to invent or correct details. | The model may misread a message, omit a field, or return a detail that was not present. A participant could be contacted using incorrect information. | Python's `check_facts()` checks extracted phone and email information against the original entry. The event team reviews uncertain records. |
| Phone-number fact check and cleaning | Python removes permitted formatting characters and checks that the digits came from the original entry. It then checks for a 10-digit number beginning with 6, 7, 8 or 9, after permitted prefix removal. | A wrong extraction or invalid number may prevent the participant from being contacted. Changing even one digit could direct communication to another person. | **No phone digit is guessed, added, removed or changed.** Invalid or missing numbers remain in `problems.csv`; the event team contacts the participant to confirm the correct number. |
| Email fact check and cleaning | Python checks that the extracted email appears in the original entry, converts it to lowercase, and checks basic format rules. | An invented or silently completed email could send event information to the wrong address or cause a participant to miss updates. | **The system never completes or corrects an email address.** Missing or invalid emails are sent to `problems.csv` for confirmation by the event team. |
| Name, year and branch cleaning | Python standardises name spacing and title case, converts recognised year forms to numbers, and checks the allowed branch list. | A year or branch may be misunderstood, which could affect grouping, eligibility checks or event reporting. | The event team checks missing, invalid or unrecognised values in `problems.csv` against the participant's confirmation or source form. |
| Validation and status assignment | Python assigns `valid`, `needs_fix` or `duplicate` using the specification's rules. | A field that passes a basic format check may still be factually wrong. A participant could be incorrectly treated as fully registered. | A `valid` status means only that the programmed checks passed; it is not proof of the participant's identity or attendance. The event team remains responsible for final registration decisions. |
| Duplicate detection | Python compares cleaned phone numbers and email addresses and marks later matching registrations as duplicates of the first one. | Two different people may share a contact detail, or the same person may use different contact details. Incorrectly merging records could remove a genuine participant. | Duplicates are not silently deleted. They remain visible in `problems.csv`; the event team checks whether they are truly the same participant before taking action. |
| Report generation | Python writes `clean_list.csv`, `problems.csv` and `summary.txt`, including counts by status, branch and year. | A software error or failed LLM request could make the summary incomplete or counts misleading. | The event team should compare the report totals with the input row count and inspect processing errors and problem records before using the clean list. |

### Contact-detail judgment: the most important boundary

Phone numbers and email addresses are personal contact details. A plausible-looking correction is still a guess. ScoobyDo AI therefore does not:

- add missing phone digits;
- change phone digits;
- add a missing email ending such as `.com`;
- convert an email written in words such as “at” or “dot” into a guessed address; or
- silently discard a duplicate or problematic registration.

The system preserves the original entry in `problems.csv` so that the event team can see what the participant actually submitted.

### Named human checkpoint

**The event team is the human checkpoint.** The team must review every entry in `problems.csv`, contact the participant to confirm missing or incorrect details, and decide whether duplicate records refer to the same person. Only after that review should the team update its official registration records.

The AI does not contact participants, approve uncertain details, or make final registration decisions.

### Conclusion

ScoobyDo AI uses automation for repetitive extraction, formatting, validation and duplicate checks. It keeps consequential decisions about uncertain identity and contact details with the event team. This division reduces manual work without treating an AI-generated result as unquestionable fact.
