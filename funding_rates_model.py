import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import zscore
import requests
from collect_bitmex_funding import update_bitmex
import os


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


def collect_funding():
    update_bitmex()
    filepath = 'data/Bitmex/funding.csv'
    if os.path.isfile(filepath):
        pass
    else:
        filepath = '/opt/python/current/app/data/Bitmex/funding.csv'
    funding_rates_df = pd.read_csv(filepath, sep=',', index_col=['timestamp'], parse_dates=True)
    funding_rates_df.index = funding_rates_df.index.tz_localize(None)
    return funding_rates_df


def funding_rate_time_series_model(coinmetrics_df, funding_rates_df, tf):
    prices = coinmetrics_df['PriceUSD'].resample(tf).mean().to_frame()
    df1 = funding_rates_df.resample(tf).mean()
    df2 = pd.merge(prices.dropna(), df1, left_index=True, right_index=True, how='inner')

    df2['fundingRate_zscore'] = zscore(df2.fundingRate)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Price", "Funding rate zscores"),
                        vertical_spacing=0.1)

    fig.append_trace(go.Scatter(x=df2.index, y=df2['PriceUSD'], mode='lines+markers', showlegend=False,
                                marker=dict(size=5,
                                            color=df2['fundingRate_zscore'],  # set color equal to a variable
                                            colorscale='viridis',  # one of plotly colorscales
                                            colorbar=dict(title='Funding rate zscores', titleside="right"),
                                            showscale=True)),
                     row=1, col=1)

    fig.append_trace(go.Bar(x=df2.index, y=df2['fundingRate_zscore'], showlegend=False,
                            marker=dict(color=df2['fundingRate_zscore'],  # set color equal to a variable
                                        colorscale='viridis',  # one of plotly colorscales
                                        showscale=False,
                                        )
                            ),
                     row=2, col=1)
    fig.update_yaxes(type='log', row=1, col=1)
    fig.update_layout(legend=dict(x=0.72, y=0.25), height=800, margin=dict(b=10, t=50, pad=1))
    return fig
