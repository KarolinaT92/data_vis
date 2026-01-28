from dash import html, dcc
import dash_daq as daq

PLOTLY_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom2d", "pan2d", "select2d", "lasso2d",
        "zoomIn2d", "zoomOut2d", "autoScale2d",
        "resetScale2d",
    ],
}

MAP_CONFIG = {
    **PLOTLY_CONFIG,
    "scrollZoom": True,
}

customers_main_panel = html.Div(
    id="customers-main-panel",
    className="flex flex-col h-full min-h-0",
    children=[

        # -------- CHART VIEW --------
        html.Div(
            id="customers-chart-view",
            className="flex flex-col h-full min-h-0",
            children=[
                html.H4(
                    "Most Profitable Customers",
                    className="font-semibold mb-1",
                ),

                html.Div(
                    [
                        html.Span(
                            "Show top",
                        ),
                        html.Span(
                            id="topn-value",
                            className="ml-2 text-sm font-semibold text-slate-700",
                        ),
                        html.Span(
                            " customers",
                        ),
                    ],
                    className="text-sm text-slate-600 text-right",
                ),
                dcc.Slider(
                    id="topn-slider",
                    min=5,
                    max=20,
                    step=1,
                    value=10,
                    marks={5: "5", 10: "10", 15: "15", 20: "20"},
                    className="mb-2",
                ),

                html.Div(
                    "Click a customer bar to view their orders",
                    className="text-xs text-slate-500 mb-2 text-center",
                ),

                dcc.Graph(
                    id="profit-graph",
                    className="flex-1 min-h-0",
                    style={"height": "100%"},
                    config=PLOTLY_CONFIG,
                ),
            ],
        ),

        # -------- TABLE VIEW --------
        html.Div(
            id="customers-table-view",
            className="flex flex-col h-full min-h-0",
            style={"display": "none"},
            children=[
                html.Button(
                    "← Back to chart",
                    id="customers-back-btn",
                    className="text-blue-600 text-sm mb-2 self-start",
                ),
                html.Div(
                    id="customers-table-content",
                    className="flex-1 overflow-auto",
                ),
            ],
        ),
    ],
)


# ====================================================
# MAP
# ====================================================

map_layout = html.Div(
    className="flex flex-col h-full",
    children=[
        html.H4("Customer Distribution and Profit", className="font-semibold mb-1"),

        dcc.Graph(
            id="customer-map",
            className="flex-1 min-h-0",
            config=MAP_CONFIG,
        ),

    html.Div(
        [
            html.Div(
                [
                    html.Span(
                        "Show cities with at least ",
                        className="text-xs text-slate-500",
                    ),
                    html.Span(
                        id="customer-min-value",
                        className="text-xs font-semibold text-slate-700 mx-1",
                    ),
                    html.Span(
                        " customers",
                        className="text-xs text-slate-500",
                    ),
                ],
                className="text-center mb-1",
            ),
            dcc.Slider(
                id="customer-min-slider",
                min=1,
                max=50,
                step=1,
                value=25,
                marks={1: "1", 25: "25", 50: "50"},
                tooltip={"placement": "bottom", "always_visible": False},
            ),
        ],
        className="mt-2",
    ),

        html.Div(
            [
                html.Span("Map key:", className="font-semibold text-xs text-slate-600 mr-1"),
                html.Span("State color = customer concentration, dot size = number of customers", className="text-xs text-slate-500 mr-3"),
            ],
            className="text-center mb-1",
        ),
    ],
)

# ====================================================
# SALES MICROBANDS
# ====================================================

sales_microbands_chart_layout = html.Div(
    className="flex flex-col h-full",
    children=[
        html.H4("Sales by Region and Segment", className="font-semibold mb-2"),
        dcc.Graph(
            id="combined-sales-chart",
            className="flex-1 min-h-0",
            config=PLOTLY_CONFIG,
        ),
    ],
)

# ====================================================
# PROFIT PER ORDER
# ====================================================


profit_per_order_layout = html.Div(
    className="flex flex-col h-full",
    children=[
        html.H4("Profit per Order by Segment", className="font-semibold mb-2"),

        html.Div(
            className="controls-row",
            children=[
                dcc.Checklist(
                    id="profit-show-yearly",
                    options=[{"label": " Yearly comparison", "value": "yearly"}],
                    value=[],  
                ),

                html.Div(
                    className="show-values-switch",
                    children=[
                        html.Span("display values", className="text-sm"),
                        daq.BooleanSwitch(
                            id="profit-show-values",
                            on=True,         
                            size=22,
                            color="#3b82f6",
                        ),
                    ],
                ),
            ],
        ),

        dcc.Graph(
            id="profit-per-order-graph",
            className="flex-1 min-h-0",
            config=PLOTLY_CONFIG,
        ),
    ],
)
