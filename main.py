import json
import httpx
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import sys

# Fetch JSON Data
url = "https://sws.maxmanager.xyz/extern/mensa_stuttgart-vaihingen.json"

try:
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
except httpx.RequestError as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    sys.exit(1)

calendar = Calendar()
calendar.add('prodid', '-//Mensa Stuttgart Vaihingen//lgeiger.de//')
calendar.add('version', '2.0')

if not data:
    print("No data received from API")
    sys.exit(1)

mensa_name = list(data.keys())[0]
dates = data[mensa_name]

if not dates:
    print("No menu dates available")
    sys.exit(1)

for date_str, meals in dates.items():
    # For all-day events, DTSTART is date, DTEND is date+1 (non-inclusive)
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    e = Event()
    e.add('summary', f"{mensa_name}")
    # Prepare description
    description = "\n".join(
        [f"{meal['category']}: {meal['meal']}" +
            (f" - {meal['description']}" if meal['description'] else "")
         for meal in meals]
    )
    e.add('description', description)
    e.add('dtstart', dt)
    e.add('dtend', dt + timedelta(days=1))
    e.add('dtstamp', datetime.utcnow())
    calendar.add_component(e)

# Write to file (must be opened in binary mode!)
try:
    with open("mensa.ics", "wb") as f:
        f.write(calendar.to_ical())
    print("ICS file generated as mensa.ics")
except IOError as e:
    print(f"Error writing file: {e}")
    sys.exit(1)
