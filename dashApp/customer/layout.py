from dash import html

from .layouts import (
    kpi_layout,
    customers_chart_layout,
    customers_table_layout,
    discount_layout,
    map_layout,
    sales_microbands_chart_layout,
    profit_detail_layout,
    profit_heatmap_layout,
    filter_layout,
)

# ====================================================
# MAIN CONTENT
# ====================================================
content = html.Div(
    style={
        "padding": "20px 30px 40px 30px",
        "flex": 1,
    },
    children=[

        # ====================================================
        # SECTION 1 — KPI + DISCOUNT (LEFT) | MAP (RIGHT)
        # ====================================================
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "35% 65%",
                "gridTemplateRows": "auto 460px",
                "gap": "24px",
                "marginBottom": "40px",
                "alignItems": "stretch",
            },
            children=[

                # KPI — top left
                html.Div(
                    kpi_layout,
                    className="border-2 rounded p-3",
                    style={
                        "gridColumn": "1",
                        "gridRow": "1",
                        "backgroundColor": "white",
                    },
                ),

                # DISCOUNT — bottom left
                html.Div(
                    discount_layout,
                    className="border-2 rounded p-3",
                    style={
                        "gridColumn": "1",
                        "gridRow": "2",
                        "backgroundColor": "white",
                    },
                ),

                # MAP — right, spans both rows
                html.Div(
                    map_layout,
                    className="border-2 rounded p-3 overflow-hidden",
                    style={
                        "gridColumn": "2",
                        "gridRow": "1 / span 2",
                        "backgroundColor": "white",
                    },
                ),
            ],
        ),

        # ====================================================
        # SECTION 2 — TOP CUSTOMERS + TABLE
        # ====================================================
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "24px",
                "marginBottom": "40px",
            },
            children=[
                html.Div(
                    customers_chart_layout,
                    className="border-2 rounded p-3",
                    style={"backgroundColor": "white"},
                ),
                html.Div(
                    customers_table_layout,
                    className="border-2 rounded p-3",
                    style={"backgroundColor": "white"},
                ),
            ],
        ),

        # ====================================================
        # SECTION 3 — SALES + HEATMAP + PROFIT DETAIL
        # ====================================================
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "2fr 1fr",
                "gap": "24px",
            },
            children=[

                # SALES CHART — left
                html.Div(
                    sales_microbands_chart_layout,
                    className="border-2 rounded p-3",
                    style={"backgroundColor": "white"},
                ),

                # RIGHT COLUMN — HEATMAP + PROFIT DETAIL
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateRows": "300px 1fr",
                        "gap": "20px",
                        "minHeight": "600px",
                    },
                    children=[
                        html.Div(
                            profit_heatmap_layout,
                            className="border-2 rounded p-3 overflow-hidden",
                            style={"backgroundColor": "white"},
                        ),
                        html.Div(
                            profit_detail_layout,
                            className="border-2 rounded p-3 overflow-hidden",
                            style={"backgroundColor": "white"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# ====================================================
# FINAL PAGE WRAPPER
# ====================================================
layout = html.Div(
    style={
        "display": "flex",
        "minHeight": "100vh",
        "backgroundColor": "#f5f5f5", 
    },
    children=[
        filter_layout,
        html.Div(
            content,
            style={
                "flex": 1,
                "overflowX": "hidden",  
            },
        ),
    ],
)
