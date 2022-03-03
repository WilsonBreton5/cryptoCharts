import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc



layout = html.Div([
    html.H2('Price According To Specific Risk'),
    html.Div(dbc.Spinner(size='lg', color='black', type='border'), id='risk-per-price-graph')
])

@callback(Output('risk-per-price-graph', 'children'), Input('df-data', 'data'))
def calc_price_per_risk(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df = df[df['Value'] > 0]
    df.index = pd.to_numeric(df.index, errors='coerce')
    df = df[df.index > 1000]
    # Calculate the `Risk Metric`
    df['MA'] = df['Value'].rolling(374, min_periods=1).mean().dropna()
    df['Preavg'] = (np.log(df.Value) - np.log(df['MA'])) * df.index**.395

    # Normalization to 0-1 range
    df['avg'] = (df['Preavg'] - df['Preavg'].cummin()) / \
        (df['Preavg'].cummax() - df['Preavg'].cummin())

    price_per_risk = {
        round(risk, 1): round(np.exp(
            (risk * (df['Preavg'].cummax().iloc[-1] - (cummin := df['Preavg'].cummin().iloc[-1]) ) + cummin) / df.index[-1]**.395 + np.log(df['MA'].iloc[-1])
        ))
        for risk in np.arange(0.0, 1.1, 0.1)
    }
   # Plot Predicting BTC price according to specific risk
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Risk', 'Price'],
                    align='center'),
        cells=dict(values=[list(price_per_risk.keys()), list(price_per_risk.values())],
                align='center'))
    ])
    fig.update_layout(template='plotly_dark')

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
