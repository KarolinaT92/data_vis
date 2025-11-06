import dash
from .layout import layout

dash.register_page(__name__,
                   path="/products",
                   name="Products",
                   order=2,
                   layout=layout, )
