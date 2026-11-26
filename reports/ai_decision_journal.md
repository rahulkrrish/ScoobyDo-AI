# SCOOBYDO AI
## AI Decision Journal

### Project Overview
ScoobyDo AI uses the Google Gemini API to extract registration details from unstructured messages. Python handles validation, cleaning, duplicate detection and report generation.

### Decision 1: Using Gemini for Information Extraction

**Decision:** Use Google Gemini API to extract name, phone, email, year and branch.

**Reason:** Registration messages arrive in different formats. Gemini can identify the required information from these messages.

**Responsibility:** Gemini extracts information; Python verifies it.

### Decision 2: Preventing Incorrect Information

**Decision:** Never allow the AI to invent missing phone digits or complete email addresses.

**Reason:** Incorrect contact information could cause communication problems.

**Implementation:** The `check_facts()` function checks extracted contact details against the original registration.

### Decision 3: Python-Based Cleaning

**Decision:** Perform all cleaning and validation using Python.

**Reason:** Cleaning rules should be consistent and predictable.

**Implementation:**
- Standardise names.
- Validate phone numbers.
- Convert emails to lowercase.
- Validate academic years.
- Check permitted branches.

### Decision 4: Duplicate Detection

**Decision:** Identify duplicates after cleaning phone numbers and email addresses.

**Reason:** The same contact information may be written in different formats.

**Implementation:** Python dictionaries track previously encountered phone numbers and email addresses.

### Decision 5: Handling Incomplete Registrations

**Decision:** Do not silently discard incomplete or invalid registrations.

**Reason:** The event team must be able to identify and correct problematic entries.

**Implementation:** Store them in `problems.csv` with reasons and original registration text.

### Decision 6: Handling API Rate Limits

**Problem:** Gemini returned a 429 RESOURCE_EXHAUSTED error during processing.

**Decision:** Introduce a five-second delay between API requests.

**Reason:** Reduce the likelihood of exceeding the free-tier request limit.

### Decision 7: Testing and Security

**Decision:** Create an evaluation harness and red-team tests.

**Reason:** Check extraction reliability and resistance to unusual inputs.

**Implementation:** Five evaluation cases were prepared, along with three red-team scenarios covering incomplete information, prompt injection and duplicate formatting.

### Human Checkpoint

The event team is responsible for contacting participants whose registrations appear in `problems.csv`. AI does not independently correct or approve uncertain contact information.

### Conclusion

The main design principle of ScoobyDo AI is to use AI for extraction while keeping validation, cleaning and important decisions under Python and human control.