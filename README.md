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

## Functions (menu actions)

### Add new entry

1. Run `python3 bin/reportrick.py`
2. Choose `1` (Add new entry)
3. Enter the entry text
4. Pick a category (`GREEN`, `AMBER`, `RED`, or `MEETING`)

You can also add entries directly via CLI:

```bash
python3 bin/reportrick.py add GREEN "Shipped onboarding flow"
```

### Change calendar week or the year

Use this when you need to log or view entries for a different week/year:

1. Run `python3 bin/reportrick.py`
2. Choose `2`
3. Enter the target year
4. Enter the target calendar week

### Show work report

1. Run `python3 bin/reportrick.py`
2. Choose `3`

This prints the current week’s report grouped by category.

### Export work report

1. Run `python3 bin/reportrick.py`
2. Choose `4`
3. Select the output format:
   - `1` HTML
   - `2` PDF
   - `3` HTML and PDF
   - `4` Text (currently no file output)

### Configure employee name and department

Use the menu to set employee details (stored in the local SQLite database):

1. Run `python3 bin/reportrick.py`
2. Choose `5` (Configure user data)
3. Enter first name, last name, and team name (department)

To update these later, choose option `5` again.

### Delete an entry

1. Open the weekly report (`3`)
2. Press `d`
3. Select the category
4. Enter the exact entry text to remove

## Output

- The SQLite database is created on first run at `database/reportrick_database.sqlite`.
- Exported HTML/PDF reports are written to `work_report/jinja_workreport.html` and `work_report/jinja_workreport.pdf`.

## Troubleshooting

- Editable install fails with `file '.../bin/reportrick.py,' does not exist`:
  - Ensure the `setup.cfg` scripts list has no trailing commas and re-run `pip install -e .`.
