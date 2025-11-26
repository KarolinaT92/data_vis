from dashApp.initialize import cache
import plotly.io as pio
from shared.read_data import get_dataframe_from_store

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

# @cache.memoize(timeout=3600)  # cache for 1 hour, adjust as needed
# def get_grouped_data(data_json):
#     """
#     Compute the grouped data for a given year's dataframe.
#     """
#     dff = get_dataframe_from_store(data_json)
#     grouped = (
#         dff.groupby("Category", as_index=False)
#         .agg({
#             "Sales": "sum",
#             "Profit": "sum",
#             "Quantity": "sum"
#         })
#     )
#     return grouped
