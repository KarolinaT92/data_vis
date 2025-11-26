from dashApp.initialize import cache
import plotly.io as pio
from shared.read_data import get_dataframe_from_store, df

CACHE_TIMEOUT = 3600  # 1 hour


# NOTE: This file should NOT contain any Dash @callback decorators
def figure_key(year, vis_name):
    return f"figure:{year}:{vis_name}"


def cache_figure_set(key, fig):
    cache.set(key, pio.to_json(fig), timeout=CACHE_TIMEOUT)


def cache_figure_get(key):
    j = cache.get(key)
    if not j:
        return None
    try:
        return pio.from_json(j)
    except Exception:
        cache.delete(key)
        return None


def invalidate_figure(year, vis_name):
    cache.delete(figure_key(year, vis_name))


def render_plot(selected_year: int, plot_name: str, build_function: callable):
    year_for_title = str(selected_year)
    key = figure_key(year_for_title, plot_name)
    # 1) FAST PATH: try cache
    fig = cache_figure_get(key)
    if fig is not None:
        return fig  # instant
    filtered_df = df[df['Year'] == selected_year]
    fig = build_function(filtered_df, year_for_title)
    cache_figure_set(key, fig)
    return fig
