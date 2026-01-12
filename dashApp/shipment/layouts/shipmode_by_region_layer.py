from dash import dcc

def shipmode_by_region_layout():
    return dcc.Graph(
        id="shipment-region-shipmode-stacked",
        style={"height": "100%"},
    )
