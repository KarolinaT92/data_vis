import dash_daq as daq
from dash import html, dcc
from .kpis_layer import kpis_layer
from ..helper.standard_design import FIRST_LAYER_HEIGHT

bubble_chart_layout = html.Div(
    children=[

        # CENTERED OVERLAY
        html.Div(
            children=[
                html.P("details on hover", className="mr-2 text-sm"),
                daq.BooleanSwitch(
                    id="bubble-hover-details-switch",
                    on=False,
                    size=25
                ),
            ],
            className=(
                "absolute top-2 left-1/2 -translate-x-1/2 "
                "flex items-center px-3 py-1 rounded shadow z-10"
            )
        ),
        dcc.Store(id='selected-category-store', data=[]),
        dcc.Loading(
            dcc.Graph(id='bubble-chart',
                      style=FIRST_LAYER_HEIGHT,
                      className="graph-shadow"),
            type="circle"
        ),
    ],
    className="relative"
)

scatter_plot_layout = html.Div(
    children=[

        # CENTERED OVERLAY
        html.Div(
            children=[
                html.P("details on hover", className="mr-2 text-sm"),
                daq.BooleanSwitch(
                    id="hover-details-switch",
                    on=False,
                    size=25
                ),
            ],
            className=(
                "absolute top-2 left-1/2 -translate-x-1/2 "
                "flex items-center bg-white/80 px-3 py-1 rounded shadow z-10"
            )
        ),

        # GRAPH
        dcc.Loading(
            dcc.Graph(
                id='scatter-plot',
                style=FIRST_LAYER_HEIGHT,
                className="graph-shadow"
            ),
            type="circle"
        )
    ],
    className="relative"
)

# first_layer = html.Div(children=[
#     html.Div(children=[kpis_layer,
#                        html.Div(
#                            dcc.Loading(
#                                dcc.Graph(id='pie-chart', style=FIRST_LAYER_HEIGHT),
#                                type="circle"
#                            )
#                        )]),
#
#     html.Div(children=[
#
#         dcc.Store(id='selected-category-store', data=[]),
#         dcc.Loading(
#             dcc.Graph(id='bubble-chart', style=FIRST_LAYER_HEIGHT, className="graph-shadow"),
#             type="circle"
#         ),
#         # dcc.Store(id="selected-indices-scatter-plot", data=[]),
#
#     ], className="first-layer-p2")
#
# ], className="first-layer")
