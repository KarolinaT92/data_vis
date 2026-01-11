import dash
from .layout import layout
from . import callbacks

dash.register_page(__name__,
                   path="/customers",
                   name="Customers",
                   order=2,
                   layout=layout)
