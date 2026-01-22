from dash import html
from dashApp.template.components.cards import CARD_CENTER


def kpi_row(kpis):
    """
    kpis: list of Dash components (recommended length = 3)
    """
    return html.Div(
        className="grid grid-cols-1 md:grid-cols-3 gap-8",
        children=[
            html.Div(kpi, className=CARD_CENTER)
            for kpi in kpis
        ],
    )
