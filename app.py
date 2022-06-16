import numpy as np
import scipy.stats as si
import streamlit as st

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
    spot = st.number_input('Spot Price (S):', value=100, min_value=0)
    strike = st.number_input('Strike Price (K):', value=100, min_value=0)
    timeInterval = st.selectbox("Time interval:", ('Days','Months','Years'),index=0)
    timeToExp = st.number_input('Time to expiration in (t - {}):'.format(timeInterval), value=30, min_value=0)
    if timeInterval == 'Days':
        t = timeToExp / 365
    elif timeInterval == 'Months':
        t = timeToExp / 12
    else:
        t = timeToExp
    st.write("Years to expiry: {:.2f}".format(t))
    rf = st.number_input('Risk-Free Interest Rate (r in %):', value=5, min_value=0)
    divRate = st.number_input('Dividend Rate (q in %):', value=0, min_value=0)
    vol = st.number_input('Volatility (v in %):', value=25, min_value=0)
    #startDate = st.date_input('Start Date', pd.to_datetime('2016-11-01'))
    #endDate = st.date_input('End Date', datetime.now())
    submit_btn = st.form_submit_button(label='Calculate')
 
call = callOption(spot, strike, t, rf/100, divRate/100, vol/100)
put = putOption(spot, strike, t, rf/100, divRate/100, vol/100)
st.write(call)
st.write(put)
