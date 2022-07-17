from bokeh.colors import RGB
from bokeh.models import Span


def return_one():
    return 1


def add_line_two_sd(p, location):
    first_line = Span(
        location=location,
        dimension="height",
        line_color=RGB(255, 140, 0, 0.2),
        line_dash="dashed",
        line_width=3,
    )
    p.add_layout(first_line)
    return p


def add_line_three_sd(p, location):
    first_line = Span(
        location=location,
        dimension="height",
        line_color=RGB(255, 69, 0),
        line_dash="dashed",
        line_width=3,
    )
    p.add_layout(first_line)
    return p
