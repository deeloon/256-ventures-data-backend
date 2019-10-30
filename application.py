import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from s2f_model import s2f_generation_halved_time_series_model, collect_coinmetrics, collect_blockchair
from mining_revenue_model import mining_rev_price_time_series_model, collect_mining_rev
from funding_rates_model import collect_funding, funding_rate_time_series_model
from OI_and_OV_plot import collect_OI_OV, plot_open_interest, update_OI_OV


blockchair_df, coinmetrics_df, mining_rev, funding_rates_df = collect_blockchair(), collect_coinmetrics(), \
                                                              collect_mining_rev(), collect_funding(),
OI_OV_df = collect_OI_OV()

s2f_fig = s2f_generation_halved_time_series_model(blockchair_df, coinmetrics_df, 'D')
mining_fig = mining_rev_price_time_series_model(coinmetrics_df, mining_rev)
funding_fig = funding_rate_time_series_model(coinmetrics_df, funding_rates_df, 'D')
OI_OV_fig = plot_open_interest(OI_OV_df, coinmetrics_df)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.scripts.config.serve_locally = True

app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='s2f model', value='tab-1', children=[
            html.Div([html.H3('S2F Model'),
                      dcc.Graph(id='s2f-graph', figure=s2f_fig)])]),
        dcc.Tab(label='mining revenue model', value='tab-2', children=[
            html.Div([html.H3('Mining Revenue Model'),
                      dcc.Graph(id='mining-graph', figure=mining_fig)])]),
        dcc.Tab(label='funding rates model', value='tab-3', children=[
            html.Div([html.H3('Funding Rates Model'),
                      dcc.Graph(id='funding-graph', figure=funding_fig)])]),
        dcc.Tab(label='OI OV plot', value='tab-4', children=[
            html.Div([html.H3('OI OV Plot'),
                      dcc.Graph(id='oi-ov-graph', figure=OI_OV_fig)])]),
              ]),
    dcc.Interval(
        id='interval-component',
        interval=1000 * 60 * 60,    #* 24,    # in milliseconds
        n_intervals=0
    )
], style={'font-family': 'Verdana'})

application = app.server


@app.callback([Output('s2f-graph', 'figure'), Output('mining-graph', 'figure'),
               Output('funding-graph', 'figure'), Output('oi-ov-graph', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    blockchair_df, coinmetrics_df, mining_rev, funding_rates_df = collect_blockchair(), collect_coinmetrics(), \
                                                                  collect_mining_rev(), collect_funding(),
    update_OI_OV()
    OI_OV_df = collect_OI_OV()
    s2f_fig = s2f_generation_halved_time_series_model(blockchair_df, coinmetrics_df, 'D')
    mining_fig = mining_rev_price_time_series_model(coinmetrics_df, mining_rev)
    funding_fig = funding_rate_time_series_model(coinmetrics_df, funding_rates_df, 'D')
    OI_OV_fig = plot_open_interest(OI_OV_df, coinmetrics_df)
    return s2f_fig, mining_fig, funding_fig, OI_OV_fig


if __name__ == '__main__':
    application.run(debug=True)
