import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import zscore
import requests

def collect_coinmetrics():
    # Get Price Data
    metrics = 'PriceUSD'
    r = requests.get('https://community-api.coinmetrics.io/v2/assets/btc/metricdata?metrics=' + metrics)
    r.raise_for_status()
    json = r.json()
    coinmetrics_df = pd.DataFrame(json['metricData']['series'], columns=['time', 'PriceUSD'])
    coinmetrics_df.time = pd.to_datetime(coinmetrics_df.time, dayfirst=True)
    coinmetrics_df.index = coinmetrics_df.time
    coinmetrics_df.index = coinmetrics_df.index.tz_localize(None)
    return coinmetrics_df


def collect_funding():
    def update_bitmex(params_dict={'symbol': 'XBTUSD', 'count': '100', 'reverse': 'false', 'start': '0'}):
        # Update data from timestamp of last entry in file
        api_call_url = 'https://www.bitmex.com/api/v1/funding?_format=csv'

        try:
            filepath = 'data/Bitmex/funding.csv'
            with open(filepath, 'r'):
                pass
        except FileNotFoundError:
            filepath = '/opt/python/current/app/data/Bitmex/funding.csv'

        # Check if any parameters are applied
        if bool(params_dict):
            # Check for timestamp of last entry
            timestamp_df = pd.read_csv(filepath, usecols=['timestamp'])

            params_dict['startTime'] = timestamp_df.values[-1][0]
            params_dict['start'] = '1'

            for param in params_dict:
                api_call_url += '&' + param + '=' + params_dict[param]

        r = requests.get(api_call_url)
        if r.status_code != 200:
            r.raise_for_status()

        csv_list = r.text.split('\n')
        with open(filepath, 'a') as csv_file:
            # Append the data, but skip the headers
            for row in csv_list[1:]:
                csv_file.write('\n' + row)

    update_bitmex()

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
