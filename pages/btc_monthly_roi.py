from dash import dcc, html, Input, Output, callback
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_pivottable as dp



layout = html.Div(
    [
        html.H2('Monthly ROI with Price Overlayed'),
        html.Div(dbc.Spinner(size='lg', color='black',
                             type='border'), id='monthly_roi'),
    ]
)

@callback(
    Output('monthly_roi', 'children'),
    Input('df-data', 'data'))
def monthly_roi(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df[df['Value'] > 0]
    
    df['monthly-roi'] = df['Value'].pct_change(30)*100
    df['Date-time-index'] = pd.to_datetime(df['Date'])
    df = df.set_index(['Date-time-index'])
    dti = pd.date_range(df['Date'][0], df['Date'][-1], freq="M")
    

    #### Plot
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Value'], name='Price', line=dict(
        color='gold')), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['monthly-roi'], name='30 Day ROI', line=dict(color='red')))
    fig.update_xaxes(title="Date")
    fig.update_yaxes(type='linear', title='30day ROI')
    fig.update_yaxes(title='Price ($USD)', type='log',
                    showgrid=False, secondary_y=True)
    fig.update_layout(template="plotly_dark", title={})

    
    
    
    


    

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})




