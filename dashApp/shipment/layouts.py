from dash import html, dcc
import dash_daq as daq
import plotly.graph_objects as go


# ====================================================
# EMPTY FIGURE 
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
# GRAPH CONFIG
# ====================================================

GRAPH_CONFIG_PNG_ONLY = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": False,
    "modeBarButtons": [["toImage"]],
}


# ====================================================
# CARDS
# ====================================================

def speed_share_card():
    return html.Div(
        [
            html.H3(
                "Delivery Time & Shipping Preference",
                className="text-base font-semibold mb-2",
            ),
            dcc.Graph(
                id="shipment-speed-share-combined",
                figure=blank_figure(),
                config=GRAPH_CONFIG_PNG_ONLY,
                className="flex-1 min-h-0",
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )


def shipmode_driver_card():
    return html.Div(
        [
            html.H3(
                "Shipping Distribution by Segment / Region",
                className="text-base font-semibold mb-2",
            ),

            html.Div(
                className="controls-row",
                children=[

                    html.Div(
                        className="flex items-center gap-3",
                        children=[
                            html.Span("Segment", className="toggle-label"),

                            dcc.Checklist(
                                id="shipment-driver-dimension",
                                options=[{"label": "", "value": "Region"}],
                                value=[],
                                className="toggle-switch",
                            ),

                            html.Span("Region", className="toggle-label"),
                        ],
                    ),

                    html.Div(
                        className="flex items-center gap-2",
                        children=[
                            html.Span(
                                "Normalize by %",
                                className="toggle-label",
                            ),
                            dcc.Checklist(
                                id="shipment-normalize-toggle",
                                options=[{"label": "", "value": "pct"}],
                                value=[],
                            ),
                        ],
                    ),
                ],
            ),

            dcc.Graph(
                id="shipment-shipmode-driver",
                figure=blank_figure(),
                className="flex-1 min-h-0",
                config=GRAPH_CONFIG_PNG_ONLY,
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )


def year_distribution_card():
    return html.Div(
        [
            html.H3(
                "Shipping Mode Trends Over Time",
                className="text-base font-semibold mb-2",
            ),
            dcc.Graph(
                id="shipment-year-distribution",
                figure=blank_figure(),
                className="flex-1 min-h-0",
                config=GRAPH_CONFIG_PNG_ONLY,
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )


def topn_subcategories_card():
    return html.Div(
        [
            html.H3(
                "Top 5 Shipped Sub-Categories of Products",
                className="text-base font-semibold mb-2",
            ),

            html.Div(
                className="controls-row",
                children=[

                    dcc.Dropdown(
                        id="shipment-drilldown-metric",
                        options=[
                            {"label": "Number of orders", "value": "count"},
                            {"label": "Share of Orders (%)", "value": "share"},
                        ],
                        value="count",
                        clearable=False,
                        searchable=False,
                        className="metric-dropdown",
                    ),

                    html.Div(
                        className="show-values-switch",
                        children=[
                            html.Span("display values", className="text-sm"),
                            daq.BooleanSwitch(
                                id="shipment-drilldown-show-values",
                                on=True,
                                size=22,
                                color="#3b82f6",
                            ),
                        ],
                    ),
                ],
            ),

            dcc.Graph(
                id="shipment-topn-subcategories",
                figure=blank_figure(),
                className="flex-1 min-h-0",
                config=GRAPH_CONFIG_PNG_ONLY,
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )
