from dash import html, dcc
from shared.read_data import df

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


customers_chart_layout = html.Div(
    children=[

        html.H4("Top most profitable customers"),

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
                            id="profit-view",
                            options=[
                                {"label": " Bar", "value": "bar"},
                                {"label": " Lollipop", "value": "lollipop"},
                            ],
                            value="bar",
                            inline=True,
                        ),
                    ]
                ),

                html.Div(
                    style={"flex": "1", "minWidth": "240px"},
                    children=[
                        html.Label("Top customers", style={"fontWeight": 600}),
                        dcc.Slider(
                            id="topn-slider",
                            min=5,
                            max=20,
                            step=1,
                            value=10,
                            marks={i: str(i) for i in [5, 10, 15, 20]},
                            tooltip={"placement": "bottom"},
                        ),
                    ],
                ),
            ],
        ),

        dcc.Graph(id="profit-graph", config=PLOTLY_DOWNLOAD_ONLY_CONFIG, style={"height": "420px"}),
    ],
)

CUSTOMER_OPTIONS = [
    {"label": c, "value": c}
    for c in sorted(df["Customer Name"].unique())
]

customers_table_layout = html.Div(
    children=[

        html.H4("Customer Order Detail"),

        html.Div(
            style={"marginBottom": "10px"},
            children=[
                html.Label("Select customer", style={"fontWeight": 600}),
                dcc.Dropdown(
                    id="customer-search-box",
                    options=CUSTOMER_OPTIONS,
                    placeholder="Start typing customer name...",
                    clearable=True,
                    searchable=True,
                    style={"width": "100%"},
                ),
            ],
        ),

        html.Div(
            id="customer-order-table",
            style={
                "maxHeight": "420px",
                "overflowY": "auto",
                "border": "1px solid #ddd",
                "padding": "5px",
                "background": "white",
            },
        ),
    ]
)
