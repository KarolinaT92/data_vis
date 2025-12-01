from dash import html, dcc
from .filter import filter_layout
from .first_layer import first_layer
from .second_layer import second_layer
from .third_layer import third_layer

test_layout = html.Div(
    [
        dcc.Store(id="selected-indices", data=[]),  # keep track of clicked points
        dcc.Graph(
            id="scatter-graph",
            style={"width": "600px", "height": "400px"},
        ),
    ]
)

layout = html.Div(
    [
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
