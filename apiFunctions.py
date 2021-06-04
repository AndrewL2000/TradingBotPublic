#*************************************** OVERVIEW ***************************************#
# Title: API Functions 
# Description: Functions for API communication
# Authors: Andrew Luo
# Last Updated: 10/05/2021
#****************************************************************************************#



# **************************** MODULES **************************** #
import os
from numpy import floor
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from binance.client import Client
from binance.helpers import round_step_size
from dotenv import load_dotenv

import datetime
# ***************************************************************** #



# **************************** SWITCH CASES **************************** #

def resolutionSwitch(i, endTime):
    res_switcher = {
        '1d': '1d',
        '4h': '4h', 
        '1h': '1h',
        '15m': '15m',
        '5m': '5m',
        '1m': '1m'
    }

    # CHANGE THESE VALUES TO MODIFY PERFORMANCE SPEED
    startTime_switcher = {
        '1d': 31622400,     # Last Year
        '4h': 7889229,  
        '1h': 7889229,      # Last 3 Months
        '15m': 2629743,     # Last Month
        '5m': 100000,
        '1m': 43830       # Last Month
    }

    

    return (res_switcher.get(i, '1d'), endTime - startTime_switcher.get(i, 31622400))

# Resolution to seconds
def refreshSwitch(i):
    
    refresh_switcher = {
        '1d': 86400,     # Last Year
        '4h': 14400,  
        '1h': 3600,      # Last 3 Months
        '15m': 900,     # Last Month
        '5m': 300,
        '1m': 60       # Last Month
    }
    return refresh_switcher.get(i, 86400)

# ***************************************************************** #


#************* API CONNECTION *************#
# Connecting to the SWYFTX Server to retrieve data

def apiConnection(ticker_input, resolution_input):

    headers = {
        'Accepts': 'application/json',
        'Content-Type': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    # Check for API Connection
    try:
        # https://binance-docs.github.io/apidocs/spot/en/#change-log
        # api key = sFCpa8vpAYIeDFhZqzqXivXz9SNfhkMUSlFUU5pK4AvH25zGs9NStIFiecf2XbZX

        endTime = int(datetime.datetime.now().timestamp()) # Epoch in seconds
        (resolution, startTime) = resolutionSwitch(resolution_input, endTime)
        startTime = startTime * 1000 # Epoch in milliseconds
        endTime = endTime * 1000 # Epoch in milliseconds
        
        #api = 'https://api.swyftx.com.au/charts/getBars/USD/' + ticker_input + '/ask/?resolution=' + resolution +'&timeStart=' + str(startTime) + '&timeEnd=' + str(endTime)
        api = 'https://api.binance.com/api/v3/klines?symbol=' + ticker_input +'&interval=' + resolution + '&limit=1000'

        response = session.get(api)
        tickerName = ticker_input

        if (response.status_code == 200):           
            data = json.loads(response.text)
            parseData = json.dumps(response.json())
            f1 = open("TickerData/" + tickerName + '-' + resolution +"-data.json", "w")
            f1.write(parseData)
            f1.close
            
        else:  # Read old data
            print("API does not exist") 
            try:
                f1 = open("TickerData/" + tickerName + '-' + resolution +"-data.json", "w")
            except IOError:
                tickerName = 'BTCUSDT'
                print("File not accessible, BTC file is used instead")
                f1 = open("TickerData/BTCUSDT-" + resolution + "-data.json", "r")

            parseData = f1.read()
            f1.close
            data = json.loads(parseData)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        print('\n')

    return (data, tickerName, resolution)




# Returns latest price 
def apiLatestPrice(ticker_input):

    headers = {
        'Accepts': 'application/json',
        'Content-Type': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    try:
        api = 'https://api.binance.com/api/v3/ticker/price?symbol=' + ticker_input
        response = session.get(api)
        data = json.loads(response.text) 
        latestPrice = round(float(data["price"]), 2)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        print('\n')

    return latestPrice

#   https://algotrading101.com/learn/binance-python-api-guide/
#   https://www.youtube.com/watch?v=3uxAn7EBSS0
#   https://python-binance.readthedocs.io/en/latest/account.html#order-validation
def apiNewOrder():
    load_dotenv()

    #init 
    BINANCE_API = os.environ.get('BINANCE_API')
    BINANCE_SECRET = os.environ.get('BINANCE_SECRET')
    API_URL = 'https://api.binance.com/api'

    try:
        client = Client(BINANCE_API, BINANCE_SECRET)
        print("Logged into Binance")
        client.API_URL = API_URL

        status = client.get_account_api_trading_status()
        print(status)
        status = client.get_account_status()
        print(status)

        info = client.get_asset_balance(asset='AUD')
        print(info)

        info = client.get_account()
        
        for bal in info['balances']:
            if float(bal['free']) > 0:
                print(bal)      

        amount = 0.000234234
        tick_size = 0.00001
        rounded_amount = round_step_size(amount, tick_size)

        print(rounded_amount)


        #trades = client.get_my_trades(symbol='')
        #for t in trades:
        #    print(t)
        

        
        #data = json.loads(response.text) 
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        print('\n')

    return 0    

