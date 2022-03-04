from cmath import exp
from tkinter import VERTICAL
from turtle import width
import urllib.request
from dash import Dash, dcc, html, Input, Output, callback, State
import numpy as np
from pages import mrkt_total_log_reg, btc_log_reg,btc_roi_from_peak, btc_roi_from_halving, btc_roi_cycle_bottom, btc_monthly_roi, btc_cowen_corridor, btc_fair_value, btc_rainbowgraph, btc_risk, btc_riskpricechart, btc_fear_greed, btc_roi_from_halving
from datetime import date
import pandas as pd
import quandl
import yfinance as yf
import dash_bootstrap_components as dbc
import requests 


# Fear & Greed Data
r = requests.get(
    'https://api.alternative.me/fng/?limit=0&format=json&date_format=us')
data = r.json()
fng_df = pd.DataFrame(data["data"])

# Download historical data from Quandl
df = quandl.get('BCHAIN/MKPRU', api_key='FYzyusVT61Y4w65nFESX').reset_index()


#url = "https://api.nomics.com/v1/market-cap/history?key=45a204e26b47d3efe8fb2d3d64b60e4ff33736f9&start=2010-04-14T00%3A00%3A00Z&end=2022-05-14T00%3A00%3A00Z"
#mrkt_df = pd.read_json(url)



# Sort data by date, just in case
df.sort_values(by='Date', inplace=True)

# Get the last price against USD
btcdata = yf.download(tickers='BTC-USD', period='1d', interval='1m')

# Append the latest price data to the dataframe
df.loc[df.index[-1]+1] = [date.today(), btcdata['Close'].iloc[-1]]
# Calculate the `Risk Metric`

df = df[df['Value'] > 0]

df['MA'] = df['Value'].rolling(374, min_periods=1).mean().dropna()
df['Preavg'] = (np.log(df.Value) - np.log(df['MA'])) * df.index**.395

# Normalization to 0-1 range
df['avg'] = (df['Preavg'] - df['Preavg'].cummin()) / (df['Preavg'].cummax() - df['Preavg'].cummin())




app = Dash(__name__, suppress_callback_exceptions=True, 
           external_stylesheets=[dbc.themes.CYBORG], meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1"},
           ],)
server = app.server


navbar2 = dbc.Container(
    dbc.Navbar(
        [
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                [

                    # html.H5('Total Crypto Market Charts'),
                    # dbc.NavItem(dbc.NavLink("Total Market Cap Logarithmic Regression",
                    #                         active="exact", href="/")),
                    html.H5('Bitcoin Charts'),
                    dbc.NavItem(dbc.NavLink("Risk Metric",
                                            active="exact", href="/btc_risk")),
                    dbc.NavItem(dbc.NavLink("Price Color Coded by Risk",
                                            active="exact", href="/btc_rainbowgraph")),
                    dbc.NavItem(dbc.NavLink("Price/Risk Chart",
                                            active="exact", href="/btc_riskpricechart")),
                    dbc.NavItem(dbc.NavLink("BTC Fair Value",
                                            active="exact", href="/btc_fair_value")),
                    dbc.NavItem(dbc.NavLink("BTC Fear & Greed Index",
                                            active="exact", href="/btc_fear_greed")),
                    dbc.NavItem(dbc.NavLink("BTC Cowen Corridor",
                                            active="exact", href="/btc_cowen_corridor")),
                    # dbc.NavItem(dbc.NavLink("BTC Logarithmic Regression",
                    #                        active="exact", href="/btc_log_reg")),

                    html.H5('Bitcoin ROI Charts'),
                    dbc.NavItem(dbc.NavLink("BTC ROI From Market Cycle Bottom",
                                            active="exact", href="/btc_from_cycle_bottom")),
                    dbc.NavItem(dbc.NavLink("BTC ROI From Halving",
                                            active="exact", href="/btc_from_halving")),
                    dbc.NavItem(dbc.NavLink("BTC ROI From Peak To Peak",
                                            active="exact", href="/btc_from_peak")),
                    dbc.NavItem(dbc.NavLink("BTC Monthly Returns",
                                            active="exact", href="/btc_monthly_roi")),

                    # html.H5('Ethereum Charts'),
                    # dbc.NavItem(dbc.NavLink("ETH Logarithmic Regression",
                    #                         active="exact", href="/eth_log_reg")),
                    # dbc.NavItem(dbc.NavLink("ETH Logarithmic Regression Rainbow",
                    #                         active="exact", href="/eth_log_rainbow")),
            
                    
                    # html.H5('Ethereum ROI Charts'),
                    # dbc.NavItem(dbc.NavLink("ETH ROI From Market Cycle Bottom",
                    #                         active="exact", href="/eth_from_cycle_bottom")),
                    # dbc.NavItem(dbc.NavLink("ETH Sub-Cycle ROI",
                    #                         active="exact", href="/eth_subcycle_roi")),
                    # #dbc.NavItem(dbc.NavLink("ETH Running ROI",
                    #  #                       active="exact", href="/btc_from_peak")),
                    # dbc.NavItem(dbc.NavLink("ETH Monthly ROI",
                    #                         active="exact", href="/eth_monthly_roi")),

                    


                ], 
                pills=True,
                vertical="sm",
                
                

                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                style={'align-items': 'start'},

                
                
            ),
            
                
        ],
        expand='xl',
        color="dark",
        dark=True,
    
    ),
    
    class_name='col-xl-2 d-flex',
   
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



header = dbc.Container(
    [
        dbc.Row(
            [ 
                dbc.Col(
                    html.H5(
                        f"Risk level: {round(df['avg'].iloc[-1], 2)}", style={'color': 'red'}),
                ),
                dbc.Col(
                    html.H5(f"Price: ${round(btcdata['Close'][-1])} USD",style={'color': 'green'}),
                ),
                dbc.Col(
                    html.H5(f"Fear & Greed: {fng_df['value'][0]}", style={'color':'blue'}),
                ),
                dbc.Col(
                    html.P(f"Updated: {btcdata.index[-1]}"),
                )
            ]
            
        ),
    ]
)

page_content = dbc.Container(
    dbc.Col(
        dbc.Row(
            html.Div(id='page-content', className='col pt-4'
            ),

            class_name='overflow-auto'
        )
       
    ), 
    class_name='col d-flex flex-column h-sm-100'
)
# Convert to dictionary to store in memory
df = df.to_dict()
fng_df = fng_df.to_dict()
#mrkt_df = mrkt_df.to_dict()

app.layout = html.Div(
    [
        dcc.Store(id="df-data", data=df),
        dcc.Store(id="fng-data", data=fng_df),
        #dcc.Store(id="mrkt_df-data", data=mrkt_df),
    
        dcc.Location(id='url', refresh=False),
        
        dbc.Container(
            [
                header,
                dbc.Row(
                    [   
                        navbar2,
                        page_content
                    ], 
                    class_name='vh-100 overflow-auto'
                ),
                #footer
            ], fluid=True, class_name='overflow-hidden'

        ),
    ], 
)

# we use a callback to toggle the collapse on small screens



@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/btc_risk':
        return btc_risk.layout
    elif pathname == '/btc_rainbowgraph':
        return btc_rainbowgraph.layout
    elif pathname == '/btc_riskpricechart':
        return btc_riskpricechart.layout
    elif pathname == '/btc_fair_value':
        return btc_fair_value.layout
    elif pathname == '/btc_fear_greed':
        return btc_fear_greed.layout
    elif pathname == '/btc_cowen_corridor':
        return btc_cowen_corridor.layout
    elif pathname == '/btc_monthly_roi':
        return btc_monthly_roi.layout
    elif pathname == '/btc_from_cycle_bottom':
        return btc_roi_cycle_bottom.layout
    elif pathname == '/btc_from_halving':
        return btc_roi_from_halving.layout
    elif pathname == '/btc_from_peak':
        return btc_roi_from_peak.layout
    elif pathname == '/btc_log_reg':
        return btc_log_reg.layout
    elif pathname == '/mrkt_total_log_reg':
        return mrkt_total_log_reg.layout

    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
