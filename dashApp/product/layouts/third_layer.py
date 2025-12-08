from audioop import reverse

from dash import html, dcc
from numpy.random import chisquare

from .table_layout import product_table_layout
from ..helper.standard_design import THIRD_LAYER_HEIGHT

bar_heatmap_layout = html.Div(children=[
    html.Div(
        dcc.Slider(
            min=5,
            max=20,
            step=5,  # only 5, 10, 15, 20
            marks={i: str(i) for i in range(5, 21, 5)},  # 5,10,15,20
            value=10,
            updatemode='drag',
            vertical=True,
            verticalHeight=190,
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
                    min=5,
                    max=20,
                    step=0.1,
                    marks={i: str(i) for i in range(5, 21, 5)},  # 5,10,15,20
                    value=10,
                    updatemode='drag',
                    vertical=True,
                    verticalHeight=190,
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
