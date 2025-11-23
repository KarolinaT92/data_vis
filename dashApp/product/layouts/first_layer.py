from dash import html, dcc
from .kpis_layer import kpis_layer

first_layer = html.Div(children=[

    kpis_layer,

    html.Div(children=[
        dcc.Loading(
            dcc.Graph(id='bubble-chart', style={"height": "260px"}, className="graph-shadow"),
            type="circle"
        ),
        html.Div(
            dcc.Loading(dcc.Graph(id='scatter-plot', style={"height": "260px"}), type="circle"),
            className="graph-shadow"
        )
    ], className="first-layer-p2")

], className="first-layer")
