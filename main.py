"""
Main script to generate a PDF calendar with day, week, and month views using ReportLab.

This script fetches events from multiple online ICS calendars specified in a `config.yaml` file,
combines them with hardcoded events, and generates a PDF calendar with day, week, and month views
for the current date using ReportLab.

Constants:
- URLS: List of URLs from the `config.yaml` file containing ICS calendar URLs.

Execution:
When executed as a standalone script, `main()` is called, which:
1. Reads the calendar URLs from `config.yaml`.
2. Fetches events from each URL using `fetch_events_from_ics`.
3. Adds hardcoded events to the fetched events list.
4. Compiles day, week, and month views for the current date into a PDF document named `calendar.pdf`.

Note:
This script requires ReportLab for PDF generation and `ics` library for parsing ICS calendars.
Make sure to have the necessary dependencies installed before running this script.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Sequence, Optional, Tuple
from ics import Calendar, Event

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
import requests
from yaml import safe_load

import styles
import drawings

with open("config.yaml", "r", encoding="utf-8") as cf:
    URLS = safe_load(cf)["URLS"]


def fetch_events_from_ics(url):
    """Fetch events from an online ICS calendar.

    Args:
        url (str): The URL of the ICS calendar.

    Returns:
        list: A list of Event objects parsed from the ICS calendar.

    If fetching the calendar fails (HTTP status code other than 200),
    an empty list is returned.
    """

    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        calendar = Calendar(response.text)
        return calendar.events
    print(f"Failed to fetch calendar from {url}")
    return []


def day_view(
    date: datetime,
    events: Sequence[Event],
    hour_span: Optional[Tuple[int, int]] = (6, 23),
):
    """Function to create a day view page with events"""

    elements = []

    title = Paragraph(f"{date.strftime(r'%A, %B %d, %Y')}", styles.title)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    table = drawings.draw_day_schedule(
        events,
        width=styles.day.colWidth + styles.day.colWidth,
        height=styles.day.rowHeight * (hour_span[1] - hour_span[0]),
        hour_span=hour_span,
        line_width=styles.day.lineWidth,
        time_col_width=styles.day.timeWidth,
    )
    elements.append(table)

    return elements


def week_view(
    start_date: datetime,
    events: Sequence[Event],
    hour_span: Optional[Tuple[int, int]] = (6, 23),
):
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
    table = drawings.draw_week_schedule(
        events=events,
        start_date=start_date,
        day_width=styles.week.colWidth,
        height=styles.week.headerHeight
        + styles.week.rowHeight * (hour_span[1] - hour_span[0]),
        hour_span=hour_span,
        time_col_width=styles.week.timeWidth,
        w_style=styles.weekday
    )
    elements.append(table)

    return elements


def month_view(
    year: int,
    month: int,
    events: Optional[Sequence[Event]] = None,
) -> Sequence[Flowable]:
    """Function to create a month view page with events."""

    if events is None:
        events = []

    elements = []

    title = Paragraph(f"{datetime(year, month, 1).strftime('%B %Y')}", styles.title)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add some space below the title

    table = drawings.draw_month_schedule(
        year=year,
        month=month,
        events=events,
        p_style=styles.minimalist,
        t_style=styles.month_table,
        w_style=styles.weekday,
        table=styles.month,
    )
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
            events=list(
                filter(lambda event: event.begin.date().month == now.month, events)
            ),
        )
    )

    doc.build(elements)


if __name__ == "__main__":
    main()
