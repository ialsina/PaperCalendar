"""
Module containing functions and utilities to draw schedules and event visualizations
using ReportLab.

Constants:
- BUBBLE_RADIUS: Radius for bubble shapes.
- FONT_SIZE: Font size for text in shapes.
- FILL_COLOR: Fill color for shapes.
- WEEKDAYS: List of weekdays for reference.

This module utilizes ReportLab's Drawing and Table classes to create visual representations
of schedules and events based on provided data.
"""

from datetime import time, datetime, timedelta
from math import floor
from typing import Sequence, Optional, Tuple

from ics import Event
from reportlab.graphics.shapes import Drawing, Circle, String, Rect, Line
from reportlab.lib.colors import black, white
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

from styles import TableMeasurements


BUBBLE_RADIUS = 5
FONT_SIZE = 4
FILL_COLOR = white

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def circle(event_name: str, r: Optional[float] = None):
    if r is None:
        r = BUBBLE_RADIUS
    drawing = Drawing(2 * BUBBLE_RADIUS, 2 * BUBBLE_RADIUS)
    bubble = Circle(BUBBLE_RADIUS, BUBBLE_RADIUS, BUBBLE_RADIUS, fillColor=black)
    event_text = String(
        r,
        r,
        event_name,
        textAnchor="middle",
        fontSize=FONT_SIZE,
        fillColor=FILL_COLOR,
    )
    drawing.add(bubble)
    drawing.add(event_text)
    return drawing


def _rectangle_shape_text(text, x, y, w, h):
    rxy = max(w, h) / 100
    shape = Rect(x, y, w, h, fillColor=black, strokeColor=black, rx=rxy, ry=rxy)
    event_text = String(
        w / 2 + x,
        h / 2 + y,
        text,
        textAnchor="middle",
        fontSize=6,
        fillColor=white,
    )
    return shape, event_text


def rectangle(
    event_name: str, width: float = 30, height: float = 10, x: float = 0, y: float = 0
):
    drawing = Drawing(width, height)
    shape, text = _rectangle_shape_text(event_name, x, y, width, height)
    drawing.add(shape)
    drawing.add(text)
    return drawing


def fit_rectangles(
    events: Sequence[str],
    width: int,
    max_height: int,
    padding: int = 2,
    max_events: int = 4,
):
    drawing = Drawing(width, max_height)
    events = events[:max_events]
    height = (max_height - padding * (len(events) - 1)) / max(len(events), 1)
    for index, event in enumerate(events):
        y = (height + padding) * index
        shape, text = _rectangle_shape_text(event, 0, y, width, height)
        drawing.add(shape)
        drawing.add(text)
    return drawing


def _time_to_float(t: time):
    return t.hour + t.minute / 60 + t.second / 3600


def draw_schedule(
    events: Sequence[Event],
    width: int,
    height: int,
    hour_min: int,
    hour_max: int,
    line_width: float = 0,
):
    drawing = Drawing(width, height)

    total_hours = hour_max - hour_min

    for event in events:
        # Calculate heights and adjust based on line widths
        event_start_float = _time_to_float(event.begin.time())
        event_end_float = _time_to_float(event.end.time())

        y0 = height * (hour_max - event_start_float) / total_hours
        y1 = height * (hour_max - event_end_float) / total_hours

        # Adjust for line widths
        y0 += floor(event_start_float - hour_min) * line_width
        y1 += floor(event_end_float - hour_min) * line_width

        shape, text = _rectangle_shape_text(event.name, 0, y0, width, y1 - y0)
        drawing.add(shape)
        drawing.add(text)

    return drawing


def add_day_events(drawing, events, x, width, total_height, hour_span, header_height=0):
    hour_min, hour_max = hour_span
    for event in events:
        event_start_float = _time_to_float(event.begin.time())
        event_end_float = _time_to_float(event.end.time())
        # Calculate positions
        y0 = (
            (total_height - header_height)
            * (hour_max - event_start_float)
            / (hour_max - hour_min)
        )
        y1 = (
            (total_height - header_height)
            * (hour_max - event_end_float)
            / (hour_max - hour_min)
        )
        shape, text = _rectangle_shape_text(event.name, x, y0, width, y1 - y0)
        drawing.add(shape)
        drawing.add(text)


def draw_day_schedule(
    events: Sequence[Event],
    width: int,
    height: int,
    hour_span: Tuple[int, int],
    padding: float = 3.0,
    line_width: float = 0.5,
    time_col_width: float = 8.0,
):
    hour_min, hour_max = hour_span
    drawing = Drawing(width, height)

    # Draw time guides
    for hour in range(hour_min, hour_max + 1):
        y = height * (hour_max - hour) / (hour_max - hour_min)
        line = Line(0, y, width, y, strokeColor=black, strokeWidth=line_width)
        time_label = String(
            x=time_col_width,
            y=y - 6,
            text=f"{hour}:00",
            fontSize=8,
            fillColor=black,
            textAnchor="end",
        )
        drawing.add(line)
        drawing.add(time_label)

    add_day_events(
        drawing=drawing,
        events=events,
        x=time_col_width + padding,
        width=width - time_col_width - padding,
        total_height=height,
        hour_span=hour_span,
    )

    return drawing


def draw_week_schedule(
    events: Sequence[Event],
    start_date: datetime,
    day_width: int,
    height: int,
    w_style,
    hour_span: Tuple[int, int],
    padding: float = 3.0,
    line_width: float = 0.5,
    time_col_width: float = 8.0,
    header_height: float = 10.0,
):
    hour_min, hour_max = hour_span
    drawing = Drawing(day_width * 7 + time_col_width, height)

    # Draw time guides
    for hour in range(hour_min, hour_max + 1):
        y = (height - header_height) * (hour_max - hour) / (hour_max - hour_min)
        line = Line(
            0,
            y,
            time_col_width + padding + 7 * day_width,
            y,
            strokeColor=black,
            strokeWidth=line_width,
        )
        time_label = String(
            x=time_col_width,
            y=y - 6,
            text=f"{hour}:00",
            fontSize=8,
            fillColor=black,
            textAnchor="end",
        )
        drawing.add(line)
        drawing.add(time_label)

    for day, weekday in enumerate(WEEKDAYS):
        day_date = start_date + timedelta(days=day)
        day_events = [
            event for event in events if event.begin.date() == day_date.date()
        ]
        weekday_label = String(
            x=time_col_width + padding + (day + 0.5) * day_width,
            y=height - (header_height / 2),
            text=weekday.upper(),
            **vars(w_style),
            textAnchor="middle",
        )
        add_day_events(
            drawing=drawing,
            events=day_events,
            x=time_col_width + padding + day * day_width,
            header_height=header_height,
            width=day_width,
            total_height=height,
            hour_span=hour_span,
        )
        drawing.add(weekday_label)

    return drawing


def draw_month_schedule(
    year: int,
    month: int,
    events,
    p_style: ParagraphStyle,
    w_style: ParagraphStyle,
    t_style: TableStyle,
    table: TableMeasurements,
):
    # Create month calendar table
    data = [[Paragraph(weekday[:3], w_style) for weekday in WEEKDAYS]]
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
            day_cell = [Paragraph(f"{day}", p_style)]
            day_drawing = fit_rectangles(
                day_events,
                max_events=4,
                width=0.92 * table.colWidth,
                max_height=(
                    table.rowHeight
                    - getattr(p_style, "fontSize", 0)
                    - getattr(p_style, "spaceAfter", 0)
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
        colWidths=[table.colWidth for _ in range(7)],
        rowHeights=[table.headerHeight]
        + [table.rowHeight for _ in range(len(month_calendar))],
    )
    table.setStyle(t_style)
    return table
