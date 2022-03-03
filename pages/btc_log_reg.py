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


layout = html.Div(
    [
        html.Div(dbc.Spinner(size='lg', color='black',
                             type='border'), id='btc-log-reg'),
    ]
)

@callback(
    Output('btc-log-reg', 'children'),
    Input('df-data', 'data'))
def calc_fair_value(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df = df[df['Value'] > 0]
    df.index = pd.to_numeric(df.index, errors='coerce')

    def func(x,p1,p2):
        return p1*np.log(x) + p2

    ydata = np.log(df['Value'])
    xdata = [x+1 for x in pd.date_range(df['Date'][0],df['Date'][-3])]

    popt, pcov = curve_fit(func, xdata, ydata, p0=(3.0,-10))

    print(popt)

    fittedYdata = func(np.array([x+1 for x in range(len(df))]), popt[0], popt[1])

    #### Plot
    fig, ax = plot.subplots()
    ax.semilogy(df['Date'], df['Value'])
    plot.yscale('log',subsy=[1])
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())


    ax.yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
    plot.plot(df["Date"], np.exp(fittedYdata))  # exponentiate the data

    plot.title("BTC logarithmic regression")
    plot.ylabel("Price in USD")
    plot.ylim(bottom=0.1)
    plot.show()

    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'})
