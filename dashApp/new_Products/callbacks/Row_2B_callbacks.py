from dash import Input, Output, callback
from dashApp.new_Products.constants import CATEGORY_DROPDOWN_ID, ROW_2B_ID
from shared.read_data import df
import plotly.graph_objects as go

# ROW 2B — Top Products
TOP_N = 10


@callback(
    Output(ROW_2B_ID, "figure"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),

)
def update_top_products(year, selected_categories):
    year = int(year)

    # If nothing selected → treat as all
    if not selected_categories:
        selected_categories = sorted(df["Category"].dropna().unique())

    dff = df[
        (df["Year"] == year) &
        (df["Category"].isin(selected_categories))
        ].copy()

    # Group by UNIQUE product key
    top = (
        dff.groupby(["Product_Key", "Product Name"], as_index=False)
        .agg(Profit=("Profit", "sum"))
        .sort_values("Profit", ascending=False)
        .head(TOP_N)
    )

    if top.empty:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Bar(
                x=top["Profit"],
                y=top["Product Name"],  # display name
                orientation="h",
                hovertext=top["Product_Key"],
                hovertemplate="<b>%{y}</b><br>Profit: %{x:,.2f}<br>Key: %{hovertext}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=f"Top {TOP_N} Profitable Products ({year})",
        xaxis_title="Total Profit",
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=10),
        height=400,
    )

    # Highest bar on top
    fig.update_yaxes(categoryorder="total ascending")

    return fig
