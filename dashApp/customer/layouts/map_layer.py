from dash import html, dcc

map_layout = html.Div(
    children=[
        html.H4("Distribution map of customers"),

        html.Div(
            style={
                "display": "flex",
                "gap": "12px",
                "marginBottom": "8px",
            },
            children=[
                html.Div(
                    children=[
                        html.Label(
                            "Minimum customers per city",
                            style={"fontWeight": 600}
                        ),
                        dcc.Slider(
                            id="customer-min-slider",
                            min=1,
                            max=50,
                            step=1,
                            value=15,
                            marks={i: str(i) for i in [1, 5, 10, 20, 30, 40, 50]},
                            tooltip={"placement": "bottom"},
                        ),
                    ]
                ),
            ],
        ),

        dcc.Graph(
            id="customer-map",
            style={"flex": 1},
            config={
                "scrollZoom": True,
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": ["lasso2d", "select2d", "pan2d"],
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100%",
    },
)
