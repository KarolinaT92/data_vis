from dash import html, dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme

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
    className="mx-auto px-3 max-w-[1100px]",
    children=[
        dcc.Store(id="cannon-store", data=[]),

        # Search bar
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

        # Table with loading
        dcc.Loading(
            id="loading-cannon-table",
            type="circle",
            children=[
                DataTable(
                    id="cannon-table",
                    columns=COLUMNS,
                    data=[],

                    page_action="none",
                    fixed_rows={"headers": True},
                    sort_action="native",
                    filter_action="native",

                    style_header={"fontWeight": "600"},
                    style_data={"whiteSpace": "nowrap"},
                    style_cell={
                        "minWidth": "110px",
                        "width": "110px",
                        "maxWidth": "320px",
                        "padding": "14px 10px",
                        "fontSize": "14px",
                        "border": "1px solid #eee",
                    },
                    style_cell_conditional=[
                        {"if": {"column_id": "Profit Margin (%)"}, "minWidth": "160px"},
                        {"if": {"column_id": "Original Unit Price"}, "minWidth": "160px"},
                        {"if": {"column_id": "Customer Name"}, "minWidth": "180px"},
                        {"if": {"column_id": "Ship Mode"}, "minWidth": "140px"},
                    ],
                    style_table={
                        "minWidth": "720px",
                        "overflowX": "auto",
                        "height": "500px",
                        "overflowY": "auto",
                    },
                )
            ]
        ),
    ]
)
