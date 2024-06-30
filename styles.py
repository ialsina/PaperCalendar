from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import TableStyle

title = ParagraphStyle(
    name="Title", fontSize=18, leading=22, alignment=1, spaceAfter=12  # Centered
)
minimalist = ParagraphStyle(
    name="Minimalist", fontSize=8, leading=10, alignment=0, spaceAfter=6  # Left-aligned
)
weekday = ParagraphStyle(
    name="Weekday",
    fontSize=8,
    leading=12,
    alignment=1,  # centered
    fontName="Helvetica",
    spaceAfter=6,
)

@dataclass(frozen=True)
class TableMeasurements:
    # pylint: disable=C0103
    colWidth: float
    timeWidth: float
    rowHeight: float
    headerHeight: float
    lineWidth: float


################################################
#                DAY TABLE                     #
################################################

day = TableMeasurements(
    colWidth = 450,
    timeWidth = 50,
    rowHeight = 36,
    headerHeight = 24,
    lineWidth = 0.5,
)

day_table = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), day.lineWidth, colors.lightgrey),
    ]
)

################################################
#               WEEK TABLE                     #
################################################

week = TableMeasurements(
    colWidth = 60,
    timeWidth = 50,
    rowHeight = 36,
    headerHeight = 24,
    lineWidth = 0.5,
)

week_table = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), week.lineWidth, colors.lightgrey),
    ]
)

################################################
#              MONTH TABLE                     #
################################################

month = TableMeasurements(
    colWidth = 80,
    rowHeight = 60,
    headerHeight = 24,
    timeWidth=None,
    lineWidth=0.5,
)

month_table = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        # ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]
)
