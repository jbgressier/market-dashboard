# Dashboard with equity (SPY), forex (USD), commodities (Gold, crude oil, wheat), bonds (Inflation-linked bonds).
# Data about growth, inflation, volatility, and yield.
# Data goes back as far as possible, with widget slider to choose time frame.

# import streamlit as st 
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

#Getting the data for SPY (daily)
#Closing prices only
data = yf.download("SPY")['Close']
data.to_csv("spy_data.csv")
print(data.index)
print('\n\n\n\n')

# Data Download
folder = "c:/Jean-Baptiste/SKEMA/FMI S1/Python/market-dashboard/"

def data_download(ticker, filename):
    path = os.path.join(folder, filename)
    data = yf.download(ticker, auto_adjust=False)['Close']
    data.to_csv(path)
    print(f"Sauvegardé : {path}")
    return data

data_dict={}
print(data_dict)
print()

ticker_filename = {
    "SPY": "spy.csv",
    "DX-Y.NYB": "usd.csv",
    "GC=F": "gold.csv",
    "WTI": "wti.csv",
    "ZW=F": "wheat.csv",
    "^TNX": "bonds.csv"
}
print(ticker_filename)

sanitized_ticker = {ticker:filename.replace('.csv','') for ticker, filename in ticker_filename.items()}
print(sanitized_ticker)

for ticker, filename in ticker_filename.items():
    data_dict[ticker] = data_download(ticker, filename)
    # print(data_dict)
    # print()

print(data_dict.keys())

# Sanity Checks
# Check for missing values
def check_na(data):
    null_sum = data.isna().sum()
    null_percentage = null_sum / len(data)
    print(f"Ratio of missing values: {null_percentage}\n Count of missing values: {null_sum}")

def fill_missing_values(df):
    '''Fill missing values using FFILL method, input is the dataframe, output is the filled dataframe'''
    df=df.ffill().dropna()
    return df

def plot_df(ticker):
    data=pd.read_csv(ticker_filename[ticker])
    plt.figure()
    plt.title(sanitized_ticker[ticker])
    plt.plot(data.index, data[ticker])
    plt.savefig(sanitized_ticker[ticker]+'.png')

for ticker in ticker_filename.keys():
    data = pd.read_csv(ticker_filename[ticker])
    check_na(data)
    data=fill_missing_values(data)
    plot_df(ticker)

spy = pd.read_csv('spy.csv', index_col=0, parse_dates=True)
spy=fill_missing_values(spy)
plot_df('SPY')
print(spy.head())
check_na(spy)

# Check for missing values
missing_values = data.isnull().sum() # number is zero, no missing values

# Plot the data
spy.plot(label='SPY')
plt.ylabel("SPY Closing Price")
plt.title("SPY Closing Price Over Time")
plt.yscale('log')

#forex using USD index
# usd = (yf.download("DX-Y.NYB", start=spy.index.min())['Close']
#        .pct_change()
#        .add(1)
#        .cumprod())

# usd.plot(label='USD Index')

usd = (yf.download("DX-Y.NYB", start=spy.index.min())['Close'].pct_change() + 1).cumprod()
usd['DX-Y.NYB'].plot(label='USD Index')

plt.legend()
plt.show()







