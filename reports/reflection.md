# ScoobyDo AI – Project Reflection

Building ScoobyDo AI helped me understand how an AI application can solve a data-cleaning problem while still requiring rules and human oversight. The project focuses on registration messages containing inconsistent names, phone formats, email addresses, academic years and branches.

I used the Google Gemini API to extract five fields: name, phone, email, year and branch. The model is used for extraction, while Python performs fact checking, cleaning, validation, duplicate detection and report generation. This separation is important because a model may misunderstand a message or produce information that was not supplied.

The program preserves the original registration text. It checks extracted contact details against the source entry and does not complete missing phone digits or email addresses. Python standardises names, removes permitted phone formatting, validates mobile-number length and starting digits, converts email addresses to lowercase, and checks year and branch values.

Duplicate detection is performed after cleaning phone numbers and email addresses, so differently formatted versions of the same contact details can match. The program also checks identical original registration text before calling Gemini, allowing exact repeated entries to be identified even when an API request would otherwise fail. The first occurrence is retained; later matching entries are recorded as duplicates.

In the latest user-run sample execution, the program processed 25 registrations and generated 8 valid registrations, 8 entries needing fixes and 9 duplicates. The counts reconcile to 25. The evaluation harness reported 5 passed tests and 0 failed tests. The red-team script reported PASS for all three displayed scenarios: incomplete details, prompt injection and duplicate detection after cleaning.

Earlier execution attempts encountered Gemini 429 quota and 503 availability errors. The corrected program includes request spacing and retry/backoff handling for temporary API errors. A retry mechanism reduces the impact of transient failures but cannot guarantee availability when a quota is exhausted. API errors should not be interpreted as proof that a participant's data is invalid; they require a retry or manual review.

The main lesson is that AI should assist with extraction, not replace verification. Entries needing correction remain visible in `problems.csv`, where the event team can review them. The current tests provide evidence for the selected cases only; they do not prove that every possible input or prompt injection will be handled correctly. Future work could expand the test dataset, measure latency systematically and add a review interface for organisers.
