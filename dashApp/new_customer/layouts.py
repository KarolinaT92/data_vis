from dash import html, dcc
import dash_daq as daq
import plotly.graph_objects as go


# ====================================================
# BLANK FIGURE
# ====================================================

def blank_figure():
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


# ====================================================
# CONFIGS
# ====================================================

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


# ====================================================
# CUSTOMERS – MAIN PANEL
# ====================================================

customers_main_panel = html.Div(
    id="customers-main-panel",
    className="flex flex-col h-full min-h-0",
    children=[

        # -------- CHART VIEW --------
        html.Div(
            id="customers-chart-view",
            className="flex flex-col h-full min-h-0",
            children=[

                # ---- TITLE ----
                html.H4(
                    "Most Profitable Customers",
                    className="font-semibold mb-1",
                ),

                # ---- CONTROLS + HINT ROW ----
                html.Div(
                    className="flex items-center justify-between mb-2",
                    children=[

                        # LEFT: controls
                        html.Div(
                            className="flex items-center gap-2",
                            children=[
                                html.Span(
                                    "Show top",
                                    className="text-base text-slate-700",
                                ),

                                html.Span(
                                    id="topn-value",
                                    className="text-base font-semibold text-slate-800 w-5 text-center",
                                ),

                                html.Span(
                                    "customers",
                                    className="text-base text-slate-700",
                                ),

                                dcc.Slider(
                                    id="topn-slider",
                                    min=0,
                                    max=2,
                                    step=1,
                                    value=1,
                                    marks={
                                        0: "3",
                                        1: "5",
                                        2: "10",
                                    },
                                    included=False,
                                    className="w-28",
                                    tooltip={"always_visible": False},
                                ),
                                
                            ],
                        ),

                        # RIGHT: hint
                        html.Span(
                            "Click a customer bar to view their orders",
                            className="text-xs text-slate-400",
                        ),
                    ],
                ),

                # ---- CHART ----
                dcc.Graph(
                    id="profit-graph",
                    figure=blank_figure(),
                    className="flex-1 min-h-0",
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
        html.H4(
            "Customer Distribution and Profit",
            className="font-semibold mb-1",
        ),

        html.Div(
            className="flex items-center gap-2",
            children=[
                html.Span(
                    "Show cities with at least:",
                    className="text-base text-slate-700",
                ),

                html.Div(
                    className="min-customers-group",
                    children=[
                        html.Button("1", id="min-btn-1", n_clicks=0),
                        html.Button("5", id="min-btn-5", n_clicks=0),
                        html.Button("10", id="min-btn-10", n_clicks=0),
                        html.Button("25", id="min-btn-25", n_clicks=1),
                        html.Button("50", id="min-btn-50", n_clicks=0),
                    ],
                ),

                html.Span(
                    "customers",
                    className="text-base text-slate-700",
                ),
            ],
        ),

        dcc.Store(id="customer-min-store", data=25),

        dcc.Graph(
            id="customer-map",
            figure=blank_figure(),
            className="w-full h-[360px]",
            config=MAP_CONFIG,
        ),
    ],
)


# ====================================================
# SALES MICROBANDS
# ====================================================

sales_microbands_chart_layout = html.Div(
    className="flex flex-col h-full",
    children=[
        html.H4(
            "Sales by Region and Segment",
            className="font-semibold mb-2",
        ),
        dcc.Graph(
            id="combined-sales-chart",
            figure=blank_figure(),
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
        html.H4(
            "Profit per Order by Segment",
            className="font-semibold mb-2",
        ),

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
            figure=blank_figure(),
            className="flex-1 min-h-0",
            config=PLOTLY_CONFIG,
        ),
    ],
)
