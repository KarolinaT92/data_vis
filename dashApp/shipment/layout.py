from dash import html, dcc

from .layouts import (
    days_vs_popularity_layout,
    shipmode_by_region_layout,
    segment_shipping_drilldown_layout,
    shipment_filter_layout,
)

# =====================================================
# TOP GRID — OVERVIEW CHARTS
# =====================================================
top_grid = html.Div(
    [

        # ============================================
        # SHIPPING SPEED VS POPULARITY
        # ============================================
        html.Div(
            children=[
                days_vs_popularity_layout(),
            ],
            className="border-2 rounded p-4 xl:col-span-2",
            style={"backgroundColor": "white"},
        ),

        # ============================================
        # SHIPPING MODE DISTRIBUTION
        # ============================================
        html.Div(
            children=[
                html.H2("Ship Mode Distribution by Region"),

                # ---- Checkbox toggle ----
                html.Div(
                    className="flex items-center gap-2 mb-3",
                    children=[
                        dcc.Checklist(
                            id="shipment-show-trend-checkbox",
                            options=[
                                {
                                    "label": "Show trend over years",
                                    "value": "show",
                                }
                            ],
                            value=[],
                        )
                    ],
                ),

                # ---- Main region chart ----
                html.Div(
                    shipmode_by_region_layout(),
                    style={"height": "420px"},
                ),

                # ---- Trend chart (hidden by default) ----
                html.Div(
                    dcc.Graph(id="shipment-shipmode-trend"),
                    id="shipment-trend-wrapper",
                    style={
                        "height": "300px",
                        "marginTop": "16px",
                        "display": "none",
                    },
                ),
            ],
            className="border-2 rounded p-4 xl:col-span-2",
            style={"backgroundColor": "white"},
        ),
    ],
    className="grid grid-cols-1 xl:grid-cols-4 gap-4",
)

# =====================================================
# BOTTOM SECTION — DRILLDOWN
# =====================================================
bottom_section = html.Div(
    children=[
        html.H2("Ship Mode by Customer Segment"),
        html.P(
            "Click on a customer segment to explore "
            "which top product sub-categories are shipped."
        ),
        segment_shipping_drilldown_layout(),
    ],
    className="border-2 rounded p-4 mt-4",
    style={"backgroundColor": "white"},
)

# =====================================================
# FINAL PAGE WRAPPER
# =====================================================
layout = html.Div(
    [
        # LEFT — FILTER PANEL
        shipment_filter_layout,

        # RIGHT — CONTENT
        html.Div(
            [
                top_grid,
                bottom_section,
            ],
            className="right-panel",
            style={
                "backgroundColor": "#f5f5f5",
                "minHeight": "100vh",
                "padding": "16px",
            },
        ),
    ],
    style={
        "display": "flex",
        "backgroundColor": "#f5f5f5",
        "minHeight": "100vh",
    },
)
