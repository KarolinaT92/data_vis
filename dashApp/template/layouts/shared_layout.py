from dash import html, dcc

from dashApp.template.layouts.KPI_template import kpi_layout
from dashApp.template.layouts.filter_options import filter_layout

CARD= "bg-gray-50 p-4 rounded-lg shadow-md"
CARD_CENTER = "p-4 rounded-lg shadow-md flex items-center justify-center"


filter_layout = html.Div(
    className="col-span-3 lg:col-span-2 bg-gray-100 p-4 rounded-lg",
    children=filter_layout.children,
)

visualization_layout = html.Div(
    className="col-span-9 lg:col-span-10 bg-white p-6 rounded-lg",
    children=[
        # Container grid
        html.Div(
            className="grid grid-cols-1 gap-6",

            children=[
                # -------- Row 1 (3 columns) --------
                html.Div(
                    className="grid grid-cols-1 md:grid-cols-3 gap-16",
                    children=[
                        html.Div(kpi_layout, className=CARD_CENTER),
                        html.Div(kpi_layout, className=CARD_CENTER),
                        html.Div(kpi_layout, className=CARD_CENTER),
                    ],
                ),

                # -------- Row 2 (2 columns) --------
                html.Div(
                    className="grid grid-cols-1 md:grid-cols-2 gap-3",
                    children=[
                        html.Div("Box 4", className=CARD),
                        html.Div("Box 5", className=CARD),
                    ],
                ),

                # -------- Row 3 (2 columns) --------
                html.Div(
                    className="grid grid-cols-1 md:grid-cols-2 gap-3",
                    children=[
                        html.Div("Box 6", className=CARD),
                        html.Div("Box 7", className=CARD),
                    ],
                ),
            ],
        ),
    ],
)


shared_layout = html.Div(
    className="grid grid-cols-12 gap-1 container", # the filter takes 3 cols, the main content takes 9 cols
    children=[
        # Filter column (small)
        filter_layout,
        # Main content column (large)
        visualization_layout
    ]
)
