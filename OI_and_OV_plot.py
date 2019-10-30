import pandas as pd
import scipy.stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os


def collect_OI_OV():
    filepath = 'data/Bitmex/OI_OV_XBT.csv'
    if os.path.isfile(filepath):
        pass
    else:
        filepath = '/opt/python/current/app/data/Bitmex/OI_OV_XBT.csv'
    OI_OV_df = pd.read_csv(filepath, index_col='timestamp')
    OI_OV_df.index = pd.to_datetime(OI_OV_df.index)
    return OI_OV_df


def update_OI_OV():
    r = requests.get('https://www.bitmex.com/api/v1/instrument?symbol=XBT&columns=timestamp%2C%20openInterest%2C%20openValue')
    if r.status_code != 200:
        r.raise_for_status()
    data = r.json()
    instrument_df = pd.DataFrame(data)
    instrument_df['openValue_BTC'] = instrument_df['openValue']/100000000
    filepath = 'data/Bitmex/OI_OV_XBT.csv'
    if os.path.isfile(filepath):
        pass
    else:
        filepath = '/opt/python/current/app/data/Bitmex/OI_OV_XBT.csv'
    instrument_df.to_csv(filepath, mode='a', header=False, index=False)


def collect_coinmetrics():
    # Get Price Data
    metrics = 'PriceUSD'
    r = requests.get('https://community-api.coinmetrics.io/v2/assets/btc/metricdata?metrics=' + metrics)
    r.raise_for_status()
    series = r.json()['metricData']['series']
    series_time = [series[i]['time'] for i in range(len(series))]
    series_values = [float(series[i]['values'][0]) for i in range(len(series))]
    coinmetrics_df = pd.DataFrame({'time': series_time, 'PriceUSD': series_values})
    coinmetrics_df.time = pd.to_datetime(coinmetrics_df.time, dayfirst=True)
    coinmetrics_df.index = coinmetrics_df.time
    coinmetrics_df.index = coinmetrics_df.index.tz_localize(None)
    return coinmetrics_df


def plot_open_interest(OI_OV_df, coinmetrics_df):
    """
    Inputs:
    OI_OV_df (dataframe): 'OI_OV_XBT.csv' dataframe declaration as well as a timeframe.

    Outputs:
    Returns a Plotly Figure object
    """
    OI_OV_df['openInterest_zscore'] = scipy.stats.zscore(OI_OV_df['openInterest'])
    OI_OV_df['openValue_zscore'] = scipy.stats.zscore(OI_OV_df['openValue_BTC'])
    first = OI_OV_df.dropna().index[0]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("Price", "Open Interest", "Open Values (BTC)"),
                        vertical_spacing=0.05)

    # Add traces
    fig.append_trace(go.Scatter(x=coinmetrics_df['PriceUSD'].loc[first:].index,
                                y=coinmetrics_df['PriceUSD'].loc[first:],
                                mode='lines+markers',
                                showlegend=True,
                                marker=dict(size=3,
                                            color=OI_OV_df['openInterest_zscore'],  # set color equal to a variable
                                            colorscale='viridis',  # one of plotly colorscales
                                            colorbar=dict(title='openInterest zscores', titleside="right"),
                                            showscale=True)
                                ),
                     row=1, col=1)

    fig.append_trace(go.Scatter(x=coinmetrics_df['PriceUSD'].loc[first:].index,
                                y=coinmetrics_df['PriceUSD'].loc[first:],
                                mode='lines+markers',
                                showlegend=True,
                                marker=dict(size=3,
                                            color=OI_OV_df['openValue_zscore'],  # set color equal to a variable
                                            colorscale='Rainbow',  # one of plotly colorscales
                                            colorbar=dict(x=1.15, title='openValue zscores', titleside="right"),
                                            showscale=True)
                                ),
                     row=1, col=1)

    fig.append_trace(go.Scatter(x=OI_OV_df['openInterest'].dropna().index, y=OI_OV_df['openInterest'].dropna(),
                                mode='lines+markers', showlegend=False,
                                marker=dict(size=3,
                                            color=OI_OV_df['openInterest_zscore'],  # set color equal to a variable
                                            colorscale='viridis',  # one of plotly colorscales
                                            showscale=False)),
                     row=2, col=1)
    fig.append_trace(go.Scatter(x=OI_OV_df['openValue_BTC'].dropna().index, y=OI_OV_df['openValue_BTC'].dropna(),
                                mode='lines+markers', showlegend=False,
                                marker=dict(size=3,
                                            color=OI_OV_df['openValue_zscore'],  # set color equal to a variable
                                            colorscale='Rainbow',  # one of plotly colorscales
                                            showscale=False)),
                     row=3, col=1)

    fig.update_yaxes(title_text="Price", type="log", row=1, col=1)
    fig.update_layout(height=1200, margin=dict(b=0, t=40, pad=1), legend=dict(x=0.88, y=0.99))
    return fig