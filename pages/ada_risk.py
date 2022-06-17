
from datetime import date
import warnings
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2('ADA Risk'),
    html.Div(dbc.Spinner(size='lg', color='black',
             type='border'), id='ada-risk-graph')
])


@callback(
    Output('ada-risk-graph', 'children'), Input('ada-data', 'data'))

def ada_risk(data):
    df = yf.download(tickers='ADA-USD',
                    period="max").reset_index()[["Date", "Close"]]
    df = df.rename(columns={'Close': 'Value'})
    df = df[df["Value"] > 0]
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True)


   


    def normalization(data):
        normalized = (data - data.min()) / (data.max() - data.min())
        return normalized


 


    ############## 4yrMA ###############################
    df["4yrMA"] = (df["Value"] - df["Value"].expanding().mean()) / \
        df["Value"].expanding().std()
    df["4yrMA"] = normalization(df["4yrMA"])

    ############## Mayer Multiple ###############################
    df["Mayer"] = df["Value"] / df["Value"].rolling(200).mean()
    df["Mayer"] = normalization(df["Mayer"])

    ############### Price/50W MA ########################################
    df["Price/50w"] = df["Value"] / df["Value"].ewm(span=365).mean()
    df["Price/50w"] = normalization(df["Price/50w"])

    ############## Sharpe Ratio ######################################
    df["Return%"] = df["Value"].pct_change() * 100
    df["Sharpe"] = (df["Return%"].rolling(365).mean() - 1) / \
        df["Return%"].rolling(365).std()
    df["Sharpe"] = normalization(df["Sharpe"])

    ############# Sortino #############################################
    dfs = df[df["Return%"] < 0]
    df["Sortino"] = (df["Return%"].rolling(365).mean() - 1) / \
        dfs["Return%"].rolling(365).std()
    df["Sortino"] = normalization(df["Sortino"])

    #################### avg ################################
    df["avg"] = df[["Price/50w", "Sharpe", "Mayer", "4yrMA"]].mean(axis=1)

    #################### Plot ################################
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    xaxis = df.Date

    fig.add_trace(go.Scatter(x=xaxis, y=df.Value, name="Price",
                line=dict(color="gold")), secondary_y=False)
    fig.add_trace(go.Scatter(x=xaxis, y=df["avg"], name="Risk", mode="lines", line=dict(
        color="white")), secondary_y=True)

    fig.add_hrect(y0=0.4, y1=0.3, line_width=0, fillcolor="green",
                opacity=0.2, secondary_y=True)
    fig.add_hrect(y0=0.3, y1=0.2, line_width=0, fillcolor="green",
                opacity=0.3, secondary_y=True)
    fig.add_hrect(y0=0.2, y1=0.1, line_width=0, fillcolor="green",
                opacity=0.4, secondary_y=True)
    fig.add_hrect(y0=0.1, y1=0, line_width=0, fillcolor="green",
                opacity=0.5, secondary_y=True)
    fig.add_hrect(y0=0.6, y1=0.7, line_width=0, fillcolor="red",
                opacity=0.3, secondary_y=True)
    fig.add_hrect(y0=0.7, y1=0.8, line_width=0, fillcolor="red",
                opacity=0.4, secondary_y=True)
    fig.add_hrect(y0=0.8, y1=0.9, line_width=0, fillcolor="red",
                opacity=0.5, secondary_y=True)
    fig.add_hrect(y0=0.9, y1=1.0, line_width=0, fillcolor="red",
                opacity=0.6, secondary_y=True)
    fig.update_layout(xaxis_title='Date', yaxis_title='Price',
                    yaxis2_title='Risk',
                    yaxis1=dict(type='log', showgrid=False),
                    yaxis2=dict(showgrid=True, tickmode='linear',
                                tick0=0.0, dtick=0.1),
                    template="plotly_dark")
    


   

    warnings.filterwarnings('ignore')

    df = yf.download(tickers='ADA-USD',
                    period="max").reset_index()[["Date", "Close"]]
    df = df.rename(columns={'Close': 'Value'})
    df = df[df["Value"] > 0]
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True)


    def normalization(data):
        normalized = (data - data.cummin()) / (data.cummax() - data.cummin())
        return normalized


    ############## 400MA ########################################
    df['400MA'] = 0
    for i in range(0, df.shape[0]):
        df['400MA'][i] = df['Value'][0 if i <
                                    400 else (i - 400): i].dropna().mean()

    df['400MArisk'] = 0
    for i in range(0, df.shape[0]):
        df['400MArisk'][i] = (df['Value'][i] / df['400MA'][i])

    ############## Mayer Multiple ########################################
    df['200MA'] = 0
    for i in range(0, df.shape[0]):
        df['200MA'][i] = df['Value'][0 if i <
                                    200 else (i - 200): i].dropna().mean()

    df['Mayer'] = 0
    for i in range(0, df.shape[0]):
        df['Mayer'][i] = (df['Value'][i] / df['200MA'][i])

    ############### Price/52W MA ########################################
    df["365MA"] = 0
    for i in range(0, df.shape[0]):
        df["365MA"][i] = df["Value"][0 if i <
                                    365 else (i - 365): i].dropna().mean()

    df["Price/52w"] = 0
    for i in range(0, df.shape[0]):
        df["Price/52w"][i] = (df["Value"][i] / df["365MA"][i])

    ############## Sharpe Ratio ########################################
    df["Return%"] = df["Value"].pct_change() * 100

    df["365Return%MA-1"] = 0
    for i in range(0, df.shape[0]):
        df["365Return%MA-1"][i] = df["Return%"][0 if i <
                                                365 else (i - 365): i].dropna().mean() - 1

    df["365Return%STD"] = 0
    for i in range(0, df.shape[0]):
        df["365Return%STD"][i] = df["Return%"][0 if i <
                                            365 else (i - 365): i].dropna().std()

    df["Sharpe"] = 0
    for i in range(0, df.shape[0]):
        df["Sharpe"][i] = (df["365Return%MA-1"][i] / df["365Return%STD"][i])

    #################### avg ################################
    indicators = ["Mayer", "Price/52w", "Sharpe", "400MArisk"]

    for item in indicators:
        df[item].update(normalization(df[item]))

    df["avg"] = df[['Mayer', 'Sharpe', '400MArisk', "Price/52w"]].mean(axis=1)
    df["avg"] = (df["avg"] - df["avg"].cummin()) / \
        (df["avg"].cummax() - df["avg"].cummin())

    #################### Plot ################################
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    xaxis = df.Date

    fig2.add_trace(go.Scatter(x=xaxis, y=df.Value, name="Price",
                line=dict(color="gold")), secondary_y=False)
    fig2.add_trace(go.Scatter(x=xaxis, y=df["avg"], name="Risk", line=dict(
        color="white")), secondary_y=True)

    fig2.add_hrect(y0=0.5, y1=0.4, line_width=0, fillcolor="green",
                opacity=0.2, secondary_y=True)
    fig2.add_hrect(y0=0.4, y1=0.3, line_width=0, fillcolor="green",
                opacity=0.3, secondary_y=True)
    fig2.add_hrect(y0=0.3, y1=0.2, line_width=0, fillcolor="green",
                opacity=0.4, secondary_y=True)
    fig2.add_hrect(y0=0.2, y1=0.1, line_width=0, fillcolor="green",
                opacity=0.5, secondary_y=True)
    fig2.add_hrect(y0=0.1, y1=0.0, line_width=0, fillcolor="green",
                opacity=0.6, secondary_y=True)
    fig2.add_hrect(y0=0.6, y1=0.7, line_width=0, fillcolor="red",
                opacity=0.3, secondary_y=True)
    fig2.add_hrect(y0=0.7, y1=0.8, line_width=0, fillcolor="red",
                opacity=0.4, secondary_y=True)
    fig2.add_hrect(y0=0.8, y1=0.9, line_width=0, fillcolor="red",
                opacity=0.5, secondary_y=True)
    fig2.add_hrect(y0=0.9, y1=1.0, line_width=0, fillcolor="red",
                opacity=0.6, secondary_y=True)
    fig2.update_xaxes(title="Date")
    fig2.update_yaxes(title="Price", type='log', showgrid=False)
    fig2.update_yaxes(title="Risk", type='linear', showgrid=True,
                    tickmode='array', tick0=0.0, dtick=0.1, secondary_y=True)
    fig2.update_layout(template="plotly_dark")


    return dcc.Graph(figure=fig, responsive=True, style={'height': '90vh'}), dcc.Graph(figure=fig2, responsive=True, style={'height': '90vh'})
    