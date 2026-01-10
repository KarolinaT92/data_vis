from dash import dcc

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


def shipmode_by_region_layout():
    return dcc.Graph(
        id="shipment-region-shipmode-stacked",
        config=PLOTLY_DOWNLOAD_ONLY_CONFIG, 
    )
