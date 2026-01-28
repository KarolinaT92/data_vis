from dash import register_page

from dashApp.template.shared_layout import build_shared_layout
from dashApp.template.layouts.filter_options import build_filter_layout
from dashApp.template.layouts.KPI_template import build_kpi

from .layouts import (
    customers_main_panel,
    map_layout,
    sales_microbands_chart_layout,
    profit_per_order_layout,
)

from . import callbacks


def layout():
    filters = build_filter_layout(id_prefix="customer")

    return build_shared_layout(
        filters=filters,
        kpis=[
            build_kpi(
                title="Total Customers",
                kpi_id="kpi-total-customers",
                img_source="https://img.icons8.com/EBC351/ios11/2x/conference-call.png",
            ),
            build_kpi(
                title="Most Profitable Region",
                kpi_id="kpi-top-region",
                img_source="https://img.icons8.com/EBC351/ios11/2x/worldwide-location.png",
            ),
            build_kpi(
                title="Most Profitable Segment",
                kpi_id="kpi-top-segment",
                img_source="https://img.icons8.com/EBC351/ios11/2x/group.png",
            ),
            build_kpi(
                title="Avg. profit per customer",
                kpi_id="kpi-avg-profit-per-customer",
                img_source="https://img.icons8.com/EBC351/ios11/2x/combo-chart.png",
            ),
        ],
        row2=[
            map_layout,
            customers_main_panel,
        ],
        row3=[
            sales_microbands_chart_layout,
            profit_per_order_layout,
        ],
    )


register_page(
    __name__,
    path="/new_customer",
    name="Customers",
    order=1,
    layout=layout,
)
