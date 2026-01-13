from dash import html, dcc

PLOTLY_DOWNLOAD_ONLY_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "select2d", "lasso2d",
        "zoomIn2d", "zoomOut2d", "autoScale2d",
        "resetScale2d", "hoverClosestCartesian",
        "hoverCompareCartesian", "toggleSpikelines",
    ],
}

profit_per_order_layout = html.Div(
    children=[
        html.H4("Segment Profit"),

        html.Div(
            style={
                "display": "flex",
                "gap": "24px",
                "flexWrap": "wrap",
                "marginBottom": "12px",
            },
            children=[
                html.Div(
                    children=[
                        dcc.Checklist(
                            id="profit-show-yearly",
                            options=[
                                {
                                    "label": " Show cumulative yearly comparison",
                                    "value": "yearly",
                                },
                            ],
                            value=[],
                            inline=True,
                            labelStyle={"fontWeight": "600"},
                        ),
                    ]
                ),
            ],
        ),

        dcc.Graph(
            id="profit-per-order-graph",
            config=PLOTLY_DOWNLOAD_ONLY_CONFIG,
            style={"flex": 1},
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100%",
    },
)
