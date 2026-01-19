import dash
from dashApp.template.layouts.shared_layout import shared_layout
from . import callbacks

dash.register_page(__name__,
                   path="/template",
                   name="template",
                   order=4,
                   layout=shared_layout, )