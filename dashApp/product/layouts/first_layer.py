import dash_daq as daq
from dash import html, dcc
from ..helper.standard_design import FIRST_LAYER_HEIGHT

bubble_chart_layout = html.Div(
    children=[

        # CENTERED OVERLAY
        html.Div(
            children=[
                html.P("details", className="mr-1 text-sm"),
                daq.BooleanSwitch(
                    id="bubble-hover-details-switch",
                    on=False,
                    size=25
                ),
            ],
            className=(
                "absolute top-1 right-1 "
                "flex items-center px-3 py-1 rounded shadow z-10 bg-gray-100"
            )
        ),
        dcc.Store(id='selected-category-store', data=[]),
        dcc.Loading(
            dcc.Graph(id='bubble-chart',
                      style=FIRST_LAYER_HEIGHT,
                      className="graph-shadow",
                      config={"displayModeBar": False}),
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
                html.P("details", className="mr-2 text-sm"),
                daq.BooleanSwitch(
                    id="hover-details-switch",
                    on=False,
                    size=25
                ),
            ],
            className=(
                "absolute top-2 left-1/2 -translate-x-1/2 "
                "flex items-center bg-white/80 px-3 py-1 rounded shadow z-10 bg-gray-100"
            )
        ),

        # GRAPH
        dcc.Loading(
            dcc.Graph(
                id='scatter-plot',
                style=FIRST_LAYER_HEIGHT,
                className="graph-shadow",
                config={
                    "displayModeBar": True,
                    "modeBarButtonsToRemove": [
                        # zoom / pan
                        "zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                        # hover / compare
                        "hoverClosestCartesian", "hoverCompareCartesian",
                        # misc UI
                        "toggleSpikelines", "toImage",
                    ],
                },
            ),
            type="circle"
        )
    ],
    className="relative"
)
