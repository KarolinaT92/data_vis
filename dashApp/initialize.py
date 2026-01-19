import os
from dash import Dash, html, dcc, page_container
from flask_caching import Cache
import dash_mantine_components as dmc

app = Dash(
    __name__,
    external_scripts=[{'src': 'https://cdn.tailwindcss.com'}],
    use_pages=True,
    pages_folder="",
    suppress_callback_exceptions=True,
    title="Superstore Dashboard",
)
server = app.server

# --- Cache setup ---
CACHE_DIR = os.path.join(os.getcwd(), 'cache-directory')
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_CONFIG = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": CACHE_DIR,
    "CACHE_DEFAULT_TIMEOUT": 3600,
}
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)

import dashApp.product, dashApp.customer, dashApp.shipment, dashApp.template  # this must be after app definition

app.layout = dmc.MantineProvider(
    defaultColorScheme="light",  # or "dark" if you prefer
    withCssVariables=True,  # optional, but nice for theming
    children=[
        html.Div(
            [
                dcc.Location(id="url"),
                html.Nav(id="nav", className="navbar"),
                html.Main(page_container, className="page"),
            ],
            className="app-shell"
        )
    ]
)
