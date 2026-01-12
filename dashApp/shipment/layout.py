from dash import html, dcc
from .layouts import (
    days_vs_popularity_layout,
    shipmode_by_region_layout,
    segment_shipping_drilldown_layout,
    shipment_filter_layout,
)

PLOTLY_CONFIG = {
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


top_grid = html.Div(
    [
        # --------------------------------------------
        # SHIPPING SPEED VS POPULARITY
        # --------------------------------------------
        html.Div(
            days_vs_popularity_layout(),
            className="border-2 rounded p-4 bg-white xl:col-span-2",
        ),

        # --------------------------------------------
        # SHIP MODE DISTRIBUTION
        # --------------------------------------------
        html.Div(
            [
                html.H2("Ship Mode Distribution"),

                dcc.Checklist(
                    id="shipment-normalize-toggle",
                    options=[
                        {"label": "Normalize by percentage", "value": "pct"}
                    ],
                    value=["pct"],
                    labelClassName="ml-2 cursor-pointer",
                    inputClassName="mr-1",
                ),

                # MAIN STACKED BAR
                dcc.Graph(
                    id="shipment-region-shipmode-stacked",
                    config=PLOTLY_CONFIG,
                    style={"height": "425px"},
                ),

                # TREND CHART
                dcc.Graph(
                    id="shipment-shipmode-trend",
                    config=PLOTLY_CONFIG,
                    style={"height": "450px", "marginTop": "25px"},
                ),
            ],
            className="border-2 rounded p-4 bg-white xl:col-span-2",
        ),
    ],
    className="grid grid-cols-1 xl:grid-cols-4 gap-4",
)


bottom_section = html.Div(
    [
        html.H2("Ship Mode by Customer Segment"),
        html.P(
            "Click on a customer segment to explore "
            "which top product sub-categories are shipped."
        ),
        segment_shipping_drilldown_layout(),
    ],
    className="border-2 rounded p-4 bg-white mt-4",
)


layout = html.Div(
    [
        shipment_filter_layout,
        html.Div([top_grid, bottom_section], className="right-panel"),
    ],
    className="container",
    style={"backgroundColor": "#f5f5f5", "minHeight": "100vh"},
)
