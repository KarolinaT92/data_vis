import dash
from dashApp.product.layouts.layout import layout
from . import callbacks

dash.register_page(__name__,
                   path="/products",
                   name="Products",
                   order=2,
                   layout=layout, )
