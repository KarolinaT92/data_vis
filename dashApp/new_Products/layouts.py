from dash import html, dcc
import dash_daq as daq
from .constants import ROW_2A_ID, ROW_2B_ID, ROW_3A_ID, ROW_3B_ID, VIEW_MODE_DROPDOWN_ID, SELECT_ON_SCATTER_PLOT, \
    CLEAR_SELECTION_BUTTON_ID, METRIC_OPTIONS_TOP_PRODUCTS_ID, METRIC_OPTIONS_TOP_HEATMAP_ID, SWITCH_HEATMAP, \
    PRODUCT_SLIDER, PLOT_TYPE_DROPDOWN_ID
from .figures import empty_figure
from ..template.plot_height import PLOT_HEIGHT

HIDE_MODEBAR = {"displayModeBar": False, "displaylogo": False}

heatmap_options = [
    {"label": "Sales ($)", "value": "Sales"},
    {"label": "Profit ($)", "value": "Profit"},
    {"label": "Profit Margin (%)", "value": "Profit Margin"},
]

product_options = [
    {"label": "Sales ($)", "value": "Sales"},
    {"label": "Profit ($)", "value": "Profit"},
]


def metric_dropdown(id, options=None):
    return html.Div(
        className="relative z-50 mb-2",  # key
        children=[
            html.Div(
                className="flex items-center gap-1",
                children=[
                    html.Label("Metric", className="filter-label whitespace-nowrap"),
                    dcc.Dropdown(
                        id=id,
                        options=options,
                        value="Profit",
                        clearable=False,
                        className="w-44 text-sm",
                    ),
                ],
            )
        ],
    )


config = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        # zoom / pan
        "zoom2d", "pan2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
        # hover / compare
        "hoverClosestCartesian", "hoverCompareCartesian",
    ],
},


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
                "↺ Reset",
                id=CLEAR_SELECTION_BUTTON_ID,
                className="text-sm px-3 py-1 rounded-md border dash-btn-reset",
                style={
                    "display": "none",
                    "whiteSpace": "nowrap",  # prevent wrapping
                    "padding": "6px 12px",  # vertical + horizontal padding
                    "width": "fit-content",  # auto width based on text
                    "color": "#1e3a8a",
                    "backgroundColor": "#eff6ff",
                },
            ),

            html.Div(
                className="",
                children=[
                    dcc.Loading(
                        children=dcc.Graph(
                            id=ROW_2A_ID,
                            figure=empty_figure(),
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
                        style={"height": "100%"},
                    )
                ]
            )

        ],
        className="flex flex-col h-full min-h-0",

    )


def row_2B():
    return html.Div(
        [
            html.H3(
                "Top 10 profitable Products",
                className="text-base font-semibold mb-2 shrink-0",
            ),

            html.Div(
                className="flex items-center gap-4 mb-2 shrink-0",
                children=[
                    metric_dropdown(METRIC_OPTIONS_TOP_PRODUCTS_ID, product_options),
                    html.Div(
                        className="flex items-center gap-3",
                        children=[
                            html.Label(
                                "Top Products",
                                className="text-sm font-medium whitespace-nowrap text-slate-600",
                            ),
                            dcc.Slider(
                                id=PRODUCT_SLIDER,
                                min=5,
                                max=15,
                                value=5,
                                marks={5: "Top 5", 10: "Top 10", 15: "Top 15"},
                                tooltip={"placement": "bottom", "always_visible": False},
                                className="w-48",
                            ),
                        ],
                    ),
                ],
            ),

            # Graph area fills remaining height of the card
            html.Div(
                className="flex-1 min-h-0 overflow-hidden",
                children=[
                    dcc.Loading(
                        children=dcc.Graph(
                            id=ROW_2B_ID,
                            config={**HIDE_MODEBAR, "responsive": True},
                            style={"height": "100%", "width": "100%"},
                        ),
                        type="circle",
                        style={"height": "100%"},
                    )
                ],
            ),
        ],
        className="flex flex-col h-full min-h-0 overflow-hidden",
    )


def row_3A():
    return html.Div(
        [
            html.H3(
                "Sales Over Time",
                className="text-base font-semibold mb-2",
            ),
            html.Div(
                className="relative z-50 mb-2",  # key
                children=[
                    html.Div(
                        className="flex items-center gap-1",
                        children=[
                            html.Label("Plot Type", className="filter-label whitespace-nowrap"),
                            dcc.Dropdown(
                                id=PLOT_TYPE_DROPDOWN_ID,
                                options=[
                                    {"label": "Bar chart", "value": "Bar chart"},
                                    {"label": "Line chart", "value": "Line chart"},
                                ],
                                value="Bar chart",
                                clearable=False,
                                className="w-40 text-sm",
                            ),
                        ],
                    )
                ],
            ),
            dcc.Loading(
                dcc.Graph(
                    id=ROW_3A_ID,
                    className="flex-1 min-h-0",
                    style=PLOT_HEIGHT,
                    config=HIDE_MODEBAR
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
            html.Div(
                className="flex items-center gap-4",
                children=[
                    metric_dropdown(METRIC_OPTIONS_TOP_HEATMAP_ID, heatmap_options),
                    html.Div(
                        children=[
                            html.P("display values", className="mr-2 text-sm"),
                            daq.BooleanSwitch(
                                id=SWITCH_HEATMAP,
                                on=False,
                                size=25
                            ),
                        ],
                        className=(
                            "flex items-center px-3 py-1 rounded shadow z-10 bg-gray-100 mb-1"
                        ),
                        style={
                            "color": "#1e3a8a",
                            "backgroundColor": "#eff6ff",
                        },
                    ),
                ],
            ),

            dcc.Loading(dcc.Graph(
                id=ROW_3B_ID,
                className="flex-1 min-h-0",
                style=PLOT_HEIGHT,
                config=HIDE_MODEBAR
            ), type="circle"),

        ],
        className="flex flex-col h-full min-h-0",
    )
