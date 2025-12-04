from audioop import reverse

from dash import html, dcc
from numpy.random import chisquare

from .table_layout import product_table_layout
from ..helper.standard_design import THIRD_LAYER_HEIGHT

bar_heatmap_layout = html.Div(children=[
    html.Div(
        dcc.Slider(
            -10, 10, None,
            value=5,
            vertical=True,
            verticalHeight=190,
            className="custom-slider",
            marks={
                -10: {'label': 'Worst 10', 'style': {'color': '#dc3545'}},  # Optional styling for negative
                -5: {'label': '-5'},
                # 0 is intentionally omitted here
                5: {'label': '5'},
                10: {'label': 'Best 10', 'style': {'color': '#28a745'}}  # Optional styling for positive
            },
            id='product-3th-layer-p1-slider'
        ),
        className="slider-column-container"
    ),
    html.Div(
        dcc.Loading(dcc.Graph(id='product-3th-layer-p1', style=THIRD_LAYER_HEIGHT),
                    type="circle"),
        className="graph-column-container"
    ),

], className="flex-row-container"),

third_layer = html.Div(
    children=[
        html.Div(children=[
            html.Div(
                dcc.Slider(
                    -10, 10, None,
                    value=5,
                    vertical=True,
                    verticalHeight=190,
                    className="custom-slider",
                    marks={
                        -10: {'label': 'Worst 10', 'style': {'color': '#dc3545'}},  # Optional styling for negative
                        -5: {'label': '-5'},
                        # 0 is intentionally omitted here
                        5: {'label': '5'},
                        10: {'label': 'Best 10', 'style': {'color': '#28a745'}}  # Optional styling for positive
                    },
                    id='product-3th-layer-p1-slider'
                ),
                className="slider-column-container"
            ),
            html.Div(
                dcc.Loading(dcc.Graph(id='product-3th-layer-p1', style=THIRD_LAYER_HEIGHT),
                            type="circle"),
                className="graph-column-container"
            ),

        ], className="third-layer-p1 flex-row-container"),

        html.Div(
            product_table_layout,
            className="third-layer-p2"
        )

    ], className="third-layer")
