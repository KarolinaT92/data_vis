from dash import Input, Output, callback
from shared.read_data import df

from .figures import (
    build_speed_share_figure,
    build_shipmode_driver_figure,
    build_year_distribution_figure,
    build_topn_subcategories_figure,
)


# =====================================================
# ROW 2A — SPEED & SHARE (COMBINED SUBPLOT)
# =====================================================

@callback(
    Output("shipment-speed-share-combined", "figure"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_speed_share(year, segments, regions):
    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    return build_speed_share_figure(dff)


# =====================================================
# ROW 2B — SHIP MODE DISTRIBUTION (DRIVER)
# =====================================================

@callback(
    Output("shipment-shipmode-driver", "figure"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
    Input("shipment-driver-dimension", "value"), 
    Input("shipment-normalize-toggle", "value"),
)
def update_shipmode_driver(year, segments, regions, dimension, normalize):
    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    return build_shipmode_driver_figure(
        dff,
        dimension=dimension,
        normalize="pct" in normalize,
    )


# =====================================================
# ROW 3A — YEAR DISTRIBUTION
# =====================================================

@callback(
    Output("shipment-year-distribution", "figure"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_year_distribution(segments, regions):
    dff = df[
        (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    return build_year_distribution_figure(
        dff,
        normalize=False,
    )


# =====================================================
# ROW 3B — TOP N SUB-CATEGORIES (DRILLDOWN)
# =====================================================

@callback(
    Output("shipment-topn-subcategories", "figure"),
    Input("shipment-shipmode-driver", "clickData"),
    Input("shipment-topn", "value"),
    Input("shipment-drilldown-show-values", "value"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_topn_subcategories(
    clickData,
    top_n,
    show_values,
    year,
    segments,
    regions,
):
    if not clickData:
        return build_topn_subcategories_figure(
            df,
            segment=None,
            ship_mode=None,
            top_n=top_n,
            show_values="on" in show_values,
        )


    dimension_value = clickData["points"][0]["x"]
    ship_mode_index = clickData["points"][0]["curveNumber"]

    from .figures import SHIP_MODE_ORDER
    ship_mode = SHIP_MODE_ORDER[ship_mode_index]

    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    segment = None
    if clickData["points"][0]["x"] in df["Segment"].unique():
        segment = clickData["points"][0]["x"]

    return build_topn_subcategories_figure(
        dff,
        segment=segment,
        ship_mode=ship_mode,
        top_n=top_n,
        show_values="on" in show_values,
    )
