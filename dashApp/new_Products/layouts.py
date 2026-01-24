from dash import html, dcc

from .constants import row_2A_id, row_2B_id, row_3A_id, row_3B_id
from .figures import empty_figure

def row_2A():
    return html.Div(
        [
            html.H3(
                "Sales, Profits and Quantity",
                className="text-base font-semibold mb-2",
            ),
            dcc.Graph(
                id=row_2A_id,
                figure=empty_figure(),
                className="flex-1 min-h-0",
            ),
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

            dcc.Graph(
                id=row_2B_id,
                className="flex-1 min-h-0",
            ),
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
            dcc.Graph(
                id=row_3A_id,
                className="flex-1 min-h-0",
            ),
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
            dcc.Graph(
                id=row_3B_id,
                className="flex-1 min-h-0",
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )
