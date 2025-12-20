from dash import callback, Output, Input
from shared.read_data import df
import plotly.express as px
from pathlib import Path
import pandas as pd
import numpy as np
from us import states   # 2-letter code


# ---- Load city coordinates (from shared/city_coordinates.csv) ----
BASE_DIR = Path(__file__).resolve().parents[3]
CITY_COORDS_PATH = BASE_DIR / "shared" / "city_coordinates.csv"
city_coords = pd.read_csv(CITY_COORDS_PATH)[["City", "State", "lat", "lon"]]


def _filter_customers(year, segments, regions):
    """Apply the standard filters for the customer page."""
    dff = df.copy()

    if isinstance(segments, str):
        segments = [segments]
    if isinstance(regions, str):
        regions = [regions]

    if year is not None:
        dff = dff[dff["Year"] == year]
    if segments:
        dff = dff[dff["Segment"].isin(segments)]
    if regions:
        dff = dff[dff["Region"].isin(regions)]

    return dff


@callback(
    Output("customer-map", "figure"),
    Input("customer-year-dropdown", "value"),
    Input("customer-segment-dropdown", "value"),
    Input("customer-region-dropdown", "value"),
    Input("customer-min-slider", "value"),
)
def update_customer_map(year, segments, regions, min_count):
    dff = _filter_customers(year, segments, regions)

    if dff.empty:
        return px.scatter_geo(title="No data for selected filters.")

    # ---------- CITY-LEVEL METRICS ----------
    city_metrics = (
        dff.groupby(["City", "State"])
        .agg(
            **{
                "Customer Count": ("Customer Name", "nunique"),
                "Total Sales": ("Sales", "sum"),
                "Total Profit": ("Profit", "sum"),
            }
        )
        .reset_index()
    )

    city_metrics = city_metrics.merge(city_coords, on=["City", "State"], how="inner")

    # ---------- STATE HEATMAP (customer count) ----------
    state_counts = (
        city_metrics.groupby("State", as_index=False)["Customer Count"]
        .sum()
    )
    state_counts["StateCode"] = state_counts["State"].apply(
        lambda x: states.lookup(x).abbr if states.lookup(x) else None
    )
    state_counts = state_counts.dropna(subset=["StateCode"])

    fig = px.choropleth(
        state_counts,
        locations="StateCode",
        locationmode="USA-states",
        color="Customer Count",
        scope="usa",
        color_continuous_scale="Blues",  
        title="Customer distribution by state and city",
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="State Customers",
            x=-0.06,   
            xpad=10,
        )
    )

    # ---------- CITY DOTS (profit heatmap) ----------
    if min_count is None:
        min_count = 1
    min_count = max(1, int(min_count))

    city_for_dots = city_metrics[city_metrics["Customer Count"] >= min_count].copy()

    if not city_for_dots.empty:
        profit_min = city_for_dots["Total Profit"].min()
        profit_max = city_for_dots["Total Profit"].max()
        profit_abs = max(abs(profit_min), abs(profit_max)) or 1

        city_for_dots["hover_text"] = (
            city_for_dots["City"]
            + ", "
            + city_for_dots["State"]
            + "<br>Customers: "
            + city_for_dots["Customer Count"].astype(int).astype(str)
            + "<br>Sales: $"
            + city_for_dots["Total Sales"].round(0).astype(int).astype(str)
            + "<br>Profit: $"
            + city_for_dots["Total Profit"].round(0).astype(int).astype(str)
        )

        sizes = 4 + 1.4 * np.sqrt(city_for_dots["Customer Count"])

        fig.add_scattergeo(
            lat=city_for_dots["lat"],
            lon=city_for_dots["lon"],
            text=city_for_dots["hover_text"],
            marker=dict(
                size=sizes,
                color=city_for_dots["Total Profit"],    
                colorscale="RdYlGn",                    
                cmin=-profit_abs,
                cmax=profit_abs,
                colorbar=dict(
                    title="City Profit",
                    x=1.05,          
                ),
                line=dict(width=0.4, color="#333"),
                opacity=0.85,
            ),
            hoverinfo="text",
            name="City (profit)",
        )

    fig.update_geos(
        projection_type="albers usa",
        showland=True,
        landcolor="#F0F0F0",
        subunitcolor="#C0C0C0",
        showsubunits=True,
        showcountries=False,
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        dragmode="pan",
    )

    return fig
