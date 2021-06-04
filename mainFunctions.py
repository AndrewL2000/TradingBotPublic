#*************************************** OVERVIEW ***************************************#
# Project: Trading Bot for SWYFTX
# Description: Receives stock data from SWYFTX API server for analysis and trading
# Authors: Andrew Luo
# Last Updated: 10/05/2021
#****************************************************************************************#

# **************************** MODULES **************************** #
from time import sleep
from dotenv import main
from numpy import empty, nan
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import datetime 
#import time   # sleep
from scipy.io import savemat  # Saving lists as matlab files

from technicalAnalysisFunctions import *  # Import all functions from this file
from apiFunctions import *  
from tickerClass import _tickerClass
from strategy1 import *
from emailAlert import *
from profitLossCalc import *

# ***************************************************************** #


# ***************************************************************** #

def tradeSwitch(i):
    
    tradeSwitcher = {
        True: "Buy",     # Last Year
        False: "Sell",  
    }
    return tradeSwitcher.get(i, "Buy")
    

    

def mainRoutine(tickerList, resolutionInputList):

    listTickerTrade = []    # List of tickers being traded this scan
    resultList = []
    
    for resolutionInput in resolutionInputList:
        for i in range(len(tickerList)):
            ticker = _tickerClass(tickerList[i], resolutionInput)
            print(f"[{ticker.tickerName[:-4]} ({ticker.resolution})] Updated: {ticker.isoTime[-1]}")

            # Put strategies here
            tradeDictList = strategy1_v1(ticker)
            plResult = profitLossCalc(ticker, tradeDictList)

            epochTime1 = list(tradeDictList['epochTime'])
            ID = list(tradeDictList['ID'])
            isoTime1 = ['']*len(epochTime1)

            # Check if time detected
            if epochTime1:
                for j in range(len(epochTime1)):
                    epoch = datetime.datetime.fromtimestamp(int(epochTime1[j]))
                    isoTime1[j] = str(epoch)

                if datetime.datetime.now().timestamp() - epochTime1[-1] <= refreshSwitch(ticker.resolution):
                    sendEmail(isoTime1[-1], ticker, round(tradeDictList["tradePrice"][-1], 2))
                    listTickerTrade.append({"Ticker":tickerList[i][:-4], "Resolution":ticker.resolution, "Time":isoTime1[-1], "Trade":tradeSwitch(tradeDictList["Trade"][-1]), "plAvg":plResult["plAvg"], "tradePrice":tradeDictList["tradePrice"][-1], "winRate":plResult["winRate"]})  # List of dictionaries
                
                if plResult["pl"]:
                    resultList.append({"Ticker":tickerList[i][:-4], "Resolution":ticker.resolution, "plTotal":plResult["plTotal"], "plMin":min(plResult["pl"]), "plMax":max(plResult["pl"]), "winRate":plResult["winRate"]})
    for j in resultList:
        
        symbol = j["Ticker"]
        resolution = j["Resolution"]
        plTotal = j["plTotal"]
        plMin = round(j["plMin"])
        plMax = round(j["plMax"])
        winRate = j["winRate"]

        print(f"[{symbol} ({resolution})] Total P/L: {plTotal}%   Lowest P/L: {plMin}%   Highest P/L: {plMax}%   WR: {winRate}%")

    nextDataTime = roundTime(datetime.datetime.now() , round_to=refreshSwitch(ticker.resolution))
    wait_seconds = nextDataTime.timestamp() - datetime.datetime.now().timestamp()
    print("Current Time:", datetime.datetime.now(), ' Next update:', wait_seconds) 
    
  
    return wait_seconds + 5, listTickerTrade, resultList, nextDayScanSeconds()




def init():
    print("************ Running Initial Test ************")
    print(f"Time until 10AM next day {nextDayScanSeconds()} seconds")
    ticker = _tickerClass('HNTUSDT', '1d')
    print("Latest price of", ticker.tickerName, apiLatestPrice(ticker.tickerName))
    print(f"[ {ticker.tickerName} ({ticker.resolution}) ] Updated: {ticker.isoTime[-1]}")

    dict1 = strategy1_v1(ticker)
    epochTime1 = list(dict1['epochTime'])
    isoTime1 = [''] * len(epochTime1)


    for i in range(len(epochTime1)):
        epoch = datetime.datetime.fromtimestamp(epochTime1[i])
        isoTime1[i] = str(epoch)

    #sendEmail(isoTime1, ticker)

    # ***************************************************************** #

    #************* MOVING AVERAGES *************#
    (MA_5) = MA(ticker.C_ha, 5)     # Short Term: Weeks (Used with MA 20)
    (MA_9) = MA(ticker.C_ha, 9)     # Short Term: Days (Used with TEMA)
    (MA_20) = MA(ticker.C_ha, 20)   # Medium Term: Fortnightly 
    (MA_50) = MA(ticker.C_ha, 50)   # Medium Term: Months (Used with MA 200)
    (MA_200) = MA(ticker.C_ha, 200) # Long Term: Years

    #************* BOLLINGER BANDS *************#
    (BOLU, BOLL) = bollingerBands(MA_20, ticker.C_ha, 20)

    #************* RELATIVE STRENGTH INDEX (RSI) *************#
    RSI = relativeStrengthIndex(ticker.C_ha, 14)

    #************* EXPONENTIAL MOVING AVERAGE (EMA) *************#
    EMA_20 = EMA(ticker.C_ha, 20)

    #************* TRIPLE EXPONENTIAL MOVING AVERAGE (TEMA) *************#
    TEMA_8 = TEMA(ticker.C_ha, 8)

    #************* MOVING AVERAGE CONVERGENCE/DIVERGENCE (MACD) *************#
    (MACD_1, EMA_26, EMA_12, MACD_EMA_9, MACD_histogram) = MACD(ticker.C_ha, 26, 12, 9)

    #************* VISUALISATION ON MATLAB *************#
    mdic = {
        "BOLU": BOLU, 
        "BOLL": BOLL, 
        "MA_5":MA_5,
        "MA_9":MA_9,
        "MA_20":MA_20,
        "MA_50":MA_50,
        "MA_200":MA_200,
        "O_ha":ticker.O_ha, 
        "H_ha":ticker.H_ha, 
        "C_ha":ticker.C_ha, 
        "L_ha":ticker.L_ha, 
        "Time":ticker.epochTime,
        "RSI":RSI,
        "TEMA_8": TEMA_8,
        "MACD": MACD_1,
        "MACD_EMA_9": MACD_EMA_9,
        "MACD_histogram": MACD_histogram,
        "TickerName": ticker.tickerName,

        "S1_Time":dict1['epochTime'],
        "S1_Trade":dict1['Trade'],
        "S1_ID":dict1['ID'],
        "S1_TradePrice":dict1["tradePrice"]
        }

    savemat("data.mat", mdic) # Saves data as matlab file
    print("************ Ending Initial Test ************")


    
def roundTime(dt=None, round_to=60):
    if dt == None: 
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds + round_to/2) // round_to * round_to 

    adjust = rounding - seconds
    if adjust < 0:
        adjust = round_to + adjust
    
    return dt + datetime.timedelta(0, adjust, -dt.microsecond)

def nextDayScanSeconds():
    tomorrow = datetime.datetime.now() + datetime.timedelta(1)
    midnight = datetime.datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=10, minute=0, second=0)
    return (midnight - datetime.datetime.now()).seconds