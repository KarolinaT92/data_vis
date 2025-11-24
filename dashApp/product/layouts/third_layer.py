from dash import html, dcc
from .table_layout import product_table_layout

third_layer = html.Div(
    children=[
        html.Div(
            dcc.Loading(dcc.Graph(id='product-3th-layer-p1'), type="circle",
                        ), className="flex-[0.65]  min-w-0 overflow-hidden border-1 rounded-[5px] shadow-xl"),
        html.Div(
            product_table_layout,
            className="flex-[0.35]  min-w-0 overflow-hidden border-1 rounded-[5px] shadow-xl"
        )

    ], className="third-layer")
