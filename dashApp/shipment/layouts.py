from dash import html, dcc
from .figures import empty_figure


def speed_share_card():
    return html.Div(
        [
            html.H3(
                "Delivery Speed & Share of Orders",
                className="text-base font-semibold mb-2",
            ),
            dcc.Graph(
                id="shipment-speed-share-combined",
                figure=empty_figure(),
                className="flex-1 min-h-0",
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )


def shipmode_driver_card():
    return html.Div(
        [
            html.H3(
                "Ship Mode Distribution",
                className="text-base font-semibold mb-2",
            ),
            html.Div(
                [
                    dcc.RadioItems(
                        id="shipment-driver-dimension",
                        options=[
                            {"label": "Region", "value": "Region"},
                            {"label": "Segment", "value": "Segment"},
                        ],
                        value="Region",
                        inline=True,
                    ),
                    dcc.Checklist(
                        id="shipment-normalize-toggle",
                        options=[
                            {"label": "Normalize by percentage", "value": "pct"}
                        ],
                        value=["pct"],
                        inline=True,
                    ),
                ],
                className="flex gap-4 mb-2 flex-shrink-0",
            ),
            dcc.Graph(
                id="shipment-shipmode-driver",
                className="flex-1 min-h-0",
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )


def year_distribution_card():
    return html.Div(
        [
            html.H3(
                "Shipment Distribution Over Time",
                className="text-base font-semibold mb-2",
            ),
            dcc.Graph(
                id="shipment-year-distribution",
                className="flex-1 min-h-0",
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )


def topn_subcategories_card():
    return html.Div(
        [
            html.H3(
                "Top Sub-Categories",
                className="text-base font-semibold mb-2",
            ),
            dcc.Dropdown(
                id="shipment-topn",
                options=[
                    {"label": "Top 5", "value": 5},
                    {"label": "Top 10", "value": 10},
                    {"label": "Top 15", "value": 15},
                ],
                value=10,
                clearable=False,
                className="mb-2 flex-shrink-0",
            ),
            dcc.Checklist(
                id="shipment-drilldown-show-values",
                options=[{"label": "Show values", "value": "on"}],
                value=["on"],
                inline=True,
                className="mb-2 flex-shrink-0",
            ),
            dcc.Graph(
                id="shipment-topn-subcategories",
                className="flex-1 min-h-0",
            ),
        ],
        className="flex flex-col h-full min-h-0",
    )
