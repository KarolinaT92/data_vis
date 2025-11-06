import dash
from .layout import layout

dash.register_page(__name__,
                   path="/customers",
                   name="Customers",
                   order=3,
                   layout=layout)
