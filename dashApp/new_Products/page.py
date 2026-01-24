from dash import register_page

from dashApp.template.shared_layout import build_shared_layout
from dashApp.template.layouts.filter_options import build_filter_layout
from dashApp.template.layouts.KPI_template import build_kpi

from .layouts import (
    row_2A,
    row_2B,
    row_3A,
    row_3B
)

from . import callbacks


def layout():
    filters = build_filter_layout(id_prefix="shipment", display_segment=False)

    return build_shared_layout(
        filters=filters,
        kpis=[
            build_kpi(
                title="Total Sales",
                kpi_id="kpi-total-sales",
                img_source="https://img.icons8.com/EBC351/ios11/2x/checkout.png"
            ),
            build_kpi(
                title="Total Profits",
                kpi_id="kpi-profit",
                img_source="https://img.icons8.com/EBC351/ios11/2x/growing-money.png"
            ),
            build_kpi(
                title="Total sold Products",
                kpi_id="kpi-orders",
                img_source="https://img.icons8.com/EBC351/ios11/2x/shopping-basket-success.png"
            ),
        ],
        row2=[
            row_2A(),
            row_2B(),
        ],
        row3=[
            row_3A(),
            row_3B(),
        ],
    )


register_page(
    __name__,
    path="/new_Products",
    name="new_Products",
    order=5,
    layout=layout,
)
