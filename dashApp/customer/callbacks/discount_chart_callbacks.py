from dash import callback, Output, Input
import plotly.express as px
import numpy as np
from shared.read_data import df


def _filter_basic(year, segments, regions):
    dff = df.copy()
    if isinstance(segments, str): segments = [segments]
    if isinstance(regions, str): regions = [regions]
    if year: dff = dff[dff["Year"] == year]
    if segments: dff = dff[dff["Segment"].isin(segments)]
    if regions: dff = dff[dff["Region"].isin(regions)]
    return dff


@callback(
    Output("discount-graph", "figure"),
    Input("customer-year-dropdown", "value"),
    Input("customer-segment-dropdown", "value"),
    Input("customer-region-dropdown", "value"),
    Input("discount-view", "value"),
    Input("bubble-size", "value"),
    Input("bubble-label-thresh", "value"),
)
def update_discount_chart(year, segments, regions, discount_view,
                          bubble_size_range, label_threshold):

    dff = _filter_basic(year, segments, regions)
    if dff.empty:
        return px.scatter(title="No data.")

    # Violin plot
    if discount_view == "violin":
        return px.violin(
            dff, x="Segment", y="Discount",
            points="all", box=True,
            hover_data=["Customer Name", "Order ID"],
            title="Discount Distribution by Segment",
        )

    # Bubble view
    tmp = dff.copy()
    tmp["DiscountRounded"] = tmp["Discount"].round(2)

    agg = tmp.groupby(["Segment", "DiscountRounded"], as_index=False).size()
    agg.rename(columns={"size": "Count"}, inplace=True)

    bubble_min, bubble_max = bubble_size_range or [14, 50]
    agg["Label"] = np.where(
        agg["Count"] >= (label_threshold or 0),
        agg["Count"].astype(str), ""
    )

    fig = px.scatter(
        agg, x="DiscountRounded", y="Segment",
        size="Count", size_max=bubble_max,
        text="Label", hover_data=["Count"],
        title="Discount by Segment — Bubble View",
    )
    fig.update_traces(textposition="top center")
    return fig
