import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import zscore


def collect_coinmetrics():
    # Get Price Data
    try:
        coinmetrics_df = pd.read_csv('data/Coinmetrics/Coinmetrics_btc.csv',
                                     usecols=['time', 'PriceUSD'], index_col=False)
    except FileNotFoundError:    # filepath is different when deployed on Elastic Beanstalk
        coinmetrics_df = pd.read_csv('/opt/python/current/app/data/Coinmetrics/Coinmetrics_btc.csv',
                                     usecols=['time', 'PriceUSD'], index_col=False)
    coinmetrics_df.time = pd.to_datetime(coinmetrics_df.time, dayfirst=True)
    coinmetrics_df.index = coinmetrics_df.time
    coinmetrics_df.index = coinmetrics_df.index.tz_localize(None)
    return coinmetrics_df


def collect_funding():
    try:
        funding_rates_df = pd.read_csv('data/Bitmex/funding.csv', sep=',', index_col=['timestamp'], parse_dates=True)
    except FileNotFoundError:
        funding_rates_df = pd.read_csv('/opt/python/current/app/data/Bitmex/funding.csv',
                                       sep=',', index_col=['timestamp'], parse_dates=True)
    funding_rates_df.index = funding_rates_df.index.tz_localize(None)
    return funding_rates_df


def funding_rate_time_series_model(coinmetrics_df, funding_rates_df, tf):
    prices = coinmetrics_df['PriceUSD'].resample(tf).mean().to_frame()
    df1 = funding_rates_df.resample(tf).mean()
    df2 = pd.merge(prices.dropna(), df1, left_index=True, right_index=True, how='inner')

    df2['fundingRate_zscore'] = zscore(df2.fundingRate)

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Price", "Funding rate zscores"))

    fig.append_trace(go.Scatter(x=df2.index, y=df2['PriceUSD'], mode='markers', showlegend=False,
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
    fig.update_layout(legend=dict(x=0.72, y=0.25))
    return fig
