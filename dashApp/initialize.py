import os
from dash import Dash
from flask_caching import Cache

app = Dash(
    __name__,
    external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
    use_pages=True,
    pages_folder="",
    suppress_callback_exceptions=True,
    title="Superstore Dashboard",
)

server = app.server

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

CACHE_DIR = os.path.join(os.getcwd(), "cache-directory")
os.makedirs(CACHE_DIR, exist_ok=True)

cache = Cache()
cache.init_app(server, config={
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": CACHE_DIR,
    "CACHE_DEFAULT_TIMEOUT": 3600,
})

import dashApp.customer
import dashApp.shipment
import dashApp.template
import dashApp.product