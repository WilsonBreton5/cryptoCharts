from dash import dcc, html, Input, Output, callback
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc



layout = html.Div([
    html.H2('Bitcoin Risk Metric'),
    html.Div(dbc.Spinner(size='lg', color='black', type='border'), id='risk-graph'), 
])

@callback(Output('risk-graph', 'children'),Input('df-data', 'data'))
def calc_risk_metric(data):
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
    
    
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'],
                                    name='Price', line=dict(color='gold')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['avg'],   name='Risk',  line=dict(
        color='white')), secondary_y=True)

    # Add green (`accumulation` or `buy`) rectangles to the figure
    opacity = 0.2
    for i in range(5, 0, -1):
        opacity += 0.05
        fig.add_hrect(y0=i*0.1, y1=((i-1)*0.1), line_width=0,
                            fillcolor='green', opacity=opacity, secondary_y=True)

    # Add red (`distribution` or `sell`) rectangles to the figure
    opacity = 0.2
    for i in range(6, 10):
        opacity += 0.1
        fig.add_hrect(y0=i*0.1, y1=((i+1)*0.1), line_width=0,
                            fillcolor='red', opacity=opacity, secondary_y=True)

    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Price ($USD)',
    type='log', showgrid=False,)
    fig.update_yaxes(title='Risk', type='linear', secondary_y=True,
                            showgrid=True, tick0=0.0, dtick=0.1, range=[0, 1],)
    fig.update_layout(template='plotly_dark')

    return dcc.Graph(figure=fig, responsive=True, style={ 'height': '90vh'})
