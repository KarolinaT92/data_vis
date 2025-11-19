from dash import html, dcc
from .kpis_layer import kpis_layer

first_layer = html.Div(children=[
    kpis_layer
], className="first-layer")




