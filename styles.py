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
    fontSize=10,
    leading=12,
    alignment=1,  # Centered
    fontName="Helvetica",
    spaceAfter=6,
)

################################################
#                DAY TABLE                     #
################################################

DAY_colWidth = 450
DAY_timeWidth = 50
DAY_rowHeight = 36
DAY_headerHeight = 24
DAY_lineWidth = 0.5

day_table = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), DAY_lineWidth, colors.lightgrey),
    ]
)

################################################
#               WEEK TABLE                     #
################################################

WEEK_colWidth = 60
WEEK_timeWidth = 50
WEEK_rowHeight = 36
WEEK_headerHeight = 24
WEEK_lineWidth = 0.5

week_table = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), WEEK_lineWidth, colors.lightgrey),
    ]
)

################################################
#              MONTH TABLE                     #
################################################

MONTH_colWidth = 80
MONTH_rowHeight = 60
MONTH_headerHeight = 24

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
