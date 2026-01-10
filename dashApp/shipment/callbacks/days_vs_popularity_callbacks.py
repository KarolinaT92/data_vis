from dash import callback, Output, Input
import plotly.express as px

from shared.read_data import df

SHIP_MODE_ORDER = [
    "Same Day",
    "First Class",
    "Second Class",
    "Standard Class",
]

SHIP_MODE_COLORS = {
    "Same Day": "#e8b7c8",       
    "First Class": "#a9c3df",    
    "Second Class": "#c3b6db",    
    "Standard Class": "#9fd3c7",  
}


@callback(
    Output("shipment-boxplot-duration-by-mode", "figure"),
    Output("shipment-bar-share-by-mode", "figure"),
    Input("shipment-year-radio", "value"),
)
def update_days_vs_popularity(year):

    dff = df[df["Year"] == year]

    medians = (
        dff.groupby("Ship Mode")["Ship_Duration"]
        .median()
        .round(1)
        .to_dict()
    )

    # --------------------------------------------
    # Chart 1 — Box plot 
    # --------------------------------------------
    fig_box = px.box(
        dff,
        x="Ship Mode",
        y="Ship_Duration",
        color="Ship Mode",
        category_orders={"Ship Mode": SHIP_MODE_ORDER},
        color_discrete_map=SHIP_MODE_COLORS,
        points=False,            
        template="plotly",
        labels={"Ship_Duration": "Delivery Time (days)"},
    )

    fig_box.update_traces(
        hoveron="points",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Median delivery time: %{customdata} days"
            "<extra></extra>"
        ),
        customdata=[
            medians.get(mode, None)
            for mode in dff["Ship Mode"]
        ],
    )

    fig_box.update_layout(
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        showlegend=False,
    )

    # --------------------------------------------
    # Chart 2 — Single-row stacked bar 
    # --------------------------------------------
    share = (
        dff.groupby("Ship Mode")
        .size()
        .reset_index(name="count")
    )

    share["share"] = share["count"] / share["count"].sum()
    share["All Orders"] = "All Orders"

    fig_share = px.bar(
        share,
        x="share",
        y="All Orders",
        orientation="h",
        color="Ship Mode",
        category_orders={"Ship Mode": SHIP_MODE_ORDER},
        color_discrete_map=SHIP_MODE_COLORS,
        text=share["share"].map(lambda x: f"{x:.0%}"),
        template="plotly",
        labels={"share": "Share of Orders"},
    )

    fig_share.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        hoverinfo="skip",
    )

    fig_share.update_layout(
        plot_bgcolor="#f5f5f5",
        paper_bgcolor="#f5f5f5",
        legend_title_text="",
        hovermode=False,
        xaxis_range=[0, 1],
        xaxis_tickformat=".0%",
        yaxis_visible=False,
        yaxis_showticklabels=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig_box, fig_share
