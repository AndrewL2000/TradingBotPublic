#*************************************** OVERVIEW ***************************************#
# Title: 
# Description: 
# Authors: Andrew Luo
# Last Updated: 12/05/2021
#****************************************************************************************#

# **************************** MODULES **************************** #
from datetime import time

from technicalAnalysisFunctions import *  # Import all functions from this file
from tickerClass import *
from statistics import mean

# ***************************************************************** #
crossingTEMA = False
fallingTEMA = True
rsi80 = False
crossingMA_20_50 = False


def pChange(final, initial):
    if final == initial:
        return 100
    elif initial == 0:
        return 0
    else: 
        return (final - initial) / initial * 100.0
        
def strategy1_v1(ticker):
    dict = {"epochTime":[], "Trade":[], "ID":[], "tradePrice":[]}

    O_ha = ticker.O_ha
    H_ha = ticker.H_ha
    C_ha = ticker.C_ha
    L_ha = ticker.L_ha

    O = ticker.O
    H = ticker.H
    C = ticker.C
    L = ticker.L

    TEMA_8 = TEMA(C_ha, 8)
    MA_9 = MA(C_ha, 9)
    MA_20 = MA(C_ha, 20)
    MA_50 = MA(C_ha, 50)
    MA_200 = MA(C_ha, 200)

    (BOLU, BOLL) = bollingerBands(MA_20, C_ha, 20)
    RSI = relativeStrengthIndex(C_ha, 14)

    g_MA_20 = np.zeros_like(O)  



  # GLOBAL VARIABLES
    global crossingTEMA 
    global fallingTEMA
    global rsi80 
    global crossingMA_20_50


    for i in range(0, ticker.samples - 1):
        
        # SELLING
        
        if dict["Trade"] and i >= 15 and dict["Trade"][-1] == True:
            
            # SELL INDICATORS
            # RSI hit 80 threshold
            if RSI[i] >= 80:
                rsi80 = True

            if MA_20[i] > MA_50[i]:
                crossingMA_20_50 = True

            if TEMA_8[i-1] > MA_9[i-1] and pChange(TEMA_8[i-1], MA_9[i-1]) - pChange(TEMA_8[i], MA_9[i]) > 0:
                fallingTEMA = True

            if TEMA(C_ha, 8)[i] > MA(C_ha, 9)[i]:
                crossingTEMA = True   

              
            # RSI[i] - min(RSI[i - 15:i])  (RSI[i] - RSI[dict["ID"][-1]]) > 20

            # PROFITS
            # Check first red
            if crossingTEMA and O_ha[i] > C_ha[i] and (abs(C_ha[i] - O_ha[i]) > abs(C_ha[i-1] - O_ha[i-1])) and ~crossingMA_20_50:
                sellPrice = O[i+1]
                dict = sellAppend(dict, ticker, i+1, sellPrice)


            elif  (RSI[i-1] - RSI[i] > 0) and fallingTEMA and crossingTEMA and (pChange(O_ha[i], C_ha[i]) < -1) and pChange(MA_9[i], TEMA_8[i]) < -1:
                sellPrice = O[i+1]
                dict = sellAppend(dict, ticker, i+1, sellPrice)


            elif rsi80 and RSI[i] < 80 and fallingTEMA and crossingTEMA:
                sellPrice = O[i+1]
                dict = sellAppend(dict, ticker, i+1, sellPrice)

            elif H[i] > 1.2*BOLU[i-1]:
                sellPrice = 1.2*BOLU[i-1]
                dict = sellAppend(dict, ticker, i, sellPrice)
                

            # STOP LOSS
            elif pChange(C[i], dict["tradePrice"][-1]) < -10:
                sellPrice = O[i+1]
                dict = sellAppend(dict, ticker, i+1, sellPrice)


        # BUYING
        else:
            if (((pChange(L_ha[i], BOLL[i]) < -5 and RSI[i] < 30) or (pChange(L_ha[i], BOLL[i]) < -10)) and L_ha[i] < BOLL[i]):
                dict = buyAppend(dict, ticker, i+1)

            # Quick Price Fall
            elif i >= 10 and max(RSI[i-10:i]) - RSI[i] >= 30: 
                dict = buyAppend(dict, ticker, i+1)


    return dict

    # TIME (Trade being made) & BUY/SELL (Type of trade)
    # 10pm | 11pm  | 1am
    # 1    | 0     | 0


def buyAppend(dict, ticker, i):
    dict["epochTime"].append(ticker.epochTime[i])
    dict["Trade"].append(True)
    dict["ID"].append(i)  

    buyPrice = ticker.O[i+1]
    #buyPrice = mean([ticker.L[i], min(ticker.O[i], ticker.C[i])])
    dict["tradePrice"].append(buyPrice)
   
    return dict

def sellAppend(dict, ticker, i, sellPrice):
    dict["epochTime"].append(ticker.epochTime[i])
    dict["Trade"].append(False) 
    dict["ID"].append(i)

    #sellPrice = mean([ticker.H[i], max([ticker.O[i], ticker.C[i]])])
    dict["tradePrice"].append(sellPrice)

    global crossingTEMA 
    global fallingTEMA
    global rsi80 
    global crossingMA_20_50

    crossingTEMA = False
    fallingTEMA = False
    rsi80 = False
    crossingMA_20_50 = False

    return dict
    


