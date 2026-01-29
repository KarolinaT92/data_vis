import pandas as pd
import plotly.express as px
from dash import Input, Output, callback

from dashApp.new_Products.constants import ROW_3B_ID, MONTH_LABELS, \
    CATEGORY_DROPDOWN_ID, REGION_DROPDOWN_ID, METRIC_OPTIONS_TOP_HEATMAP_ID, SWITCH_HEATMAP, SELECT_ON_SCATTER_PLOT, \
    HEATMAP_TITLE
from dashApp.new_Products.helper import react_to_category_dropdown
from shared.read_data import df


def normalize_to_list(v):
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return list(v)
    return [v]


def metric_label(metric_value: str) -> str:
    # map dropdown value -> text in title
    if metric_value == "Sales":
        return "Sales"
    if metric_value == "Profit":
        return "Profit"
    if metric_value == "Profit Margin":
        return "Profit Margin"
    return str(metric_value)


@callback(
    Output(ROW_3B_ID, "figure"),
    Output(HEATMAP_TITLE, "children"),
    Input("shipment-year", "value"),
    Input(CATEGORY_DROPDOWN_ID, "value"),
    Input(REGION_DROPDOWN_ID, "value"),
    Input(METRIC_OPTIONS_TOP_HEATMAP_ID, "value"),
    Input(SWITCH_HEATMAP, "on"),
    Input(SELECT_ON_SCATTER_PLOT, "data"),
)
def update_heatmap(year, selected_category, selected_regions, metric, show_text, selected_ids):
    # ---- normalize inputs
    selected_category_list = normalize_to_list(selected_category)
    x = metric_label(metric)

    # ---- build title
    if len(selected_category_list) == 1:
        cat = selected_category_list[0]
        title = f"Monthly {x} made by Sub-Category of {cat}"
    else:
        title = f"Monthly {x} made by Categories"
    dff = react_to_category_dropdown(df, year, selected_category, selected_regions)

    # filter by scatter selection
    if selected_ids:
        dff = dff[dff["Product_Key"].isin(selected_ids)]

    # ---- Dynamic Y-axis dimension
    if selected_category and len(selected_category) == 1:
        y_dim = "Sub-Category"
        y_title = "Sub-Category"
    else:
        y_dim = "Category"
        y_title = "Category"

    # ---- Metric logic (IMPORTANT: keep NaN = blank cells)
    if metric == "Sales":
        pivot = pd.pivot_table(
            dff, values="Sales", index=y_dim, columns="Month",
            aggfunc="sum"  # no fill_value=0
        )
        text_auto = ".0f" if show_text else False

    elif metric == "Profit":
        pivot = pd.pivot_table(
            dff, values="Profit", index=y_dim, columns="Month",
            aggfunc="sum"  # no fill_value=0
        )
        text_auto = ".0f" if show_text else False

    else:  # Profit Margin
        g = (
            dff.groupby([y_dim, "Month"], as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        )
        g["Profit Margin"] = g["Profit"] / g["Sales"].replace(0, pd.NA)
        pivot = g.pivot(index=y_dim, columns="Month", values="Profit Margin")
        text_auto = ".1%" if show_text else False

    # force 12 equal month columns even when filtered
    # (keep missing as NaN so cells stay blank, not colored)
    pivot = pivot.reindex(columns=list(range(1, 13)))

    # optional: use month names as column labels (prevents any spacing/category weirdness)
    pivot.columns = MONTH_LABELS  # now columns are ["Jan","Feb",...,"Dec"]

    fig = px.imshow(
        pivot,
        text_auto=text_auto,
        color_continuous_scale="RdBu",
        aspect="auto",
    )

    #  don't show hover for empty cells
    fig.update_traces(hoverongaps=False)

    fig.update_layout(
        title=None,
        margin=dict(l=60, r=40, t=40, b=80),
        xaxis_title="Month",
        yaxis_title=y_title,
    )

    # keep a stable categorical order so cells never "shift"
    fig.update_xaxes(type="category", categoryorder="array", categoryarray=MONTH_LABELS)

    return fig, title
