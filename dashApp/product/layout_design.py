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
        style={"justifySelf": "start"},
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
            className="grid grid-cols-1 md:grid-cols-2 gap-4 min-h-0 flex-1",
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
        className="col-span-12 lg:col-span-10 min-h-0",
        children=[
            html.Div(
                className="flex flex-col gap-1 min-h-0",
                # This is the only "fixed" vertical boundary: the viewport shell
                style={
                    "height": f"calc(100vh - {NAVBAR_HEIGHT}px - {BOTTOM_BUFFER}px)"
                },
                children=[
                    kpi_section,
                    # charts area fills the remaining height
                    html.Div(
                        className="flex flex-col flex-1 min-h-0 gap-8",
                        children=[
                            chart_row(row2, flex=1),
                            chart_row(row3, flex=1),
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
        # Use min-h-screen instead of h-full so the height chain is well-defined
        className="w-full min-h-screen overflow-hidden",
        children=[
            html.Div(
                className="w-full max-w-[1600px] mx-auto p-4",
                children=[
                    html.Div(
                        className="grid grid-cols-12 gap-4 min-h-0",
                        children=[filter_column, visualization_column],
                    )
                ],
            )
        ],
    )
