from dash import register_page

from dashApp.template.shared_layout import build_shared_layout
from dashApp.template.layouts.filter_options import build_filter_layout
from dashApp.template.layouts.KPI_template import build_kpi

from .layouts import (
    speed_share_card,
    shipmode_driver_card,
    year_distribution_card,
    topn_subcategories_card,
)

from . import callbacks


def layout():
    filters = build_filter_layout(id_prefix="shipment")

    return build_shared_layout(
        filters=filters,
        kpis=[
            build_kpi(
                title="Avg Ship Duration",
                kpi_id="shipment-avg-duration",
            ),
            build_kpi(
                title="On-time Rate",
                kpi_id="shipment-on-time",
            ),
            build_kpi(
                title="Total Shipments",
                kpi_id="shipment-total",
            ),
        ],
        row2=[
            speed_share_card(),
            shipmode_driver_card(),
        ],
        row3=[
            year_distribution_card(),
            topn_subcategories_card(),
        ],
    )


register_page(
    __name__,
    path="/shipments",
    name="Shipments",
    order=3,
    layout=layout,
)
