from dash import html, dcc
import dash_daq as daq
from .constants import ROW_2A_ID, ROW_2B_ID, ROW_3A_ID, ROW_3B_ID, VIEW_MODE_DROPDOWN_ID, SELECT_ON_SCATTER_PLOT, \
    CLEAR_SELECTION_BUTTON_ID, METRIC_OPTIONS_TOP_PRODUCTS_ID, METRIC_OPTIONS_TOP_HEATMAP_ID, SWITCH_HEATMAP
from .figures import empty_figure
from ..template.plot_height import PLOT_HEIGHT

HIDE_MODEBAR = {"displayModeBar": False, "displaylogo": False}


def metric_dropdown(id):
    return html.Div(
        className="relative z-50 mb-2",  # key
        children=[
            html.Div(
                className="flex items-center gap-1",
                children=[
                    html.Label("Metric", className="filter-label whitespace-nowrap"),
                    dcc.Dropdown(
                        id=id,
                        options=[
                            {"label": "Sales ($)", "value": "Sales"},
                            {"label": "Profit ($)", "value": "Profit"},
                            {"label": "Profit Margin (%)", "value": "Profit Margin"},
                        ],
                        value="Profit",
                        clearable=False,
                        className="w-44 text-sm",
                    ),
                ],
            )
        ],
    )


def row_2A():
    return html.Div(
        [
            html.H3(
                "Sales, Profits and Quantity",
                className="text-base font-semibold mb-2",
            ),
            dcc.Store(id=SELECT_ON_SCATTER_PLOT, data=[]),
            html.Div(
                className="flex items-center gap-4",
                children=[
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
                    html.Div(
                        className="flex items-center gap-4",
                        children=[
                            # Left content
                            html.Div(
                                "Opacity",
                                className="text-sm font-medium whitespace-nowrap text-slate-600"
                            ),

                            # Slider
                            dcc.Slider(
                                id="opacity-slider",
                                min=0,
                                max=1,
                                step=0.05,
                                value=1,
                                marks={
                                    0: "0%",
                                    0.5: "50%",
                                    1: "100%",
                                },
                                tooltip={"placement": "bottom", "always_visible": False},
                                className="w-40",  # controls width
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
            html.Div(
                className="flex items-center gap-4",
                children=[
                    metric_dropdown(METRIC_OPTIONS_TOP_PRODUCTS_ID),
                    html.Div(
                        className="flex items-center gap-3",
                        children=[
                            html.Label("Top Products",
                                       className="text-sm font-medium whitespace-nowrap text-slate-600"),

                            dcc.Slider(
                                id="top-n-slider",
                                min=5,
                                max=15,
                                value=10,  # default
                                marks={
                                    5: "Top 5",
                                    10: "Top 10",
                                    15: "Top 15",
                                },
                                tooltip={"placement": "bottom", "always_visible": False},
                                className="w-48",
                            ),
                        ],
                    )

                ],
            )

            ,
            dcc.Loading(
                dcc.Graph(
                    id=ROW_2B_ID,
                    className="flex-1 min-h-0",
                    style=PLOT_HEIGHT,
                    config=HIDE_MODEBAR
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
                "Sales Over Time",
                className="text-base font-semibold mb-2",
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
                    metric_dropdown(METRIC_OPTIONS_TOP_HEATMAP_ID),
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
