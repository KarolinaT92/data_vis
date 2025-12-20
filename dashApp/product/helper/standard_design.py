import calendar

TOP_LEFT_TITLE = {
    'x': 0.0,  # Position on the far left
    'xanchor': 'left',  # Align the text start to the left edge
    'y': 0.95,  # Position near the top
    'yanchor': 'top',  # Align the top of the text to the position
    'font': {'size': 13},
    'pad': {'t': 0, 'b': 0, 'l': 10, 'r': 0}
}
MODE_BAR = {'orientation': 'v'}  # Set the orientation to 'v' (vertical)

SALES_COLOR = "rgba(110, 150, 180, 0.8)"  # Muted Blue/Teal
PROFIT_COLOR = "#FF9966"  # Soft Coral/Orange

#  for bubble chart
CAT_COLORS = {
    "Furniture": "#007bff",
    "Office Supplies": "#ffa600",
    "Technology": "#374151"  #green: "#2ca02c", dard gray: "#374151"
}

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_ABBR = {i: calendar.month_abbr[i] for i in range(1, 13)}

PIE_CHART_HEIGHT = {"height": "12vh"}
FIRST_LAYER_HEIGHT = {"height": "22vh"}
SECOND_LAYER_HEIGHT = {"height": "25vh"}
THIRD_LAYER_HEIGHT = {"height": "37vh"}

DISPLAY_COLS = [
    'Product Name', 'Order Date', 'Discount', 'Quantity', 'Sales', 'Profit', 'Profit Margin (%)',
    'Original Unit Price', 'Ship Date', 'Ship Mode', 'Ship_Duration', 'Customer Name',
    'Segment', 'City', 'State', 'Postal Code', 'Region'
]
