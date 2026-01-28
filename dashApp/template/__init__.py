import dash
from dash import html

from shared.read_data import df

from dashApp.template.shared_layout import build_shared_layout
from dashApp.template.layouts.filter_options import build_filter_layout
from dashApp.template.layouts.KPI_template import build_kpi



def layout():

    filters = build_filter_layout(id_prefix="template")

    return build_shared_layout(
        filters=filters.children,
        kpis=[
            build_kpi(
                title="Total customers",
                kpi_id="template-total-customers",
                img_source="https://img.icons8.com/EBC351/ios11/2x/conference-call.png",
            ),
            build_kpi(
                title="Total sales",
                kpi_id="template-total-sales",
            ),
            build_kpi(
                title="Total profit",
                kpi_id="template-total-profit",
            ),
        ],
        row2=[
            html.Div("Row 2 - Chart A"),
            html.Div("Row 2 - Chart B"),
        ],
        row3=[
            html.Div("Row 3 - Chart A"),
            html.Div("Row 3 - Chart B"),
        ],
    )

""""
dash.register_page(
    __name__,
    path="/template",
    name="Template",
    order=4,
    layout=layout,  
)
"""