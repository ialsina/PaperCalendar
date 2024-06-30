from reportlab.graphics.shapes import Drawing, Circle, String, Rect
from reportlab.lib.colors import Color, black, white
from typing import Optional

import styles

BUBBLE_RADIUS = 5
FONT_SIZE = 4
FILL_COLOR = white


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


def fit_rectangles(events, width: int, max_height, padding: int = 2, max_events: int = 4):
    drawing = Drawing(width, max_height)
    events = events[:max_events]
    height = (max_height - padding * (len(events) - 1)) / max(len(events), 1)
    for index, event in enumerate(events):
        y = (height + padding) * index
        shape, text = _rectangle_shape_text(event, 0, y, width, height)
        drawing.add(shape)
        drawing.add(text)
        # elements.append(
        #     rectangle(event, width, height, x_position, y_position)
        # )
    return drawing
