from dash import Input, Output, callback
from shared.read_data import df

from .figures import (
    build_speed_share_figure,
    build_shipmode_driver_figure,
    build_year_distribution_figure,
    build_topn_subcategories_figure,
)

# =====================================================
# KPIs
# =====================================================

@callback(
    Output("kpi-total-orders", "children"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_kpi_total_orders(year, segments, regions):
    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    return f"{len(dff):,}"


@callback(
    Output("kpi-average-delivery", "children"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_kpi_average_delivery(year, segments, regions):
    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    if dff.empty:
        return "—"

    avg_days = dff["Ship_Duration"].mean()
    
    return f"{avg_days:.1f} days"


@callback(
    Output("kpi-top-ship-mode", "children"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_kpi_top_ship_mode(year, segments, regions):
    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    if dff.empty:
        return "—"

    mode_share = dff["Ship Mode"].value_counts(normalize=True)
    top_mode = mode_share.index[0]
    share = mode_share.iloc[0]

    return f"{top_mode} ({share:.0%})"



# =====================================================
# ROW 2A — SPEED & SHARE 
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
# ROW 2B — SHIP MODE DISTRIBUTION 
# =====================================================

@callback(
    Output("shipment-shipmode-driver", "figure"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
    Input("shipment-driver-dimension", "value"),
    Input("shipment-normalize-toggle", "value"),
)
def update_shipmode_driver(year, segments, regions, dimension_toggle, normalize):

    dimension = "Region" if "Region" in dimension_toggle else "Segment"

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
        normalize=True,
    )


# =====================================================
# ROW 3B — TOP SUB-CATEGORIES
# =====================================================

@callback(
    Output("shipment-topn-subcategories", "figure"),
    Input("shipment-shipmode-driver", "clickData"),
    Input("shipment-drilldown-metric", "value"),
    Input("shipment-drilldown-show-values", "on"),
    Input("shipment-year", "value"),
    Input("shipment-segment", "value"),
    Input("shipment-region", "value"),
)
def update_topn_subcategories(
    clickData,
    metric,
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
            metric=metric,
            show_values=show_values,
        )

    ship_mode_index = clickData["points"][0]["curveNumber"]

    from .figures import SHIP_MODE_ORDER
    ship_mode = SHIP_MODE_ORDER[ship_mode_index]

    dff = df[
        (df["Year"] == year)
        & (df["Segment"].isin(segments))
        & (df["Region"].isin(regions))
    ]

    segment = None
    x_value = clickData["points"][0]["x"]
    if x_value in df["Segment"].unique():
        segment = x_value

    return build_topn_subcategories_figure(
        dff,
        segment=segment,
        ship_mode=ship_mode,
        metric=metric,
        show_values=show_values,
    )
