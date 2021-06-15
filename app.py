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



app = dash.Dash(__name__, title="Demo app for presentation", assets_folder="./assets")

paper_color = "#dddddd"

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
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(7)

    return html.Div([
        html.Div([
            html.H1("Dash demo"),
        ], style={"textAlign": "center"}),
        html.Div([dcc.Dropdown(
            id="company-dropdown",
            options=dropdown_options,
            value="AAPL"
        ), dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=datetime.date(2021, 1, 1),
            max_date_allowed=end_date,
            start_date=start_date,
            end_date=end_date
        )]),
        html.Div([
            dcc.Graph(id="findata-graph")
        ])
    ])


@app.callback(
    Output("findata-graph", "figure"),
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("company-dropdown", "value"),
    ]
)
def update_graph(start_date, end_date, selected_company):
    start_date = datetime.datetime.fromisoformat(start_date)
    end_date = datetime.datetime.fromisoformat(end_date)

##    apple = yf.Ticker("aapl")
##    df = apple.history(interval="15m", start=start_date, end=end_date, actions=False)
    
    df = pd.read_csv("data/apple_data_cache.csv", index_col="Datetime") # in order to not exhaust the limited yf api calls

    exp12 = df["Close"].ewm(span=12, adjust=False).mean()
    exp26 = df["Close"].ewm(span=26, adjust=False).mean()

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03,
                        subplot_titles=(ticker_map[selected_company] + " stock", "Trading volume"),
                        row_width=[0.4, 0.6])

    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"],
        high=df["High"], low=df["Low"],
        close=df["Close"], name="OHLC"), row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=exp12, name="12 Period EMA"), row=1, col=1)
    fig.add_trace(go.Line(x=df.index, y=exp26, name="26 Period EMA"), row=1, col=1)
    fig.add_trace(go.Bar(y=df["Volume"], showlegend=False), row=2, col=1)

    fig.update_layout(xaxis=dict(type="category"))
    fig.update_xaxes(showticklabels=False)
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(height=900)
    fig.update_layout(paper_bgcolor=paper_color)

    return fig


app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(debug=True, port=4000)
