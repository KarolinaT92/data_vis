import dash
from .layout import layout
from . import callbacks

dash.register_page(__name__,
                   path="/shipments",
                   name="Shipments",
                   order=4,
                   layout=layout )
