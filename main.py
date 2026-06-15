import json
import httpx
import sys
import re
import time
from datetime import datetime, timedelta, timezone
from icalendar import Calendar, Event
from zoneinfo import ZoneInfo

# Dictionary to replace category names with shorter versions
CATEGORY_REPLACEMENTS = {
    "Tagesangebot 1": "1",
    "Tagesangebot 2": "2", 
    "Tagesangebot 3": "3",
    "Tagesangebot 4": "4",
    "Tagesangebot 5": "5",
    "Gemüsebeilage": "Gemüse",
    "Stärkebeilage 1": "Beilage 1",
    "Stärkebeilage 2": "Beilage 2",
    "Stärkebeilage 3": "Beilage 3"
}

def clean_meal_name(meal_name):
    """Remove 'Begrenztes Angebot:' prefix from meal names"""
    return re.sub(r'^Begrenztes Angebot:\s*', '', meal_name)

def get_event_title_from_meals(meals):
    """Generate event title from the first words of main dishes (Tagesangebot 1-5)"""
    main_dishes = []
    for meal in meals:
        if meal['category'].startswith('Tagesangebot'):
            cleaned_meal = clean_meal_name(meal['meal'])
            # Extract first 1-2 words from the dish name
            words = cleaned_meal.split()
            if len(words) >= 2:
                # if less than 8 characters take first two words
                if len(words[0]) <= 8:
                    main_dishes.append(f"{words[0]} {words[1]}")
                else:
                    main_dishes.append(words[0])
            elif len(words) == 1:
                main_dishes.append(words[0])
    
    if main_dishes:
        return ", ".join(main_dishes[:5])  # Limit to first 5 dishes
    return "Mensa Menu"

# Fetch JSON Data
url = "https://sws.maxmanager.xyz/extern/mensa_stuttgart-vaihingen.json"

# Use a simple, descriptive user agent
headers = {
    "User-Agent": "mensa-to-ical/1.0 (Python-httpx)"
}

MAX_RETRIES = 10
BASE_TIMEOUT = 15  # Initial timeout in seconds
TIMEOUT_STEP = 5   # Add 5 seconds per retry
data = None

# Robust Network Fetch Loop (shared client keeps connections pooled)
with httpx.Client(headers=headers) as client:
    for attempt in range(1, MAX_RETRIES + 1):
        # Start with a practical timeout and increase gradually
        current_timeout = BASE_TIMEOUT + ((attempt - 1) * TIMEOUT_STEP)
        try:
            print(f"Attempt {attempt}/{MAX_RETRIES}: Fetching data (Timeout: {current_timeout}s)...")
            response = client.get(url, timeout=current_timeout)
            response.raise_for_status()
            data = response.json()
            print("Data fetched successfully!")
            break  # Exit loop on success
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as e:
            print(f"Attempt {attempt} failed due to: {type(e).__name__} - {e}")
            if attempt < MAX_RETRIES:
                # Wait longer between each retry: 10s -> 20s -> 30s
                sleep_duration = attempt * 10
                print(f"Waiting {sleep_duration} seconds before next attempt...")
                time.sleep(sleep_duration)
            else:
                print("All retry attempts failed. Exiting script.")
                sys.exit(1)

calendar = Calendar()
calendar.add('prodid', '-//Mensa Stuttgart Vaihingen//')
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
    
    # Generate a deterministic UID based on the date so calendar clients can track updates
    e.add('uid', f"{date_str}-mensa-stuttgart-vaihingen@maxmanager.xyz")
    
    # Generate event title from main dishes
    event_title = get_event_title_from_meals(meals)
    e.add('summary', event_title)
    
    # Prepare description with improved formatting
    description_parts = []
    for meal in meals:
        # Replace category names with shorter versions
        category = CATEGORY_REPLACEMENTS.get(meal['category'], meal['category'])
        
        # Clean meal name
        meal_name = clean_meal_name(meal['meal'])
        
        # Format the line
        line = f"{category}: {meal_name}"
        if meal['description']:
            line += f" - {meal['description']}"
        
        description_parts.append(line)
    
    description = "\n".join(description_parts)
    berlin_time = datetime.now(ZoneInfo("Europe/Berlin"))
    description += "\nUpdated: " + berlin_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    e.add('description', description)
    e.add('dtstart', dt)
    e.add('dtend', dt + timedelta(days=1))
    e.add('dtstamp', datetime.now(timezone.utc))
    calendar.add_component(e)

# Write to file (opened in binary mode)
try:
    with open("mensa.ics", "wb") as f:
        f.write(calendar.to_ical())
    print("ICS file generated cleanly as mensa.ics")
except IOError as e:
    print(f"Error writing file: {e}")
    sys.exit(1)
