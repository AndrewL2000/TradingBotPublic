#*************************************** OVERVIEW ***************************************#
# Project: Trading Bot for SWYFTX
# Description: Receives stock data from SWYFTX API server for analysis and trading
# Authors: Andrew Luo
# Last Updated: 10/05/2021
#****************************************************************************************#

# **************************** MODULES **************************** #
from mainFunctions import *
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
from mainFunctions import *
from profitLossCalc import *


# ***************************************************************** #


# ***************************************************************** #


init()

tickerList = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'LTCUSDT', 'BCHUSDT', 'UNIUSDT', 'ADAUSDT', 'DOTUSDT', 'BATUSDT', 'VETUSDT', 'BTGUSDT', 'ETCUSDT', 'HNTUSDT', 'SHIBUSDT', 'DOGEUSDT', 'SOLUSDT', 'LINKUSDT']
tickerList = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ADAUSDT', 'DOTUSDT', 'HNTUSDT']
tickerList = ['XRPUSDT']
resolutionInput = ['15m', '1d']

waitTime, listTickerTrade, plResultList, nextDaySeconds = mainRoutine(tickerList, resolutionInput)

#apiNewOrder()

#while True:
  
  #waitTime, listTickerTrade, plResultList, nextDaySeconds = mainRoutine(tickerList, resolutionInput)
  #sleep(waitTime + 5)
