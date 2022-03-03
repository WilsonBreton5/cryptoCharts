from dash import dcc, html, Input, Output, callback
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


layout = html.Div(
    [
        html.H2('Bitcoin ROI As Measured From The Halving'),
        html.Div(dbc.Spinner(size='lg', color='black',
                             type='border'), id='btc_roi_from_halving'),
    ]
)


@callback(
    Output('btc_roi_from_halving', 'children'),
    Input('df-data', 'data'))
def monthly_roi(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    df = df[df['Value'] > 0]
    halving1 = pd.date_range(df['Date'][2], '2012/11/28', freq='D')
    halving2 = pd.date_range('2012/11/28', '2016/6/9', freq='D')
    halving3 = pd.date_range('2016/6/9', '2020/4/11', freq='D')
    halving4 = pd.date_range('2020/4/11', df['Date'][-3], freq='D')

    df['Date-time-index'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date-time-index'])

    df['halving1'] = df['Value'][halving1].dropna().pct_change(1)*100
    df['halving2'] = df['Value'][halving2].dropna().pct_change(1)*100
    df['halving3'] = df['Value'][halving3].dropna().pct_change(1)*100
    df['halving4'] = df['Value'][halving4].dropna().pct_change(1)*100

    # df['cycle1avg'] = (df['cycle1'] - df['cycle1'].cummin()) / (df['cycle1'].cummax() - df['cycle1'].cummin())

    # df['cycle2avg'] = (df['cycle2'] - df['cycle2'].cummin()) / (df['cycle2'].cummax() - df['cycle2'].cummin())
    # df['cycle3avg'] = (df['cycle3'] - df['cycle3'].cummin()) / (df['cycle3'].cummax() - df['cycle3'].cummin())
    # df['cycle4avg'] = (df['cycle4'] - df['cycle4'].cummin()) / (df['cycle4'].cummax() - df['cycle4'].cummin())

    #### Plot
    fig = make_subplots()
    fig.add_trace(go.Scatter(y=df['halving1'].cumsum(
    ).dropna(), name='halving 1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(y=df['halving2'].cumsum(
    ).dropna(), name='halving 2', line=dict(color='orange')))
    fig.add_trace(go.Scatter(y=df['halving3'].cumsum(
    ).dropna(), name='halving 3', line=dict(color='yellow')))
    fig.add_trace(go.Scatter(y=df['halving4'].cumsum(
    ).dropna(), name='halving 4', line=dict(color='purple')))
    fig.update_xaxes(type='linear', range=[0, 2000], title="Days Since Last Halving")
    fig.update_yaxes(type='linear', title='ROI')
    fig.update_layout(template="plotly_dark")

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
