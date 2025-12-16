from dash import html, dcc
from dash.dash_table.Format import Format, Scheme
from ..helper.standard_design import DISPLAY_COLS

money = Format(precision=2, scheme=Scheme.fixed, group=True)
percent_0 = Format(precision=0, scheme=Scheme.percentage)  # for Discount only

COLUMNS = [{"name": c, "id": c} for c in DISPLAY_COLS]
for col in COLUMNS:
    if col["id"] in ["Sales", "Profit", "Original Unit Price"]:
        col.update({"type": "numeric", "format": money})
    elif col["id"] == "Discount":
        col.update({"type": "numeric", "format": percent_0})
    elif col["id"] in ["Quantity", "Ship_Duration", "Postal Code"]:
        col.update({"type": "numeric"})

product_table_layout = html.Div(
    className="product-table-container",  # parent div
    children=[


        html.Div(
            id="top10-table-container",  # callback will inject dmc.Table here
            className="product-table-body"
        )
    ]
)
