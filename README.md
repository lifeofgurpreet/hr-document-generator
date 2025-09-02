# HR Onboarding Automation System

This system automates HR documents (employment contracts, roles & responsibilities, and confirmation letters) using Jinja2 templates with optional OpenAI enhancements.

## Quick Start

1) Install dependencies
```bash
pip install -r requirements.txt
```

2) Run the Web UI (fallbacks work without AI)
```bash
python app.py
# Open http://localhost:5001
```

3) Optional: enable AI
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Project Structure

```
HRTemplate/
├── templates/                 # Markdown + Jinja2 templates
│   ├── contract.md
│   ├── roles-responsibilities.md
│   └── confirmation.md
├── config/                    # JSON configs
│   ├── company-info.json
│   ├── job-roles.json
│   └── ai-prompts.json
├── scripts/
│   ├── generate-documents.py  # CLI generator
│   ├── ai_helper.py           # OpenAI v1 helper (optional)
│   └── pdf-converter.py       # Markdown → PDF
├── output/                    # Generated files (gitignored)
├── sample/                    # Sample inputs
├── hr_interface.html          # Web UI page
├── test_system.py             # Smoke test
└── app.py                     # Flask server (UI + generation)
```

## Usage

- CLI (interactive): `python scripts/generate-documents.py --interactive`
- CLI (quick): `python scripts/generate-documents.py --employee "John Doe" --role "Marketing Associate" --salary "RM 5000"`
- CLI (batch): `python scripts/generate-documents.py --batch sample_employees.csv`
- Web UI: `python app.py` then open http://localhost:5001
- PDF: `python scripts/pdf-converter.py output/Jane_Doe/`

## Notes

- Without `OPENAI_API_KEY`, the app renders templates from `config/` reliably.
- KPI keys are normalized; activities are populated even without AI.
- Generated content and `.env` are gitignored by default.

---

**Note**: This system is designed for internal HR use. Ensure compliance with local labor laws and company policies when generating employment documents.
