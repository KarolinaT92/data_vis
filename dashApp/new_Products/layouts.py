from dash import html, dcc

from .constants import ROW_2A_ID, ROW_2B_ID, ROW_3A_ID, ROW_3B_ID, VIEW_MODE_DROPDOWN_ID, SELECT_ON_SCATTER_PLOT, \
    CLEAR_SELECTION_BUTTON_ID
from .figures import empty_figure
from ..template.plot_height import PLOT_HEIGHT


def row_2A():
    return html.Div(
        [
            html.H3(
                "Sales, Profits and Quantity",
                className="text-base font-semibold mb-2",
            ),
            dcc.Store(id=SELECT_ON_SCATTER_PLOT, data=[]),
            html.Div(
                className="relative z-50 mb-2",  # key
                children=[
                    html.Div(
                        className="flex items-center gap-1",
                        children=[
                            html.Label("View Mode", className="filter-label whitespace-nowrap"),
                            dcc.Dropdown(
                                id=VIEW_MODE_DROPDOWN_ID,
                                options=[
                                    {"label": "Category Summary", "value": "summary"},
                                    {"label": "Detailed Data Points", "value": "detail"},
                                ],
                                value="summary",
                                clearable=False,
                                className="w-44 text-sm",
                            ),
                        ],
                    )
                ],
            ),
            html.Button(
                "Clear selection",
                id=CLEAR_SELECTION_BUTTON_ID,
                className="text-sm px-3 py-1 rounded-md border",
            ),

            dcc.Loading(
                dcc.Graph(
                    id=ROW_2A_ID,
                    figure=empty_figure(),
                    className="flex-1 min-h-0",
                    style=PLOT_HEIGHT,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": [
                            # zoom / pan
                            "zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                            # hover / compare
                            "hoverClosestCartesian", "hoverCompareCartesian",
                        ],
                    },
                ),
                type="circle",

            )
        ],
        className="flex flex-col h-full min-h-0",
    )


def row_2B():
    return html.Div(
        [
            html.H3(
                "Top 10 profitable Products",
                className="text-base font-semibold mb-2",
            ),
            dcc.Loading(
                dcc.Graph(
                    id=ROW_2B_ID,
                    className="flex-1 min-h-0",
                    style=PLOT_HEIGHT,
                ),
                type="circle",
            )

        ],
        className="flex flex-col h-full min-h-0",
    )


def row_3A():
    return html.Div(
        [
            html.H3(
                "Monthly Sales and Profits",
                className="text-base font-semibold mb-2",
            ),
            dcc.Loading(
                dcc.Graph(
                    id=ROW_3A_ID,
                    className="flex-1 min-h-0",
                    style=PLOT_HEIGHT
                ),
                type="circle"
            )

        ],
        className="flex flex-col h-full min-h-0",
    )


def row_3B():
    return html.Div(
        [
            html.H3(
                "Monthly Profits made by Category",
                className="text-base font-semibold mb-2",
            ),
            dcc.Loading(dcc.Graph(
                id=ROW_3B_ID,
                className="flex-1 min-h-0",
                style=PLOT_HEIGHT
            ), type="circle"),

        ],
        className="flex flex-col h-full min-h-0",
    )
