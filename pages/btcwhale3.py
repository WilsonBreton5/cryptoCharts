

from numpy import NaN
import pandas as pd


import yfinance as yf
import requests

import plotly.graph_objects as go
from plotly.subplots import make_subplots

url = 'https://bitinfocharts.com/bitcoin/address/3EKWP3ZviLXudcoAfzammYQKwaz2zJKwQW-full'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)
btcdata = yf.download(tickers='BTC-USD', period='max', interval='1d')


df = pd.read_html(r.text)
btc = pd.DataFrame(btcdata)



df[2]["Time"] = pd.to_datetime(df[2]["Time"])
df[2] = df[2].set_index(df[2]['Time'])

btc['Dates'] = btc.index

print(btc.info())



df[2]['Balance'] = df[2]['Balance'].str.replace("BTC","")
df[2]['Balance'] = df[2]['Balance'].str.replace(",", "")
df[2]['Balance'] = pd.to_numeric(df[2]['Balance'])

df[2]['Amount'] = df[2]['Amount'].str.replace(r"\(.*\)", "")
df[2]['Amount'] = df[2]['Amount'].str.replace("BTC", "")
df[2]['Amount'] = df[2]['Amount'].str.replace(",", "")
df[2]['Amount'] = pd.to_numeric(df[2]['Amount'])


# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])


fig.add_trace(
    go.Scatter(x=df[2]['Time'], y=df[2]['Amount'].where(
        df[2]['Amount'] < 0), line={'color': 'red'}, mode='markers'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df[2]['Time'], y=df[2]['Amount'].where(
        df[2]['Amount'] > 1), line={'color': 'green'},mode='markers'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=btc['Dates'], y=btc['Close'],
               name="Price", line={'color': 'gold'}),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="BTC Whale #3"
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Amount Purchased/Sold</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>BTC Price</b>", secondary_y=True)

fig.show()



