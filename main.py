from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from datetime import datetime, timedelta
import requests
from ics import Calendar
from yaml import safe_load

import styles

with open("config.yaml", "r", encoding="utf-8") as cf:
    URLS = safe_load(cf)["URLS"]

WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Set up the document
doc = SimpleDocTemplate("calendar.pdf", pagesize=A4)


def fetch_events_from_ics(url):
    """Function to fetch events from an online ICS calendar"""

    response = requests.get(url)
    if response.status_code == 200:
        calendar = Calendar(response.text)
        return calendar.events
    print(f"Failed to fetch calendar from {url}")
    return []


def day_view(date, events):
    """Function to create a day view page with events"""

    elements = []

    title = Paragraph(f"{date.strftime(r'%A, %B %d, %Y')}", styles.title)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    # Create hourly schedule table
    data = [["Time", "Task"]]
    for hour in range(6, 22):  # 6 AM to 10 PM
        hour_str = f"{hour}:00"
        tasks = [event.name for event in events if event.begin.hour == hour]
        data.append(
            [
                Paragraph(hour_str, styles.minimalist),
                Paragraph("\n".join(tasks), styles.minimalist),
            ]
        )

    table = Table(
        data, colWidths=[50, 490], rowHeights=[24] + [36 for _ in range(16)]
    )  # Adjusted colWidths and rowHeights
    table.setStyle(styles.day_table)
    elements.append(table)

    return elements


def week_view(start_date, events):
    """Function to create a week view page with events."""
    elements = []

    title = Paragraph(
        f"Week {start_date.strftime('%U')}: {start_date.strftime('%B %d')} - {(start_date + timedelta(days=6)).strftime('%B %d, %Y')}",
        styles.title,
    )
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    # Create week schedule table
    data = [
        [
            "Time",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    ]
    for hour in range(6, 22):  # 6 AM to 10 PM
        row = [Paragraph(f"{hour}:00", styles.minimalist)]
        for day in range(7):
            day_date = start_date + timedelta(days=day)
            day_events = [
                event.name
                for event in events
                if event.begin.date() == day_date.date() and event.begin.hour == hour
            ]
            row.append(Paragraph("\n".join(day_events), styles.minimalist))
        data.append(row)

    table = Table(
        data,
        colWidths=[50] + [60 for _ in range(7)],
        rowHeights=[24] + [36 for _ in range(16)],
    )  # Adjusted colWidths and rowHeights
    table.setStyle(styles.week_table)
    elements.append(table)

    return elements


def month_view(year, month, events):
    """Function to create a month view page with events."""

    elements = []

    title = Paragraph(f"{datetime(year, month, 1).strftime('%B %Y')}", styles.title)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    # Create month calendar table
    data = [[Paragraph(weekday, styles.weekday) for weekday in WEEKDAYS]]
    month_calendar = [[]]

    start_day = datetime(year, month, 1).weekday()  # 0 is Monday, 6 is Sunday

    # Fill in leading empty cells before the first day of the month
    for _ in range(start_day):
        month_calendar[-1].append("")

    day = 1
    while day <= 31:
        try:
            if len(month_calendar[-1]) == 7:
                month_calendar.append([])
            day_events = [event.name for event in events if event.begin.day == day]
            month_calendar[-1].append(
                Paragraph(f"{day}\n" + "\n".join(day_events), styles.minimalist)
            )
            day += 1
        except ValueError:
            break

    # Fill in remaining blanks if necessary
    while len(month_calendar[-1]) < 7:
        month_calendar[-1].append("")

    for week in month_calendar:
        data.append(week)

    table = Table(
        data,
        colWidths=[50 for _ in range(7)],
        rowHeights=[24] + [84 for _ in range(len(month_calendar))],
    )  # Adjusted colWidths and rowHeights
    table.setStyle(styles.month_table)
    elements.append(table)

    return elements


# events = fetch_events_from_ics(ics_url)
events = [event for url in URLS for event in fetch_events_from_ics(url)]

# Compile the document with day, week, and month views
all_elements = []

# Example: Add one day view, one week view, and one month view with events
now = datetime.now()

all_elements.extend(
    day_view(now, list(filter(lambda event: event.begin.date() == now.date(), events)))
)
all_elements.append(Spacer(1, 36))
all_elements.extend(week_view(now - timedelta(days=now.weekday()), events))
all_elements.append(Spacer(1, 36))
all_elements.extend(
    month_view(
        now.year,
        now.month,
        list(filter(lambda event: event.begin.date().month == now.month, events)),
    )
)

doc.build(all_elements)