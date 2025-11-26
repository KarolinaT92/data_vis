from dash import html, dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme
import dash_mantine_components as dmc

DISPLAY_COLS = [
    'Order Date', 'Discount', 'Quantity', 'Sales', 'Profit', 'Profit Margin (%)',
    'Original Unit Price', 'Ship Date', 'Ship Mode', 'Ship_Duration', 'Customer Name',
    'Segment', 'City', 'State', 'Postal Code', 'Region'
]

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
            id="product-table-controls",
            className="product-table-controls",
            children=[
                html.Div(
                    className="relative mb-6",
                    children=[
                        dcc.Input(
                            id="cannon-search-input",
                            type="text",
                            value="",
                            placeholder="Search Product Name...",
                            className="w-full pl-3 pr-10 py-2 border rounded focus:outline-none",
                            debounce=True,
                        ),
                        html.Span(
                            "🔍",
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 cursor-pointer",
                        ),
                    ],
                ),
            ]
        ),

        html.Div(
            id="top10-table-container",  # callback will inject dmc.Table here
            className="product-table-body"
        )
    ]
)
