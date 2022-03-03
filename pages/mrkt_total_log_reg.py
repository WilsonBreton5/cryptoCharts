from dash import dcc, html, Input, Output, callback
import matplotlib
from matplotlib.pyplot import plot
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import mplcursors as mplcursors
import numpy as np
from scipy.optimize import curve_fit
from sklearn import linear_model


layout = html.Div(
    [
        html.Div(dbc.Spinner(size='lg', color='black',
                             type='border'), id='mrkt-total-log-reg'),
    ]
)


@callback(
    Output('mrkt-total-log-reg', 'children'),
    Input('mrkt_df-data', 'data'))
def calc_mrkt_fair_value(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)
    
    
    df.index = pd.to_numeric(df.index, errors='coerce')
    df = df.iloc[365:]
    print(df)

    def LinearReg(ind, value):
        X = np.array(np.log(ind)).reshape(-1, 1)
        y = np.array(np.log(value))
        ransac = linear_model.RANSACRegressor(
            residual_threshold=2.989, random_state=1)
        ransac.fit(X, y)
        LinearRegRANSAC = ransac.predict(X)
        return LinearRegRANSAC
    
    

    df["LinearRegRANSAC"] = LinearReg(df.index, df.market_cap)
    
    #### Plot
    fig = make_subplots()
    fig.add_trace(go.Scatter(
    x=df["timestamp"], y=df["market_cap"], name="Price", line=dict(color="gold")))
    fig.add_trace(go.Scatter(x=df["timestamp"], y=np.exp(
    df["LinearRegRANSAC"]), name="Fair Value", line=dict(color="green")))
    fig.update_layout(template="plotly_dark", title={
                    'text': f"Fair Value: ${round(np.exp(df['LinearRegRANSAC'].iloc[-1]))}"})
    mplcursors.cursor(hover=True)
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Price", type='log', showgrid=True)

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
