# import necessary libraries
import yfinance as yf
import datetime
import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objects as go

from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html


# set start and end dates (also possible: period kwarg)
"""end = datetime.datetime.today()
start = end - datetime.timedelta(days=5)"""

# read data about the apple stock (AAPL)
# actions=False (defaults to True) : avoid downloading unnecessary data
"""apple = yf.Ticker("aapl")
data = apple.history(interval="5m", start=start, end=end, actions=False)"""
# commented out so they don't blacklist me lmao


app = dash.Dash(__name__, title="Demo app for presentation", assets_folder="assets")

ticker_map = {
    "AAPL": "Apple",
    "GOOG": "Google",
    "TSLA": "Tesla",
    "SPY": "S&P 500 ETF",
}

dropdown_options = []
for symbol, company in ticker_map.items():
    dropdown_options.append({
        "label": company,
        "value": symbol
    })

def serve_layout():
    end = datetime.datetime.now()
    start = end - datetime.timedelta(7)

    return html.Div([
        html.Div([
            html.H1("Dash demo"),
        ], style={"textAlign": "center"}),
        html.Div([dcc.Dropdown(
            id="company-dropdown",
            options=dropdown_options,
            value="AAPL"
        ), dcc.DatePickerRange(
            id="date-range,
            min_date_allowed=datetime.date(2021, 1, 1),
            max_date_allowed=end_date,
            start_date=start,
            end_date=end
        )]),
        html.Div([
            dcc.Graph(id="findata-graph")
        ])
    ])


