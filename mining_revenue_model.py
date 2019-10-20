import pandas as pd
import scipy.stats
import statsmodels.formula.api as smf
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def collect_mining_rev():
    try:
        mining_rev = pd.read_csv('data/Quandl/BCHAIN_MIREV.csv', index_col=False)
    except FileNotFoundError:    # filepath is different when deployed on Elastic Beanstalk
        mining_rev = pd.read_csv('/opt/python/current/app/data/Quandl/BCHAIN_MIREV.csv', index_col=False)
    return mining_rev


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


def mining_rev_price_time_series_model(coinmetrics_df, mining_rev):
    df = pd.merge(coinmetrics_df, mining_rev, left_index=True, right_index=True, how='inner')
    df = df.rename({"Value": "mining_rev"}, axis=1)
    df = df[['PriceUSD', 'mining_rev']]

    df['mining_365'] = df.mining_rev.rolling(365).mean()
    # Remove beginnning values to avoid using skewed values of mining_365
    df.drop(df.loc[:'2011-08-17'].index, inplace=True)
    df['mining_multiple'] = df.mining_rev / df.mining_365
    df['mining_m_zscore'] = (df.mining_multiple - df.mining_multiple.mean()) / df.mining_multiple.std(ddof=0)

    df['price_log'] = np.log(df['PriceUSD'])

    df['X'] = df.mining_rev.values.reshape(-1, 1)
    df['Y'] = df['PriceUSD'].values.reshape(-1, 1)
    df1 = df.dropna(axis=0)
    est = smf.ols(formula='Y ~ X', data=df1).fit()

    df1['price_pred'] = est.predict()
    df1['price_pred_dif'] = df1.price_pred - df1.Y
    df1['price_pred_dif_zscore'] = scipy.stats.zscore(df1.price_pred_dif)

    # Create figure with secondary y-axis
    fig = make_subplots()

    fig = fig.add_trace(go.Scatter(x=df1.index, y=df1['PriceUSD'], mode='lines+markers', name='price_pred_dif_zscore',
                                   marker=dict(size=5,
                                               color=df1['price_pred_dif_zscore'],  # set color equal to a variable
                                               colorscale='viridis',  # one of plotly colorscales
                                               colorbar=dict(title='price_pred_dif_zscore', titleside="right"),
                                               showscale=True)))

    fig = fig.add_trace(go.Scatter(x=df1.index, y=df1['PriceUSD'], mode='lines+markers', name='mining_multiple_z_score',
                                   marker=dict(size=5,
                                               color=df1['mining_m_zscore'],
                                               colorscale='rainbow',  # one of plotly colorscales
                                               colorbar=dict(x=1.12, title='mining_multiple_z_score',
                                                             titleside="right"),
                                               showscale=True)))

    fig.add_trace(go.Scatter(x=df1.index,
                             y=df1['price_pred'],
                             name='price_pred',
                             mode='lines',
                             ))

    fig.update_layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Time", font=dict(size=14))),
                      yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Price", font=dict(size=14))),
                      legend=dict(x=0.72, y=0.05))
    fig.update_yaxes(type='log')
    return fig
