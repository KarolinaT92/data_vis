from dash import html, dcc
import dash_daq as daq

PLOTLY_DOWNLOAD_ONLY_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "toggleSpikelines",
    ],
}

def segment_shipping_drilldown_layout():
    return html.Div(
        children=[
            # ============================
            # MAIN CHART
            # ============================
            dcc.Graph(
                id="shipment-segment-shipmode",
                config=PLOTLY_DOWNLOAD_ONLY_CONFIG, 
            ),

            html.Hr(),

            # ============================
            # CONTROLS
            # ============================
            html.Div(
                className="flex items-center gap-6 mb-3",
                children=[
                    html.Div(
                        className="flex items-center gap-2",
                        children=[
                            html.Label("Top N Sub-Categories:", className="font-medium"),
                            dcc.Dropdown(
                                id="shipment-topn-dropdown",
                                options=[
                                    {"label": "Top 3", "value": 3},
                                    {"label": "Top 5", "value": 5},
                                    {"label": "Top 10", "value": 10},
                                ],
                                value=5,
                                clearable=False,
                                className="w-[120px]",
                            ),
                        ],
                    ),

                    html.Div(
                        className="flex items-center gap-2",
                        children=[
                            html.Span("Display values", className="text-sm"),
                            daq.BooleanSwitch(
                                id="shipment-drilldown-show-values",
                                on=False,   
                                size=24,
                            ),
                        ],
                    ),
                ],
            ),

            # ============================
            # DRILL-DOWN CHART
            # ============================
            dcc.Graph(
                id="shipment-drilldown-chart",
                config=PLOTLY_DOWNLOAD_ONLY_CONFIG, 
            ),
        ]
    )
