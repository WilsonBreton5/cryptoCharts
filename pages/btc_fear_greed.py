from re import X
from turtle import color
from unicodedata import name
from dash import dcc, html, Input, Output, callback
from matplotlib.pyplot import title
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import mplcursors as mplcursors
import numpy as np
from pyparsing import line


layout = html.Div(
    [   html.H2('Fear & Greed Index'),
        html.Div(dbc.Spinner(size='lg', color='black', type='border'), id='fng-graph'),
        html.Br(),
        html.Div(
            [
                html.H2("Data Sources"),
                html.Hr(),
                html.P('We are gathering data from the five following sources. Each data point is valued the same as the day before in order to visualize a meaningful progress in sentiment change of the crypto market. First of all, the current index is for bitcoin only(we offer separate indices for large alt coins soon), because a big part of it is the volatility of the coin price. But lets list all the different factors were including in the current index:'),
                html.H5('Volatility (25%)'),
                html.P('Were measuring the current volatility and max. drawdowns of bitcoin and compare it with the corresponding average values of the last 30 days and 90 days. We argue that an unusual rise in volatility is a sign of a fearful market.'),
                html.H5('Market Momentum/Volume (25%)'),
                html.P('Also, were measuring the current volume and market momentum(again in comparison with the last 30/90 day average values) and put those two values together. Generally, when we see high buying volumes in a positive market on a daily basis, we conclude that the market acts overly greedy / too bullish.'),
                html.H5('Social Media (15%)'),
                html.P('While our reddit sentiment analysis is still not in the live index(were still experimenting some market-related key words in the text processing algorithm), our twitter analysis is running. There, we gather and count posts on various hashtags for each coin(publicly, we show only those for Bitcoin) and check how fast and how many interactions they receive in certain time frames). A unusual high interaction rate results in a grown public interest in the coin and in our eyes, corresponds to a greedy market behaviour.'),
                html.H5('Dominance (10%)'),
                html.P('The dominance of a coin resembles the market cap share of the whole crypto market. Especially for Bitcoin, we think that a rise in Bitcoin dominance is caused by a fear of (and thus a reduction of) too speculative alt-coin investments, since Bitcoin is becoming more and more the safe haven of crypto. On the other side, when Bitcoin dominance shrinks, people are getting more greedy by investing in more risky alt-coins, dreaming of their chance in next big bull run. Anyhow, analyzing the dominance for a coin other than Bitcoin, you could argue the other way round, since more interest in an alt-coin may conclude a bullish/greedy behaviour for that specific coin.'),
                html.H5('Trends (10%)'),
                html.P('We pull Google Trends data for various Bitcoin related search queries and crunch those numbers, especially the change of search volumes as well as recommended other currently popular searches. For example, if you check Google Trends for "Bitcoin", you cant get much information from the search volume. But currently, you can see that there is currently a (+1,550%) rise of the query „bitcoin price manipulation“ in the box of related search queries (as of 05/29/2018). This is clearly a sign of fear in the market, and we use that for our index.'),


            ],
        ),
            
    ],
)

@callback(
    Output('fng-graph', 'children'),
    Input('fng-data', 'data'))

def fear_greed(data):
    fng_df = pd.DataFrame(data)
    fng_df['timestamp'] = pd.to_datetime(fng_df['timestamp'])
    fng_df.sort_values(by='timestamp', inplace=True)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=fng_df['timestamp'], y=fng_df['value'], name='Fear & Greed', line=dict(color='gold')))
    fig.update_layout(template="plotly_dark", title={'text':f"Current Value: {fng_df['value'][-1]}"})
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Fear & Greed Index", type='linear')

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})

    

