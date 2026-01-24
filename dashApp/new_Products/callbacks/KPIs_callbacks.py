from dash import Input, Output, callback

from shared.read_data import df


# ROW 1 — KPI UPDATES

@callback(
    Output('kpi-total-sales', 'children'),
    Output('kpi-profit', 'children'),
    Output('kpi-orders', 'children'),
    Input("shipment-year", "value"),
    # Input("shipment-segment", "value"),
    # Input("shipment-region", "value"),
)
def update_kpis(year):
    df_selected_year = df[
        (df["Year"] == year)
        # & (df["Segment"].isin(segments))
        # & (df["Region"].isin(regions))
    ]
    sales_of_year = df_selected_year["Sales"].sum()
    sales = f"${sales_of_year:,.0f}"
    profit_of_year = df_selected_year["Profit"].sum()

    profit = f"${profit_of_year:,.0f}"
    orders_of_year = df_selected_year["Quantity"].sum()
    orders = f"{orders_of_year:,}"
    return sales, profit, orders