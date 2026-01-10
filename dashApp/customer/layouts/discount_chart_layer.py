from dash import html, dcc

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


discount_layout = html.Div(
    children=[
        html.H4("Discount by Segment"),

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "marginBottom": "10px",
            },
            children=[
                html.Div(
                    children=[
                        html.Label("View", style={"fontWeight": 600}),
                        dcc.RadioItems(
                            id="discount-view",
                            options=[
                                {"label": " Violin", "value": "violin"},
                                {"label": " Bubble", "value": "bubble"},
                            ],
                            value="violin",
                            inline=True,
                        ),
                    ]
                ),

                html.Div(
                    children=[
                        html.Label("Bubble size (px)", style={"fontWeight": 600}),
                        dcc.RangeSlider(
                            id="bubble-size",
                            min=8,
                            max=80,
                            value=[14, 50],
                            marks={i: str(i) for i in [8, 20, 40, 60, 80]},
                            tooltip={"placement": "bottom"},
                        ),
                    ],
                ),

                html.Div(
                    children=[
                        html.Label("Label threshold", style={"fontWeight": 600}),
                        dcc.Input(
                            id="bubble-label-thresh",
                            type="number",
                            value=70,
                            style={"width": "110px","textAlign": "center"},
                        ),
                    ]
                ),
            ],
        ),


        dcc.Graph(
            id="discount-graph", config=PLOTLY_DOWNLOAD_ONLY_CONFIG,
            style={"flex": 1},
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100%",       
    },
)
