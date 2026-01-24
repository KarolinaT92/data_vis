from dash import html
from dashApp.template.components import CARD, kpi_row

# --------------------------------------------------
# LAYOUT CONSTANTS
# --------------------------------------------------

NAVBAR_HEIGHT = 64
BOTTOM_BUFFER = 30
KPI_HEIGHT = 120


def build_shared_layout(*, filters, kpis, row2, row3):
    assert len(row2) == 2
    assert len(row3) == 2

    # -------------------------------
    # FILTER COLUMN
    # -------------------------------
    filter_column = html.Div(
        filters,
        className="""
        col-span-12 lg:col-span-2
        bg-gray-50 p-4 rounded-xl
        max-w-[280px] 
        w-full
        """,
        style={
            "justifySelf": "start",
        },
    )

    # -------------------------------
    # KPI ROW 
    # -------------------------------
    kpi_section = html.Div(
        kpi_row(kpis),
        style={"height": f"{KPI_HEIGHT}px"},
        className="flex-shrink-0",
    )

    # -------------------------------
    # CHART ROW HELPER
    # -------------------------------
    def chart_row(components, flex):
        return html.Div(
            className="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-0",
            style={"flex": flex},
            children=[
                html.Div(
                    component,
                    className=f"{CARD} flex flex-col h-full min-h-0 overflow-hidden",
                )
                for component in components
            ],
        )

    # -------------------------------
    # VISUALIZATION COLUMN
    # -------------------------------
    visualization_column = html.Div(
        className="col-span-12 lg:col-span-10 h-full min-h-0",
        children=[
            html.Div(
                className="flex flex-col gap-1 min-h-0",
                style={
                    "height": f"calc(100vh - {NAVBAR_HEIGHT}px - {BOTTOM_BUFFER}px)"
                },
                children=[
                    kpi_section,

                    html.Div(
                        className="flex flex-col flex-1 gap-8 min-h-0",
                        children=[
                            chart_row(row2, flex=5),
                            chart_row(row3, flex=5),
                        ],
                    ),
                ],
            )
        ],
    )

    # -------------------------------
    # ROOT
    # -------------------------------
    return html.Div(
        className="w-full h-full min-h-0 overflow-hidden",
        children=[
            html.Div(
                className="w-full max-w-[1600px] mx-auto p-4",
                children=[
                    html.Div(
                        className="grid grid-cols-12 gap-4 h-full min-h-0 overflow-hidden",
                        children=[filter_column, visualization_column],
                    )
                ],
            )
        ],
    )

    #
    # return html.Div(
    #     className="grid grid-cols-12 gap-4 2xl:gap-2 h-full min-h-0 overflow-hidden p-4",
    #     children=[filter_column, visualization_column],
    # )
