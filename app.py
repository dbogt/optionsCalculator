import numpy as np
import scipy.stats as si
import streamlit as st
import yfinUDFs as yf
import pandas as pd

#%% Options Functions
def N(x):
    return si.norm.cdf(x)
    
def callOption(S, K, T, r, q, sigma):
    d1 = (np.log(S/K) + (r - q + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    return S*np.exp(-q*T) * N(d1) - K * np.exp(-r*T)* N(d2)

def putOption(S, K, T, r, q, sigma):
    d1 = (np.log(S/K) + (r - q + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    return K*np.exp(-r*T)*N(-d2) - S*np.exp(-q*T)*N(-d1)

#%% Streamlit Controls
st.header("Options Calculator")

with st.sidebar.form(key='inputs_form'):    
    spot = st.number_input('Spot Price (S):', value=100.0, min_value=0.0)
    strike = st.number_input('Strike Price (K):', value=100.0, min_value=0.0)
    timeInterval = st.selectbox("Time interval:", ('Days','Months','Years'),index=0)
    timeToExp = st.number_input('Time to expiration in (t - {}):'.format(timeInterval), value=30, min_value=0)
    if timeInterval == 'Days':
        t = timeToExp / 365
    elif timeInterval == 'Months':
        t = timeToExp / 12
    else:
        t = timeToExp
    st.write("Years to expiry: {:.2f}".format(t))
    rf = st.number_input('Risk-Free Interest Rate (r in %):', value=5.0, min_value=0.0)
    divRate = st.number_input('Dividend Rate (q in %):', value=0.0, min_value=0.0)
    vol = st.number_input('Volatility (v in %):', value=25.0, min_value=0.0)
    #startDate = st.date_input('Start Date', pd.to_datetime('2016-11-01'))
    #endDate = st.date_input('End Date', datetime.now())
    submit_btn = st.form_submit_button(label='Calculate')
 
call = callOption(spot, strike, t, rf/100, divRate/100, vol/100)
put = putOption(spot, strike, t, rf/100, divRate/100, vol/100)
st.metric("Call Value","${:.4f}".format(call))
st.metric("Put Value","${:.4f}".format(put))
output = """Spot: {:.2f}\n
Strike: {:.2f}\n
Time (years): {:.2f}\n 
Risk-Free Rate: {:.2%}\n
Dividend Rate: {:.2%}\n
Volatility: {:.2%}\n
""".format(spot, strike, t, rf/100, divRate/100, vol/100)
st.write(output)


st.header("Option Chain")
ticker = st.text_input("Ticker:","SPY")
expDate = st.text_input("Expiry Date:","2022-11-18")
optionType = st.selectbox("Call or Puts:",('calls','puts'),index=0)
df = yf.optionChain(ticker=ticker, date=expDate, calls_puts = optionType)
expDF = yf.grabExpDates(ticker)
link = "https://query2.finance.yahoo.com/v7/finance/options/{}?date=".format(ticker)
expDF['Link'] = expDF.apply(lambda x: link+str(x['Unix Date']), axis=1)

price = yf.fnYFinJSON(ticker, "regularMarketPrice")
ltmDivYield = yf.fnYFinJSON(ticker,'trailingAnnualDividendYield')
st.metric("{} Last Price".format(ticker),"{:.2f}".format(price))
st.metric("{} LTM Dividend Yield".format(ticker),"{:.2%}".format(ltmDivYield))
st.write(df)

st.write("Expiry Dates")

st.dataframe(expDF)
#st.write(expDF.to_html(escape=False, index=False), unsafe_allow_html=True)