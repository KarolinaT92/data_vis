from audioop import reverse

from dash import html, dcc
from .table_layout import product_table_layout

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
                dcc.Loading(dcc.Graph(id='product-3th-layer-p1', style={"height": "335px", "width": "100%"}),
                            type="circle"),
                className="graph-column-container"
            ),

        ], className="third-layer-p1 flex-row-container"),

        html.Div(
            product_table_layout,
            className="third-layer-p2"
        )

    ], className="third-layer")
