
from dash import dcc, html, Input, Output, callback
from mplcursors import HoverMode
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


layout = html.Div(
    [
        html.H2('Bitcoin ROI As Measured From The Market Cycle Bottom'),
        html.Div(dbc.Spinner(size='lg', color='black', type='border'), id='btc_roi_cycle_bottom'),
        html.Hr(),
        html.Br(),
        html.Div(
            [
                


            ]
        )
    ]
)

@callback(
    Output('btc_roi_cycle_bottom', 'children'),
    Input('df-data', 'data'))
def monthly_roi(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    df = df[df['Value'] > 0]
    cycle1 = pd.date_range(df['Date'][2], '2011/11/18',freq='D') 
    cycle2 = pd.date_range('2011/11/18', '2015/1/14', freq='D')
    cycle3 = pd.date_range('2015/1/14', '2018/12/5', freq='D')
    cycle4 = pd.date_range('2018/12/5', df['Date'][-3], freq='D')
    
    df['Date-time-index'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date-time-index'])

    df['cycle1'] = df['Value'][cycle1].dropna().pct_change(1)*100
    df['cycle2'] = df['Value'][cycle2].dropna().pct_change(1)*100
    df['cycle3'] = df['Value'][cycle3].dropna().pct_change(1)*100
    df['cycle4'] = df['Value'][cycle4].dropna().pct_change(1)*100
    

    # df['cycle1avg'] = (df['cycle1'] - df['cycle1'].cummin()) / (df['cycle1'].cummax() - df['cycle1'].cummin())

    # df['cycle2avg'] = (df['cycle2'] - df['cycle2'].cummin()) / (df['cycle2'].cummax() - df['cycle2'].cummin())
    # df['cycle3avg'] = (df['cycle3'] - df['cycle3'].cummin()) / (df['cycle3'].cummax() - df['cycle3'].cummin())
    # df['cycle4avg'] = (df['cycle4'] - df['cycle4'].cummin()) / (df['cycle4'].cummax() - df['cycle4'].cummin())

    #### Plot
    fig = make_subplots()
    fig.add_trace(go.Scatter(y=df['cycle1'].cumsum().dropna(), name='cycle1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(y=df['cycle2'].cumsum().dropna(), name='cycle2', line=dict(color='orange')))
    fig.add_trace(go.Scatter(y=df['cycle3'].cumsum().dropna(), name='cycle3', line=dict(color='yellow')))
    fig.add_trace(go.Scatter(y=df['cycle4'].cumsum().dropna(), name='cycle4', line=dict(color='purple')))
    fig.update_xaxes(type='linear',range=[0,2000],title="Days Since Bottom")
    fig.update_yaxes(type='linear', title='ROI')
    fig.update_layout(template="plotly_dark")
    
    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
