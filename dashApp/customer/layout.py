from dash import html, dcc
from shared.read_data import df

from .layouts import (
    kpi_layout,
    customers_chart_layout,
    customers_table_layout,
    discount_layout,
    map_layout,
    sales_microbands_chart_layout,
    profit_detail_layout,
    profit_heatmap_layout,
)

# Filter options
YEARS = sorted(df["Year"].dropna().unique())
SEGMENTS = sorted(df["Segment"].dropna().unique())
REGIONS = sorted(df["Region"].dropna().unique())
DEFAULT_YEAR = max(YEARS)


# ============================================
# FIXED FLOATING SIDEBAR
# ============================================
sidebar = html.Div(
    id="sidebar",
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "width": "260px",
        "height": "100vh",
        "background": "#f7f7f7",
        "borderRight": "1px solid #ddd",
        "padding": "20px",
        "overflowY": "auto",
        "zIndex": 1000,
    },
    children=[
        html.H3("Filters"),

        html.Div([
            html.Label("Year", style={"fontWeight": 600}),
            dcc.Dropdown(
                id="customer-year-dropdown",
                options=[{"label": str(y), "value": int(y)} for y in YEARS],
                value=int(DEFAULT_YEAR),
                clearable=False,
            ),
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Segment", style={"fontWeight": 600}),
            dcc.Dropdown(
                id="customer-segment-dropdown",
                options=[{"label": s, "value": s} for s in SEGMENTS],
                value=SEGMENTS,
                multi=True,
                clearable=False,
            ),
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Region", style={"fontWeight": 600}),
            dcc.Dropdown(
                id="customer-region-dropdown",
                options=[{"label": r, "value": r} for r in REGIONS],
                value=REGIONS,
                multi=True,
                clearable=False,
            ),
        ]),
    ]
)


# ============================================
# MAIN CONTENT AREA — SCROLLABLE
# ============================================
content = html.Div(
    style={
        "paddingLeft": "300px",
        "paddingRight": "30px",
        "paddingTop": "20px",
        "paddingBottom": "40px",
    },
    children=[

        # ====================================================
        # SECTION 1 — KPIs + MAP + DISCOUNT
        # ====================================================
        html.Div(
            style={
                "display": "flex",
                "gap": "24px",
                "flexWrap": "wrap",
                "alignItems": "flex-start",
            },
            children=[
                # LEFT: KPI + MAP
                html.Div(
                    style={
                        "flex": 1,
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "20px",
                        "minWidth": "350px",
                    },
                    children=[
                        html.Div(kpi_layout),
                        html.Div(map_layout),
                    ],
                ),

                # RIGHT: DISCOUNT
                html.Div(
                    discount_layout,
                    style={"flex": 1, "minWidth": "380px"},
                ),
            ],
        ),

        # ====================================================
        # SECTION 2 — TOP CUSTOMERS + TABLE
        # ====================================================
        html.Div(
            style={
                "display": "flex",
                "gap": "24px",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(customers_chart_layout, style={"flex": 1, "minWidth": "350px"}),
                html.Div(customers_table_layout, style={"flex": 1, "minWidth": "350px"}),
            ],
        ),

        # ====================================================
        # SECTION 3 — SALES + (HEATMAP ABOVE PROFIT DETAIL)
        # WITH FINAL HEATMAP FIX (GRID + REAL HEIGHT)
        # ====================================================
        html.Div(
            style={
                "display": "flex",
                "gap": "24px",
                "flexWrap": "wrap",
            },
            children=[

                # LEFT — SALES CHART
                html.Div(
                    sales_microbands_chart_layout,
                    style={
                        "flex": 2,
                        "minWidth": "450px",
                    },
                ),

                # RIGHT — HEATMAP + PROFIT DETAIL (stable grid)
                html.Div(
                    style={
                        "flex": 1,
                        "minWidth": "350px",
                        "display": "grid",
                        "gridTemplateRows": "300px 1fr",
                        "rowGap": "20px",
                        "alignContent": "stretch",
                        "minHeight": "600px",
                    },
                    children=[

                        # HEATMAP (TOP)
                        html.Div(
                            profit_heatmap_layout,
                            style={
                                "overflow": "hidden",
                                "minHeight": "300px",
                                "height": "100%",
                            },
                        ),

                        # PROFIT DETAIL (BOTTOM)
                        html.Div(
                            profit_detail_layout,
                            style={
                                "overflow": "hidden",
                            },
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# ============================================
# FINAL PAGE WRAPPER
# ============================================
layout = html.Div(
    children=[sidebar, content],
    style={
        "position": "relative",
        "overflow": "visible",
    },
)
