# Reportrick

A CLI tool for creating weekly reports.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Run the interactive menu:

```bash
python3 bin/reportrick.py
```

## CLI usage

Add entries (categories are **case-sensitive** and must be `GREEN`, `AMBER`, `RED`, or `MEETING`):

```bash
python3 bin/reportrick.py add GREEN "Shipped onboarding flow"
python3 bin/reportrick.py add MEETING "Weekly sync with team"
```

List the current week report:

```bash
python3 bin/reportrick.py list
```

Open the menu explicitly:

```bash
python3 bin/reportrick.py menu
```

## Menu commands

When you run `python3 bin/reportrick.py` (or `menu`), you can choose:

1. Add new entry
2. Change calendar week or the year
3. Show work report
4. Export work report (HTML/PDF/HTML+PDF/Text)
5. Configure user data
6. Exit the program

While viewing the weekly report, you can also delete entries by choosing `d` and then selecting a category.

## Output

- The SQLite database is created on first run at `database/reportrick_database.sqlite`.
- Exported HTML/PDF reports are written to `work_report/jinja_workreport.html` and `work_report/jinja_workreport.pdf`.

## Troubleshooting

- Editable install fails with `file '.../bin/reportrick.py,' does not exist`:
  - Ensure the `setup.cfg` scripts list has no trailing commas and re-run `pip install -e .`.
