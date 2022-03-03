import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import numpy as np
from datetime import date

layout = html.Div([
    html.H2('Cowen Corridor'),
    html.Div(dbc.Spinner(size='lg', color='black',
             type='border'), id='cowen-corridor-graph')
])

@callback(
    Output('cowen-corridor-graph', 'children'), Input('df-data', 'data'))
def cowen_corridor(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    dayssince = df['Date'][-1] - pd.to_datetime(date(2010, 7, 18))
    dti = pd.date_range(df['Date'][0], df['Date'][-3], freq="W")
    df['Date-time-index'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date-time-index'])

    x = pd.to_numeric(dayssince.days)
    pi = 3.1415926535
    df['CCy1'] = df['Value'].rolling(141).mean()*16*pi*pi/np.sqrt(x)
    df['CCy2'] = df['Value'].rolling(141).mean()/100*np.sqrt(x)
    df = df[df['CCy1'] > 1]

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['CCy1'], name='y1', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['CCy2'], name='y2' ,line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], name='Price', line=dict(color='gold')))
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Price", type='log')
    fig.update_layout(template="plotly_dark", title={'text': f"Current Range: ${round(df['CCy1'][-1])} - ${round(df['CCy2'][-1])}"})

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
