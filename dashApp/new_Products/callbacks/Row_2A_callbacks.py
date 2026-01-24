from dash import Input, Output, State, callback, ctx
import plotly.express as px
from dashApp.new_Products.constants import SELECT_ON_SCATTER_PLOT, ROW_2A_ID, CATEGORY_DROPDOWN_ID, \
    VIEW_MODE_DROPDOWN_ID, CLEAR_SELECTION_BUTTON_ID
from shared.read_data import df


#  select points on scatter plot
@callback(
    Output(SELECT_ON_SCATTER_PLOT, "data"),
    Input(ROW_2A_ID, "selectedData"),
    Input(CLEAR_SELECTION_BUTTON_ID, "n_clicks"),
    State(SELECT_ON_SCATTER_PLOT, "data"),
    prevent_initial_call=True,
)
def sync_selected_points(selectedData, clear_clicks, current_ids):
    trigger = ctx.triggered_id

    # Clear selection ONLY by button
    if trigger == CLEAR_SELECTION_BUTTON_ID:
        return []

    # Update selection from lasso/box
    if selectedData and selectedData.get("points"):
        selected_ids = []
        for p in selectedData["points"]:
            cd = p.get("customdata")
            if cd:
                selected_ids.append(cd[0])

        # de-duplicate while preserving order
        seen = set()
        selected_ids = [x for x in selected_ids if not (x in seen or seen.add(x))]
        return selected_ids

    # If user unselects / nothing selected => clear
    return []

# ROW 2A — Bubble Chart

@callback(
    Output(ROW_2A_ID, "figure"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(VIEW_MODE_DROPDOWN_ID, "value"),
    Input(CLEAR_SELECTION_BUTTON_ID, "n_clicks"),   # ✅ add clear button
)
def update_bubble_chart(year, selected_category, view_mode, clear_clicks):
    year = int(year)

    if not selected_category:
        selected_category = sorted(df["Category"].dropna().unique())

    dff = df[
        (df["Year"] == year) &
        (df["Category"].isin(selected_category))
    ].copy()

    # ---- VIEW MODE: Detailed (all data points)
    if view_mode == "detail":
        fig = px.scatter(
            dff,
            x="Profit",
            y="Sales",
            custom_data=["Product_Key"],
            size="Quantity",
            size_max=18,
            color="Category" if len(selected_category) > 1 else None,
            labels={"Profit": "Profit ($)", "Sales": "Sales ($)"},
        )

        fig.update_layout(
            title=None,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
            margin=dict(l=10, r=10, t=50, b=10),
            xaxis_title="Profit ($)",
            yaxis_title="Sales ($)",
            hovermode=False,
            dragmode="select",
        )

        # ✅ If clear button triggered, remove selection overlay + selected state
        if ctx.triggered_id == CLEAR_SELECTION_BUTTON_ID:
            fig.update_layout(selections=[])  # clears drawn selection box/polygon
            fig.update_traces(selectedpoints=None)

        return fig

    # ---- VIEW MODE: Summary
    category_summary = (
        dff.groupby("Category", as_index=False)
           .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
    )

    fig = px.scatter(
        category_summary,
        x="Profit",
        y="Sales",
        size="Quantity",
        color="Category",
        text="Category",
        size_max=60,
        labels={"Profit": "Profit ($)", "Sales": "Sales ($)", "Quantity": "Total Quantity"},
    )

    fig.update_traces(textposition="middle center", textfont=dict(size=12, color="white"))

    fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Profit ($)",
        yaxis_title="Sales ($)",
        selections=[],  # (harmless here, but keeps state clean if user switches modes)
    )

    return fig
