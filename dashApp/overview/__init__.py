import dash
from .layout import layout

dash.register_page(
    __name__,
    path="/",
    name="Overview",
    title="Overview Dashboard",
    order=1,
    layout=layout,
)
