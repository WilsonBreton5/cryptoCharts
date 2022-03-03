from dash import dcc, html, Input, Output, callback
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import mplcursors as mplcursors
import numpy as np
from sklearn import linear_model





layout = html.Div(
    [
        html.H2('Bitcoin Fair Value Logarithmic Regression'),
        html.Div(dbc.Spinner(size='lg', color='black',
             type='border'), id='fair-value-graph'),
    ]
)

@callback(
    Output('fair-value-graph', 'children'),
    Input('df-data', 'data'))
def calc_fair_value(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df = df[df['Value'] > 0]
    df.index = pd.to_numeric(df.index, errors='coerce')
    
    
    def LinearReg(ind, value):
        X = np.array(np.log(ind)).reshape(-1, 1)
        y = np.array(np.log(value))
        ransac = linear_model.RANSACRegressor(
            residual_threshold=2.989, random_state=0)
        ransac.fit(X, y)
        LinearRegRANSAC = ransac.predict(X)
        return LinearRegRANSAC

    df["LinearRegRANSAC"] = LinearReg(df.index, df.Value)

    #### Plot
    fig = make_subplots()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], name="Price", line=dict(color="gold")))
    fig.add_trace(go.Scatter(x=df["Date"], y=np.exp(df["LinearRegRANSAC"]), name="Fair Value", line=dict(color="green")))
    fig.update_layout(template="plotly_dark", title={'text': f"Fair Value: ${round(np.exp(df['LinearRegRANSAC'].iloc[-1]))}"})
    mplcursors.cursor(hover=True)
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Price", type='log', showgrid=True)

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
