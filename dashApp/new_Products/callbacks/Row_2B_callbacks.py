import plotly.graph_objects as go
from dash import Input, Output, callback
from dashApp.new_Products.constants import CATEGORY_DROPDOWN_ID, ROW_2B_ID, REGION_DROPDOWN_ID
from dashApp.new_Products.helper import react_to_category_dropdown
from shared.read_data import df

# ROW 2B — Top Products
TOP_N = 10


def truncate_name(name, max_len=30):
    return name if len(name) <= max_len else name[:max_len] + "…"


@callback(
    Output(ROW_2B_ID, "figure"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
)
def update_top_products(year, selected_categories, selected_regions):
    dff = react_to_category_dropdown(df, year, selected_categories, selected_regions)
    # Group by UNIQUE product key
    top = (
        dff.groupby(["Product_Key", "Product Name"], as_index=False)
        .agg(Profit=("Profit", "sum"))
        .sort_values("Profit", ascending=False)
        .head(TOP_N)
    )

    top["Product Name Short"] = top["Product Name"].apply(
        truncate_name
    )
    if top.empty:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Bar(
                x=top["Profit"],
                y=top["Product Name Short"],
                orientation="h",
                customdata=top["Product Name"],
                hovertemplate="<b>%{customdata}</b><br>Profit: %{x:,.0f} $<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Profit ($)",
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=10),
        height=400,
    )

    # Highest bar on top
    fig.update_yaxes(categoryorder="total ascending")

    return fig
