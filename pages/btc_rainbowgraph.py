from dash import dcc, html, Input, Output, callback
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


layout = html.Div([
    html.H2('Price Color Coded By Risk'),
    html.Div(dbc.Spinner(size='lg', color='black', type='border'), id='rainbow-graph'),
])

@callback(
    Output('rainbow-graph', 'children'),
    Input('df-data', 'data'))
def calc_rainbow_metric(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df = df[df['Value'] > 0]
    df.index = pd.to_numeric(df.index, errors='coerce')
    
    # Calculate the `Risk Metric`
    df['MA'] = df['Value'].rolling(374, min_periods=1).mean().dropna()
    df['Preavg'] = (np.log(df.Value) - np.log(df['MA'])) * df.index**.395

    # Normalization to 0-1 range
    df['avg'] = (df['Preavg'] - df['Preavg'].cummin()) / \
        (df['Preavg'].cummax() - df['Preavg'].cummin())

    df = df[df.index > 1000]
    fig = px.scatter(df, x='Date', y='Value', color='avg', color_continuous_scale='jet')
    fig.update_layout(template='plotly_dark')
    fig.update_yaxes(title='Price ($USD)', type='log', showgrid=False)

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})


