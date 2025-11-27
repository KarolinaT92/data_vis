from pydoc import classname

from dash import html, dcc
from .kpis_layer import kpis_layer

first_layer = html.Div(children=[
    html.Div(children=[kpis_layer,
                       html.Div(
                           dcc.Loading(
                               dcc.Graph(id='pie-chart', style={"height": "120px"}),
                               type="circle"
                           )
                       )], className="first-layer-p1"),

    html.Div(children=[
        dcc.Loading(
            dcc.Graph(id='bubble-chart', style={"height": "205px"}, className="graph-shadow"),
            type="circle"
        ),
        html.Div(
            dcc.Loading(dcc.Graph(id='scatter-plot', style={"height": "205px"}, className="graph-shadow"),
                        type="circle"),

        )
    ], className="first-layer-p2")

], className="first-layer")
