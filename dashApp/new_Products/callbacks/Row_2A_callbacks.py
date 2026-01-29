from dash import Input, Output, State, callback, ctx
import plotly.express as px

from dashApp.new_Products.colors import FURNITURE_COLOR, OFFICE_COLOR, TECHNOLOGY_COLOR
from dashApp.new_Products.constants import SELECT_ON_SCATTER_PLOT, ROW_2A_ID, CATEGORY_DROPDOWN_ID, \
    VIEW_MODE_DROPDOWN_ID, CLEAR_SELECTION_BUTTON_ID, REGION_DROPDOWN_ID
from dashApp.new_Products.helper import react_to_category_dropdown
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


@callback(
    Output(CLEAR_SELECTION_BUTTON_ID, "style"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
    prevent_initial_call=True,
)
def toggle_reset_button(selected_ids):
    if selected_ids:
        return {
            "display": "inline-flex",
            "whiteSpace": "nowrap",  # prevent wrapping
            "padding": "6px 12px",  # vertical + horizontal padding
            "width": "fit-content",  # auto width based on text
            "color": "white",
            "backgroundColor": "#2563eb",
        }

    return {"display": "none"}


# ROW 2A — Bubble Chart

CATEGORY_COLORS = {
    "Furniture": FURNITURE_COLOR,
    "Office Supplies": OFFICE_COLOR,
    "Technology": TECHNOLOGY_COLOR,
}


@callback(
    Output(ROW_2A_ID, "figure"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(VIEW_MODE_DROPDOWN_ID, "value"),
    Input(CLEAR_SELECTION_BUTTON_ID, "n_clicks"),
    Input(REGION_DROPDOWN_ID, "value"),
)
def update_bubble_chart(year, selected_category, view_mode, clear_clicks, selected_region):
    dff = react_to_category_dropdown(df, year, selected_category, selected_region)

    # ---- VIEW MODE: Detailed (all data points)
    if view_mode == "detail":
        fig = px.scatter(
            dff,
            x="Profit",
            y="Sales",
            custom_data=["Product_Key"],
            # size="Quantity",
            # size_max=18,
            color="Category",  # keep consistent colors
            color_discrete_map=CATEGORY_COLORS,  # fixed mapping
            # color="Category" if len(selected_category) > 1 else None,
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
            margin=dict(l=10, r=10, t=30, b=100),
            xaxis_title="Profit ($)",
            yaxis_title="Sales ($)",
            hovermode=False,
            dragmode="select",
        )

        # If clear button triggered, remove selection overlay + selected state
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
        color_discrete_map=CATEGORY_COLORS,
        text="Category",
        size_max=60,
        labels={"Profit": "Profit ($)", "Sales": "Sales ($)", "Quantity": "Total Quantity"},
    )

    fig.update_traces(textposition="middle center", textfont=dict(size=12))

    fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=100),
        xaxis_title="Profit ($)",
        yaxis_title="Sales ($)",
        selections=[],
    )

    return fig
