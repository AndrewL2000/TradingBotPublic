#*************************************** OVERVIEW ***************************************#
# Title: Ticker Object
# Description: Receives stock data from SWYFTX API server for analysis and trading
# Authors: Andrew Luo
# Last Updated: 10/05/2021
#****************************************************************************************#



# **************************** MODULES **************************** #
from statistics import median_low
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import datetime
import time
from scipy.io import savemat  # Saving lists as matlab files

from technicalAnalysisFunctions import *  # Import all functions from this file
from apiFunctions import *  

# ***************************************************************** #

class _tickerClass:
    def __init__(self, ticker_input, resolution_input):

        #ticker_input = str(input("Enter a cryptocurrency ticker: \n"))
        #resolution_input= str(input("Enter a resolution: \n"))

        #ticker_input = 'SHIB'
        #resolution_input = '1m'

        (self.data, self.tickerName, self.resolution) = apiConnection(ticker_input, resolution_input)

        # ************* CANDLESTICK INITIALISATION ************* #
        self.samples = len(self.data)  # Number of bars in the chart
        self.O = [0] * self.samples 
        self.H = [0] * self.samples  
        self.C = [0] * self.samples     
        self.L = [0] * self.samples       # Low Price
        self.V = [0] * self.samples       # Volume
        self.epochTime = [0] * self.samples
        self.isoTime = [0] * self.samples 
        self.latestPrice = apiLatestPrice(self.tickerName)

        # Converting data from JSON dicts into values
        i = 0
        for ohclv in self.data:
            self.O[i] = float(ohclv[1])  # Converting OHCLV into floats 
            self.H[i] = float(ohclv[2])
            self.C[i] = float(ohclv[4])
            self.L[i] = float(ohclv[3])
            self.V[i] = float(ohclv[5])
            self.epochTime[i] = int(ohclv[0])/1000 # EPOCH Opening Time in Seconds
            self.isoTime[i] = datetime.datetime.fromtimestamp(self.epochTime[i])  # ISO Time
            i = i + 1

        self.samples += 1
        self.O.append(self.latestPrice)
        self.H.append(self.latestPrice)
        self.C.append(self.latestPrice)
        self.L.append(self.latestPrice)
        self.epochTime.append(int(time.time()))
        self.isoTime.append(datetime.datetime.fromtimestamp(self.epochTime[-1]))

        #************* INITIALISATION OF HEIKEN ASHI ARRAYS *************#
        self.O_ha = [0] * self.samples 
        self.H_ha = [0] * self.samples  
        self.C_ha = [0] * self.samples     
        self.L_ha = [0] * self.samples   

        # Obtain Heiken Ashi values
        (self.O_ha, self.H_ha, self.C_ha, self.L_ha) = heikenAshi(self.O, self.H, self.C, self.L) 



    @property
    def get_C(self):
        return self.C
        