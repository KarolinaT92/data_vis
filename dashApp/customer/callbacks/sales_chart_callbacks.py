from dash import callback, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from shared.read_data import df


# ============================================================
# MAIN CALLBACK — SALES + HEATMAP (INLINE VERSION)
# ============================================================
@callback(
    Output("combined-sales-chart", "figure"),
    Output("profit-heatmap-chart", "figure"),
    Input("customer-year-dropdown", "value"),
    Input("customer-segment-dropdown", "value"),
    Input("customer-region-dropdown", "value"),
)
def update_sales_and_heatmap(year, segments, regions):

    # -----------------------------
    # Filter dataset
    # -----------------------------
    dff = df.copy()
    if isinstance(segments, str): segments = [segments]
    if isinstance(regions, str): regions = [regions]

    if year:
        dff = dff[dff["Year"] == year]
    if segments:
        dff = dff[dff["Segment"].isin(segments)]
    if regions:
        dff = dff[dff["Region"].isin(regions)]

    # -----------------------------
    # BUILD SALES MICROBANDS FIGURE
    # -----------------------------
    agg = (
        dff.groupby(["Region", "Segment", "Category"], as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )

    # Empty fallback
    if agg.empty:
        sales_fig = px.scatter(title="No data.")
        sales_fig.update_layout(autosize=True, height=None)
    else:
        category_colors = {
            "Furniture": "rgba(78,121,167,0.75)",
            "Technology": "rgba(242,142,43,0.75)",
            "Office Supplies": "rgba(90,161,80,0.75)",
        }

        offsets = {"Consumer": 0.25, "Corporate": 0.00, "Home Office": -0.25}

        sales_fig = go.Figure()
        regions_sorted = sorted(agg["Region"].unique())

        # WHICH SEGMENTS ARE ACTUALLY PRESENT?
        segments_present = agg["Segment"].unique()

        # BARS + HOVER
        for region in regions_sorted:
            reg_data = agg[agg["Region"] == region]
            base_y = regions_sorted.index(region)

            for seg, off in offsets.items():
                if seg not in segments_present:
                    continue

                subset = reg_data[reg_data["Segment"] == seg]
                if subset.empty:
                    continue

                y_level = base_y + off

                for _, row in subset.iterrows():
                    sales_fig.add_trace(go.Bar(
                        x=[row["Sales"]],
                        y=[y_level],
                        width=0.22,
                        orientation="h",
                        marker_color=category_colors[row["Category"]],
                        showlegend=False,
                        customdata=[[region, seg, row["Category"], row["Profit"]]],
                        hovertemplate="<b>%{customdata[0]}</b><br>"
                                      "Segment: %{customdata[1]}<br>"
                                      "Category: %{customdata[2]}<br>"
                                      "Sales: %{x:,.0f}<br>"
                                      "Profit: %{customdata[3]:,.0f}<extra></extra>",
                    ))

        # ----------------------------------------
        # SEGMENT LABEL FIX — ONLY LABEL VALID SEGMENTS
        # ----------------------------------------
        for region in regions_sorted:
            reg_data = agg[agg["Region"] == region]
            base_y = regions_sorted.index(region)

            for seg, off in offsets.items():

                # label only segments that exist for this region
                if seg not in reg_data["Segment"].values:
                    continue

                sales_fig.add_annotation(
                    xref="paper",
                    yref="y",
                    x=1.02,
                    y=base_y + off,
                    text=seg,
                    showarrow=False,
                    font=dict(size=12, color="#333"),
                )

        # AXES
        sales_fig.update_yaxes(
            tickvals=list(range(len(regions_sorted))),
            ticktext=regions_sorted,
            title="Region",
            automargin=True,
        )
        sales_fig.update_xaxes(title="Sales", automargin=True)

        # LAYOUT
        sales_fig.update_layout(
            barmode="stack",
            autosize=True,
            height=None,
            plot_bgcolor="white",
            margin=dict(l=50, r=80, t=70, b=40),
            transition=None,
        )

    # -----------------------------
    # BUILD PROFIT HEATMAP (INLINE)
    # -----------------------------
    heat = (
        dff.groupby(["Region", "Segment"])["Profit"]
           .sum()
           .reset_index()
    )

    if heat.empty:
        heatmap_fig = go.Figure()
        heatmap_fig.add_annotation(
            x=0.5, y=0.5,
            text="No data for selection",
            showarrow=False,
            font=dict(size=16)
        )
        heatmap_fig.update_layout(autosize=True, height=None)
    else:
        pivot = heat.pivot(index="Region", columns="Segment", values="Profit").fillna(0)

        heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale=[
                    [0.0, "rgb(220,50,50)"],
                    [0.5, "rgb(255,235,140)"],
                    [1.0, "rgb(50,160,55)"],
                ],
                hovertemplate="Region: %{y}<br>"
                              "Segment: %{x}<br>"
                              "Profit: %{z:,.0f}<extra></extra>",
                colorbar=dict(title="Profit", thickness=12),
            )
        )

        heatmap_fig.update_layout(
            autosize=True,
            height=None,
            title=None,
            xaxis_title="Segment",
            yaxis_title="Region",
            margin=dict(l=10, r=10, t=10, b=10),
            transition=None,
        )

        heatmap_fig.update_xaxes(automargin=True)
        heatmap_fig.update_yaxes(automargin=True)

    return sales_fig, heatmap_fig


# ============================================================
# PROFIT DETAIL CALLBACK (INLINE)
# ============================================================
@callback(
    Output("profit-detail-chart", "figure"),
    Input("combined-sales-chart", "clickData"),
    State("customer-year-dropdown", "value"),
    State("customer-segment-dropdown", "value"),
    State("customer-region-dropdown", "value"),
)
def update_profit_detail(clickData, year, segments, regions):

    if not clickData:
        fig = px.scatter(title="Click a bar to see details")
        fig.update_layout(autosize=True, height=None)
        return fig

    region, segment, category, _profit = clickData["points"][0]["customdata"]

    dff = df.copy()
    if isinstance(segments, str): segments = [segments]
    if isinstance(regions, str): regions = [regions]

    dff = dff[
        (dff["Year"] == year) &
        (dff["Segment"].isin(segments)) &
        (dff["Region"].isin(regions))
    ]

    selected = dff[
        (dff["Region"] == region) &
        (dff["Segment"] == segment) &
        (dff["Category"] == category)
    ]

    if selected.empty:
        fig = px.scatter(title="No detail data available")
        fig.update_layout(autosize=True, height=None)
        return fig

    detail = selected.groupby("Sub-Category", as_index=False)["Profit"].sum()
    detail["Color"] = np.where(
        detail["Profit"] >= 0,
        "rgba(50,160,55,0.9)",
        "rgba(200,50,50,0.9)"
    )

    fig = go.Figure(go.Bar(
        x=detail["Profit"],
        y=detail["Sub-Category"],
        orientation="h",
        marker_color=detail["Color"],
        hovertemplate="<b>%{y}</b><br>Profit: %{x:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        autosize=True,
        height=None,
        xaxis_title="Profit",
        yaxis_title="Sub-Category",
        margin=dict(l=40, r=40, t=40, b=20),
        transition=None,
    )

    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)

    return fig
