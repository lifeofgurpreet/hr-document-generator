# Repository Guidelines

## Project Structure & Module Organization
- `app.py`: Flask UI for generating and downloading documents.
- `scripts/`: CLI tools — `generate-documents.py`, `ai-helper.py`, `pdf-converter.py`.
- `templates/`: Jinja2-ready Markdown templates (`contract.md`, `roles-responsibilities.md`, `confirmation.md`).
- `config/`: JSON config (`company-info.json`, `job-roles.json`, `ai-prompts.json`).
- `output/`: Generated files per employee (e.g., `output/Jane_Doe/`).
- `hr_interface.html`: Local UI page served by Flask.
- `test_system.py`: Smoke test and system overview.

## Build, Test, and Development Commands
- Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run CLI (interactive): `python scripts/generate-documents.py --interactive`.
- Run CLI (quick): `python scripts/generate-documents.py --employee "John Doe" --role "Marketing Associate" --salary "RM 5000"`.
- Batch mode: `python scripts/generate-documents.py --batch sample_employees.csv`.
- Web UI: `export OPENAI_API_KEY=... && python app.py` then open `http://localhost:5000`.
- Convert to PDF: `python scripts/pdf-converter.py output/Jane_Doe/`.
- Smoke tests: `python test_system.py`.

## Coding Style & Naming Conventions
- Python 3.10+; follow PEP 8 with 4‑space indentation and type hints where practical.
- Use `snake_case` for functions/variables, `PascalCase` for classes, lowercase file names with underscores for importable modules.
- Templates use Jinja-style placeholders (e.g., `{{ employee_name }}`) and Markdown headings.
- Config files are JSON; prefer stable keys and explicit defaults.

## Testing Guidelines
- Primary smoke test: `python test_system.py` (loads configs, renders templates, writes to `output/test_employee`).
- Add focused tests by extending `test_system.py` to cover template rendering, CSV parsing, and PDF conversion.
- Aim to validate: required fields present, templates render without errors, and outputs are created in the expected paths.

## Commit & Pull Request Guidelines
- Commit messages: imperative mood with scope, e.g., `scripts: add batch CSV validation`, `templates: refine contract header`.
- PRs must include: clear summary, linked issue (if any), testing steps/commands, and sample output paths or screenshots.
- Do not include secrets or PII; exclude `output/` artifacts from commits.

## Security & Configuration Tips
- Secrets: set `OPENAI_API_KEY` via environment variables or `.env` (supported by `python-dotenv`). Never commit keys.
- Data hygiene: generated documents may contain PII; keep `output/` local and ephemeral.
- Network usage: AI features require connectivity; scripts gracefully degrade when unavailable.
