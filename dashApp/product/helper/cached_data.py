from dashApp.initialize import cache
import plotly.io as pio
from shared.read_data import get_dataframe_from_store, df

CACHE_TIMEOUT = 3600  # 1 hour


# NOTE: This file should NOT contain any Dash @callback decorators
def figure_key(year, vis_name, *extra_parts):
    parts = ["figure", str(year), vis_name]
    parts.extend(str(p) for p in extra_parts)
    return ":".join(parts)


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


def retrieve_cached_figure(key):
    fig = cache_figure_get(key)
    if fig is not None:
        return fig


class PlotRenderer:
    """This class handles filtering the DataFrame, generating a unique cache key from all
    plot parameters, and calling the specific plot build function with flexible arguments."""

    @staticmethod
    def render_plot(selected_year: int, plot_name: str, build_function: callable):
        year_for_title = str(selected_year)
        key = figure_key(year_for_title, plot_name)
        retrieve_cached_figure(key)

        filtered_df = df[df['Year'] == selected_year]
        generate_fig = build_function(filtered_df, year_for_title)
        cache_figure_set(key, generate_fig)
        return generate_fig

    @staticmethod
    def render_plot_top_profitable_products(selected_year: int, plot_name: str, build_function: callable,
                                            top_n: int = None):
        year_for_title = str(selected_year)
        key = figure_key(year_for_title, plot_name, top_n)
        retrieve_cached_figure(key)

        filtered_df = df[df['Year'] == selected_year]
        generate_fig = build_function(filtered_df, year_for_title, top_n)
        cache_figure_set(key, generate_fig)
        return generate_fig

    @staticmethod
    def render_selected_plot_type(selected_year: int, plot_name: str, build_function: callable,
                                  sales_chart_type: str, profit_chart_type: str):
        year_for_title = str(selected_year)
        key = figure_key(year_for_title, plot_name, sales_chart_type, profit_chart_type)
        retrieve_cached_figure(key)

        filtered_df = df[df['Year'] == selected_year]
        generate_fig = build_function(filtered_df, year_for_title, sales_chart_type, profit_chart_type)
        cache_figure_set(key, generate_fig)
        return generate_fig
