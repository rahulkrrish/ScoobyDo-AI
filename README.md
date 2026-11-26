# ScoobyDo AI – Event Registration Cleaner

## 1. Project Overview

ScoobyDo AI is an AI-powered event registration cleaning system developed using Python and the Google Gemini API.

It helps event organisers process messy registration details received through forms and WhatsApp messages.

The system extracts participant information, validates the details, identifies duplicate registrations and generates organised reports.

The main objective is to reduce manual data-cleaning work while preventing incorrect contact information from entering the final registration list.

## 2. Features

- Extracts participant details using Google Gemini AI.
- Reads registration data from CSV files.
- Validates phone numbers and email addresses.
- Standardises names and contact information.
- Validates academic year and branch.
- Identifies duplicate registrations.
- Separates valid and problematic registrations.
- Generates summary reports automatically.

## 3. Technologies Used

- Python
- Google Gemini API
- Google Gen AI SDK
- CSV module
- Regular Expressions
- python-dotenv
- VS Code

## 4. Project Structure

```text
ScoobyDo_AI/
│
├── data/
│   └── registrations.csv
│
├── src/
│   ├── main.py
│   ├── csv_reader.py
│   └── system_prompt.txt
│
├── tests/
│   ├── test_cleaning.py
│   ├── eval_harness.py
│   └── red_team.py
│
├── reports/
│   ├── judgment_framework.md
│   ├── evaluation_results.md
│   ├── red_team_results.md
│   ├── clean_list.csv
│   ├── problems.csv
│   ├── summary.txt
│   ├── red_team_results.md
│   └── cost_latency_note.md
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## 5. Installation

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd ScoobyDo_AI
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## 6. API Configuration

Create a `.env` file in the project root directory.

Add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Obtain an API key through Google AI Studio.

Never upload your actual API key to GitHub.

## 7. Input Format

The application reads registration information from:

`data/registrations.csv`

The CSV contains two columns:

| Column | Description |
|---|---|
| id | Unique registration identifier |
| entry | Original registration message |

Example:

```csv
id,entry
R01,"Name: Priya K, phone 98400 12345, email priya@gmail.com, 2nd year CSE"
```

## 8. How to Run

From the project root directory, activate the virtual environment and execute:

```bash
python src/main.py
```

The program processes registrations and generates three output files.

## 9. Output Files

### clean_list.csv
Contains registrations that passed validation and duplicate checks.

### problems.csv
Contains registrations that need correction or are identified as duplicates, along with reasons and original entries.

### summary.txt
Contains:
- Total registrations
- Valid registrations
- Registrations needing correction
- Duplicate registrations
- Valid registrations by branch
- Valid registrations by academic year

## 10. Testing

The project includes:

- `test_cleaning.py` – Tests Python cleaning and validation functions.
- `eval_harness.py` – Evaluates five predefined registration examples.
- `red_team.py` – Tests incomplete details, prompt injection and duplicate formatting.

## 11. Project Outcome

ScoobyDo AI successfully processed 25 sample registration entries.

The generated summary contained:

- Total registrations: 25
- Valid registrations: 8
- Needs fixing: 8
- Duplicates: 9

The system demonstrates how AI-based information extraction can be combined with Python validation and cleaning to improve registration data quality.

## 12. Future Improvements

- Continue improving extraction reliability for unusual registration formats.
- Support larger registration datasets.
- Introduce a graphical user interface.
- Expand evaluation and red-team coverage beyond the current test cases.

---

**Developed as part of the CIT MSc Software Systems programme.**