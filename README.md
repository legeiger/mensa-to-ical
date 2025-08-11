# Mensa Stuttgart Vaihingen Calendar

This repository automatically generates an iCalendar file (`.ics`) with daily menus from Mensa Stuttgart Vaihingen.

## Files

- `main.py` - Main script that fetches menu data and generates the calendar
- `mensa.ics` - Generated iCalendar file (updated daily at 5 AM UTC)
- `requirements.txt` - Python dependencies

## Usage

### Subscribe to the calendar

You can subscribe to the calendar using the following URL:
```
https://raw.githubusercontent.com/legeiger/mensa-to-ical/main/mensa.ics
```

### Manual run

To run the script manually:

```bash
pip install -r requirements.txt
python main.py
```

## Automation

The calendar is automatically updated daily at 5:00 AM UTC using GitHub Actions. The workflow:

1. Fetches the latest menu data from the Mensa API
2. Generates a new `mensa.ics` file
3. Commits and pushes the updated file to the repository

## Data Source

Menu data is fetched from: `https://sws.maxmanager.xyz/extern/mensa_stuttgart-vaihingen.json`
