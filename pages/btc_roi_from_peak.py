
from dash import dcc, html, Input, Output, callback
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


layout = html.Div(
    [
        html.H2('Bitcoin ROI As Measured From Peak To Peak'),
        html.Div(dbc.Spinner(size='lg', color='black',
                             type='border'), id='btc_roi_from_peak'),
    ]
)
@callback(
    Output('btc_roi_from_peak', 'children'),
    Input('df-data', 'data'))
def btc_roi_from_peak(data):

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    peak1 = pd.date_range('2011/5/8', '2013/12/4', freq='D')
    peak2 = pd.date_range('2013/12/4', '2017/12/17', freq='D')
    peak3 = pd.date_range('2017/12/17', df['Date'][-3], freq='D')

    df['Date-time-index'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date-time-index'])

    df['peak1'] = df['Value'][peak1].dropna().pct_change(1)*100
    df['peak2'] = df['Value'][peak2].dropna().pct_change(1)*100
    df['peak3'] = df['Value'][peak3].dropna().pct_change(1)*100

    #### Plot
    fig = make_subplots()
    fig.add_trace(go.Scatter(y=df['peak1'].cumsum(
    ).dropna(), name='peak 1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(y=df['peak2'].cumsum(
    ).dropna(), name='peak 2', line=dict(color='orange')))
    fig.add_trace(go.Scatter(y=df['peak3'].cumsum(
    ).dropna(), name='peak 3', line=dict(color='yellow')))
    fig.update_xaxes(type='linear', range=[
        0, 2000], title="Days Since Last Peak")
    fig.update_yaxes(type='linear', title='ROI')
    fig.update_layout(template="plotly_dark")

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
