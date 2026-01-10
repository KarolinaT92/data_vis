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

def days_vs_popularity_layout():
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.H4("Delivery Time by Ship Mode"),
                    dcc.Graph(id="shipment-boxplot-duration-by-mode", config=PLOTLY_DOWNLOAD_ONLY_CONFIG),
                ]
            ),
            html.Div(
                children=[
                    html.H4("Share of Orders by Ship Mode"),
                    dcc.Graph(id="shipment-bar-share-by-mode", config=PLOTLY_DOWNLOAD_ONLY_CONFIG),
                ]
            ),
        ]
    )
