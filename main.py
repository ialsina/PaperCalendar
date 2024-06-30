from __future__ import annotations

from datetime import datetime, timedelta
from typing import Sequence, Optional
from ics import Calendar, Event

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, Flowable
import requests
from yaml import safe_load

import styles
import drawings

with open("config.yaml", "r", encoding="utf-8") as cf:
    URLS = safe_load(cf)["URLS"]

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def fetch_events_from_ics(url):
    """Function to fetch events from an online ICS calendar"""

    response = requests.get(url, timeout=60)
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


def week_view(start_date, events: Sequence[Event]):
    """Function to create a week view page with events."""

    elements = []

    title = Paragraph(
        (
            f"Week {start_date.strftime('%U')}: "
            f"{start_date.strftime('%B %d')} - "
            f"{(start_date + timedelta(days=6)).strftime('%B %d, %Y')}"
        ),
        styles.title,
    )
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    # Create week schedule table
    data = [["Time"] + WEEKDAYS]
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


def month_view(
    year: int,
    month: int,
    style: ParagraphStyle,  # pylint: disable=E0602
    events: Optional[Sequence[Event]] = None,
) -> Sequence[Flowable]:
    """Function to create a month view page with events."""

    if events is None:
        events = []

    elements = []

    title = Paragraph(f"{datetime(year, month, 1).strftime('%B %Y')}", styles.title)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    # Create month calendar table
    data = [[Paragraph(weekday[:3], styles.weekday) for weekday in WEEKDAYS]]
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
            day_events = [
                event.name
                for event in events
                if (
                    event.begin.year == year
                    and event.begin.month == month
                    and event.begin.day == day
                )
            ]
            day_cell = [Paragraph(f"{day}", style)]
            day_drawing = drawings.fit_rectangles(
                day_events,
                max_events=4,
                width=0.92 * styles.MONTH_TABLE_colWidth,
                max_height=(
                    styles.MONTH_TABLE_rowHeight
                    - getattr(style, "fontSize", 0)
                    - getattr(style, "spaceAfter", 0)
                )
                * 0.8,
                padding=2,
            )
            day_cell.append(day_drawing)
            month_calendar[-1].append(day_cell)
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
        colWidths=[styles.MONTH_TABLE_colWidth for _ in range(7)],
        rowHeights=[styles.MONTH_TABLE_headerHeight]
        + [styles.MONTH_TABLE_rowHeight for _ in range(len(month_calendar))],
    )
    table.setStyle(styles.month_table)
    elements.append(table)

    return elements


def main() -> None:
    # Set up the document
    doc = SimpleDocTemplate("calendar.pdf", pagesize=A4)

    # events = fetch_events_from_ics(ics_url)
    events = [event for url in URLS for event in fetch_events_from_ics(url)]

    # Compile the document with day, week, and month views
    elements = []

    # Example: Add one day view, one week view, and one month view with events
    now = datetime.now()

    elements.extend(
        day_view(
            now, list(filter(lambda event: event.begin.date() == now.date(), events))
        )
    )
    elements.append(Spacer(1, 36))
    elements.extend(week_view(now - timedelta(days=now.weekday()), events))
    elements.append(Spacer(1, 36))
    elements.extend(
        month_view(
            year=now.year,
            month=now.month,
            style=styles.minimalist,
            events=list(
                filter(lambda event: event.begin.date().month == now.month, events)
            ),
        )
    )

    doc.build(elements)


if __name__ == "__main__":
    main()
