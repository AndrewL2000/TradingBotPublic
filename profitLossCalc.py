#*************************************** OVERVIEW ***************************************#
# Project: 
# Description: 
# Authors: Andrew Luo
# Last Updated: 12/05/2021
#****************************************************************************************#

# **************************** MODULES **************************** #
from datetime import time
from statistics import mean
from numpy import nan

from numpy.lib.function_base import average
from technicalAnalysisFunctions import *  # Import all functions from this file
from tickerClass import *

# ***************************************************************** #

def profitLossCalc(ticker, dictTrade):
    result = {"pl":[]}

    ID = dictTrade["ID"]
    trade = dictTrade["Trade"]
    tradePrice = dictTrade["tradePrice"]

    #ticker.C_ha[ID]
    sum = 0
    count = 0
    buyCount = 0
    sellCount = 0

    for i in range(len(ID)):
        if trade[i] == True:
            sum += tradePrice[i]
            count += 1
            buyCount += 1

            
        else:
            avgBuyPrice = sum / count
            result["pl"].append((tradePrice[i] - avgBuyPrice) / avgBuyPrice * 100)

            count = 0
            sum = 0
            sellCount += 1
    
    sum = 0
    win = 0

    for i in result["pl"]:
        sum += i
        if i > 0:
            win += 1

    result["plTotal"] = round(sum)
    
    if len(result["pl"]):
        result["winRate"] = round(win / len(result["pl"]) * 100) 
        result["plAvg"] = round(mean(result["pl"]))
    else:
        result["winRate"] = nan
    result["buyTrades"] = buyCount
    result["sellTrades"] = sellCount
    result["totalTrades"] = buyCount + sellCount

    return result