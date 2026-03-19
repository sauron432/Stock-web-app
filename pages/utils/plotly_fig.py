import plotly.graph_objects as go
import pandas as pd
import ta
import dateutil
import datetime

axis_style = dict(
    color="white",
    showgrid=True,
    gridcolor="#2a2a3e",
    gridwidth=1,
    linecolor="#555555",
    zeroline=True,
    zerolinecolor="#444444",
)


def plotly_table(df, max_height=400):
    index_vals = [str(i)[:10] for i in df.index.tolist()]

    col_names = ["Date"] + df.columns.tolist()
    col_values = [index_vals] + [df[col].tolist() for col in df.columns]

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=col_names,
                    fill_color="#1a1a2e",
                    font=dict(color="white", size=13),
                    align="left",
                    line_color="#1a1a2e",
                    height=36,
                ),
                cells=dict(
                    values=col_values,
                    fill_color=[["#13071e", "#1e0f35"] * len(df)],
                    font=dict(color="white", size=12),
                    align=["left"] + ["right"] * len(df.columns),
                    line_color=["#0f0f1a", "#1a1a2e"],
                    height=32,
                ),
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max_height,
    )
    return fig


def filter_data(dataframe, num_period):
    # FIX: correct relativedelta values (5d was using months=-5, 1y was using months=-1)
    if num_period == "1mo":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == "5d":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == "6mo":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == "1y":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == "5y":
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == "ytd":
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]

    return dataframe.reset_index()[dataframe.reset_index()["Date"] > date]


def close_chart(dataframe, num_period=False):
    if isinstance(dataframe.columns, pd.MultiIndex):
        dataframe.columns = dataframe.columns.get_level_values(0)
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Open"],
            mode="lines",
            name="Open",
            line=dict(width=2, color="#5ab7ff"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2, color="black"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["High"],
            mode="lines",
            name="High",
            line=dict(width=2, color="#0078ff"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Low"],
            mode="lines",
            name="Low",
            line=dict(width=2, color="red"),
        )
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        title=dict(
            text="Price Chart",  # change per function
            font=dict(color="white", size=16),
            x=0.5,  # left align
        ),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f1a",
        font=dict(color="white"),
        xaxis=axis_style,
        yaxis=axis_style,
        # Border via margin + shape
        margin=dict(l=10, r=10, t=40, b=10),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#444466", width=1),
            )
        ],
    )
    return fig


def candle_stick(dataframe, num_period):
    if isinstance(dataframe.columns, pd.MultiIndex):
        dataframe.columns = dataframe.columns.get_level_values(0)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=dataframe["Date"],
            open=dataframe["Open"],
            high=dataframe["High"],
            low=dataframe["Low"],
            close=dataframe["Close"],
        )
    )
    fig.update_layout(
        title=dict(
            text="Candlestick Chart",  # change per function
            font=dict(color="white", size=16),
            x=0.5,  # left align
        ),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f1a",
        font=dict(color="white"),
        xaxis=axis_style,
        yaxis=axis_style,
        # Border via margin + shape
        margin=dict(l=10, r=10, t=40, b=10),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#444466", width=1),
            )
        ],
    )
    return fig


def RSI(dataframe, num_period):
    if isinstance(dataframe.columns, pd.MultiIndex):
        dataframe.columns = dataframe.columns.get_level_values(0)

    dataframe["RSI"] = ta.momentum.RSIIndicator(dataframe["Close"], window=14).rsi()
    dataframe = filter_data(dataframe, num_period)

    # close = dataframe["Close"].squeeze()
    # dataframe["RSI"] = ta.momentum.RSIIndicator(close, window=14).rsi()
    # dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["RSI"],
            name="RSI",
            line=dict(width=2, color="orange"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=[70] * len(dataframe),
            name="Overbought",
            line=dict(width=2, color="red", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=[30] * len(dataframe),
            name="Oversold",
            line=dict(width=2, color="#79da84", dash="dash"),
        )
    )

    fig.update_layout(
        title=dict(
            text="RSI (14)",  # change per function
            font=dict(color="white", size=16),
            x=0.5,  # left align
        ),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f1a",
        font=dict(color="white"),
        xaxis=axis_style,
        yaxis=axis_style,
        # Border via margin + shape
        margin=dict(l=10, r=10, t=40, b=10),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#444466", width=1),
            )
        ],
    )
    return fig


def Moving_average(dataframe, num_period=False):
    if isinstance(dataframe.columns, pd.MultiIndex):
        dataframe.columns = dataframe.columns.get_level_values(0)
    dataframe["SMA_20"] = ta.trend.SMAIndicator(
        dataframe["Close"], window=20
    ).sma_indicator()
    dataframe["SMA_50"] = ta.trend.SMAIndicator(
        dataframe["Close"], window=50
    ).sma_indicator()
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Open"],
            mode="lines",
            name="Open",
            line=dict(width=2, color="#5ab7ff"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2, color="black"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["High"],
            mode="lines",
            name="High",
            line=dict(width=2, color="#0078ff"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Low"],
            mode="lines",
            name="Low",
            line=dict(width=2, color="red"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["SMA_20"],
            mode="lines",
            name="SMA-20",
            line=dict(width=2, color="orange"),
        )
    )
    # FIX: was "SMA-50" (with dash) but column is named "SMA_50" (with underscore)
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["SMA_50"],
            mode="lines",
            name="SMA-50",
            line=dict(width=2, color="purple"),
        )
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        title=dict(
            text="Moving Average",  # change per function
            font=dict(color="white", size=16),
            x=0.5,  # left align
        ),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f1a",
        font=dict(color="white"),
        xaxis=axis_style,
        yaxis=axis_style,
        # Border via margin + shape
        margin=dict(l=10, r=10, t=40, b=10),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#444466", width=1),
            )
        ],
    )


def MACD(dataframe, num_period):
    if isinstance(dataframe.columns, pd.MultiIndex):
        dataframe.columns = dataframe.columns.get_level_values(0)

    # FIX: removed old pta.macd() calls, using only ta library
    macd_indicator = ta.trend.MACD(dataframe["Close"])
    dataframe["MACD"] = macd_indicator.macd()
    dataframe["MACD Signal"] = macd_indicator.macd_signal()
    dataframe["MACD Hist"] = macd_indicator.macd_diff()
    dataframe = filter_data(dataframe, num_period)

    colors = ["red" if val < 0 else "green" for val in dataframe["MACD Hist"]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["MACD"],
            name="MACD",
            line=dict(width=2, color="orange"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["MACD Signal"],
            name="Signal",
            line=dict(width=2, color="red", dash="dash"),
        )
    )
    # FIX: actually added the histogram bar chart (it was calculated but never plotted)
    fig.add_trace(
        go.Bar(
            x=dataframe["Date"],
            y=dataframe["MACD Hist"],
            name="Histogram",
            marker_color=colors,
        )
    )
    fig.update_layout(
        title=dict(
            text="MACD",  # change per function
            font=dict(color="white", size=16),
            x=0.5,  # left align
        ),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f1a",
        font=dict(color="white"),
        xaxis=axis_style,
        yaxis=axis_style,
        # Border via margin + shape
        margin=dict(l=10, r=10, t=40, b=10),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#444466", width=1),
            )
        ],
    )
    return fig


def moving_average_forecast(forecast):
    forecast = forecast.copy()
    forecast.index = pd.to_datetime(forecast.index)  # ensure datetime index
    
    split = len(forecast) - 30  # last 30 rows are forecast

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast.index[:split],
        y=forecast["Close"].iloc[:split],
        mode="lines",
        name="Close Price",
        line=dict(width=2, color="#5ab7ff"),
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index[split:],
        y=forecast["Close"].iloc[split:],
        mode="lines",
        name="Forecast",
        line=dict(width=2, color="orange", dash="dash"),
    ))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f1a",
        font=dict(color="white"),
        legend=dict(yanchor="top", xanchor="right"),
    )
    return fig
