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
                title="Total Orders",
                kpi_id="kpi-total-orders",
                img_source="https://img.icons8.com/EBC351/ios11/2x/shopping-basket-success.png",
            ),
            build_kpi(
                title="Average Delivery Time",
                kpi_id="kpi-average-delivery",
                img_source="https://img.icons8.com/EBC351/ios11/2x/delivery.png",
            ),
            build_kpi(
                title="Preferred Shipping",
                kpi_id="kpi-top-ship-mode",
                img_source="https://img.icons8.com/EBC351/ios11/2x/fast-cart.png",
            ),
        ],
        row2=[
            speed_share_card(),
            year_distribution_card(),
            
        ],
        row3=[
            shipmode_driver_card(),
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
