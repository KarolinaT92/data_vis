from dash import html, dcc
from .filter import filter_layout
from .first_layer import first_layer
from .second_layer import second_layer
from .third_layer import third_layer

layout = html.Div(
    [
        dcc.Store(id='filtered-year-data'),
        dcc.Store(id='aggregated-category-data'),
        filter_layout,
        html.Div(
            [
                first_layer,
                second_layer,
                third_layer
            ],
            className="right-panel"
        )
    ],
    className="container"
)
