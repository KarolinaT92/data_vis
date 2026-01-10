from dash import html, dcc

PLOTLY_DOWNLOAD_ONLY_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "toggleSpikelines",
    ],
}

# ---------------------------------------
# STATIC LEGEND FOR SALES MICRO-BANDS
# ---------------------------------------
legend_row = html.Div(
    style={
        "display": "flex",
        "gap": "25px",
        "marginTop": "10px",
        "alignItems": "center",
    },
    children=[
        html.Div([
            html.Div(style={
                "backgroundColor": "rgba(78,121,167,0.75)",
                "width": "18px",
                "height": "18px",
                "display": "inline-block",
                "marginRight": "6px"
            }),
            html.Span("Furniture")
        ]),
        html.Div([
            html.Div(style={
                "backgroundColor": "rgba(242,142,43,0.75)",
                "width": "18px",
                "height": "18px",
                "display": "inline-block",
                "marginRight": "6px"
            }),
            html.Span("Technology")
        ]),
        html.Div([
            html.Div(style={
                "backgroundColor": "rgba(90,161,80,0.75)",
                "width": "18px",
                "height": "18px",
                "display": "inline-block",
                "marginRight": "6px"
            }),
            html.Span("Office Supplies")
        ]),
    ],
)

# ---------------------------------------
# SALES CATEGORY CHART (FLEXIBLE)
# ---------------------------------------
sales_microbands_chart_layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "gap": "10px",
        "width": "100%",
        "height": "100%",   
    },
    children=[
        html.H4("Sales by region"),
        legend_row,
        dcc.Graph(
            id="combined-sales-chart",
            style={
                "height": "100%",    
                "width": "100%",
            },
            config=PLOTLY_DOWNLOAD_ONLY_CONFIG,
        ),
    ],
)

# ---------------------------------------
# PROFIT DETAIL CHART (FLEXIBLE)
# ---------------------------------------
profit_detail_layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "gap": "10px",
        "width": "100%",
        "height": "100%",  
    },
    children=[
        html.H4("Sub-category profit (based on category selection)"),
        dcc.Graph(
            id="profit-detail-chart",
            style={
                "height": "100%",  
                "width": "100%",
            },
            config=PLOTLY_DOWNLOAD_ONLY_CONFIG,
        ),
    ],
)

# ---------------------------------------
# PROFIT HEATMAP (FLEXIBLE)
# ---------------------------------------
profit_heatmap_layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "gap": "10px",
        "width": "100%",
        "height": "100%", 
    },
    children=[
        html.H4("Profit heatmap (Region x Segment)"),
        dcc.Graph(
            id="profit-heatmap-chart",
            style={
                "height": "100%", 
                "width": "100%",
            },
            config=PLOTLY_DOWNLOAD_ONLY_CONFIG,
        ),
    ],
)
