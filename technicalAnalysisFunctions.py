#*************************************** OVERVIEW ***************************************#
# Title: Technical Analysis Functions
# Description: Functions for technical analysis
# Authors: Andrew Luo
# Last Updated: 11/05/2021
#****************************************************************************************#

# **************************** MODULES **************************** #
# Importing the statistics module
from statistics import pstdev   # population standard deviation
import numpy as np
from numpy.core.function_base import linspace
# ***************************************************************** #

 

# ************* HEIKEN ASHI ************* #
# Removes noise and smooths price action
def heikenAshi(O, H, C, L):
  samples = len(O)  # Number of bars in the chart

  O_ha = np.zeros_like(O) 
  H_ha = np.zeros_like(H) 
  C_ha = np.zeros_like(C)      
  L_ha = np.zeros_like(L)    

  # First Heiken Ashi Bar
  O_ha[0] = 1/2 * (O[0] + C[0])
  H_ha[0] = max(H[0], O[0], C[0])
  C_ha[0] = 1/4 * (O[0] + H[0] + L[0] + C[0])
  L_ha[0] = min(L[0], O[0], C[0])

  for i in range(1, len(O)):   
    O_ha[i] = 1/2 * (O_ha[i-1] + C_ha[i-1])
    H_ha[i] = max(H[i], O[i], C[i])
    C_ha[i] = 1/4 * (O[i] + H[i] + L[i] + C[i])
    L_ha[i] = min(L[i], O[i], C[i])
    
  return (O_ha, H_ha, C_ha, L_ha)



# ************* MOVING AVERAGE ************* #
# Moving Average (also known as Simple Moving Average) based on close price
# Window size determines how many previous bars to use, including current bar 

# matlab https://medium.com/python-data/setting-up-a-bollinger-band-with-python-28941e2fa300

def MA(C, MA_window_size):       
  MA = np.zeros_like(C)    # 0 represents values that are out of scope
  for i in range(MA_window_size, len(C)+1):
    this_window = C[i-MA_window_size:i]
    MA[i-1] = sum(this_window) / MA_window_size     # Calculation for finding Moving Average
    if i == MA_window_size:
      MA[:MA_window_size-1] = np.nan
  return MA



# ************* BOLLINGER BANDS ************* #
# Composed of 3 lines: Middle is MA 20 
# Upper and Lower bands are +- 2 standard deviations 
def bollingerBands(MA, C, MA_window_size):       
  BOLU = np.zeros_like(C)    # 0 represents values that are out of scope
  BOLL = np.zeros_like(C)    # 0 represents values that are out of scope
  for i in range(MA_window_size, len(C)+1):
    this_window = C[i-MA_window_size:i]
    sd = pstdev(this_window)
    BOLU[i-1] = MA[i-1] + 2*sd
    BOLL[i-1] = MA[i-1] - 2*sd

    if i == MA_window_size:
      BOLU[:MA_window_size-1] = BOLU[i-1]
      BOLL[:MA_window_size-1] = BOLL[i-1]
  return (BOLU, BOLL)  



# ************* RSI ************* #
# https://github.com/mtamer/python-rsi/blob/master/src/stock.py
# https://github.com/mtamer/python-rsi/blob/master/src/main.py
def relativeStrengthIndex(C, RSI_window_size):
  diffs = np.diff(C)

  # First RSI value for first window
  seed = diffs[:RSI_window_size+1]  # Slicing upto first window size bars e.g. 14 bars
  up = sum(seed[seed >= 0]) / RSI_window_size
  down = -sum(seed[seed < 0]) / RSI_window_size
  rs = up / down
  RSI = np.zeros_like(C) 
  RSI[:RSI_window_size] = 100 - 100/(1 + rs)

  # Rest of RSI values
  for i in range(RSI_window_size, len(C)):
    diff = diffs[i-1]
    if diff > 0:
      up_val = diff
      down_val = 0
    else:
      up_val = 0
      down_val = -diff
    
    up = (up * (RSI_window_size - 1) + up_val) / RSI_window_size
    down = (down * (RSI_window_size - 1) + down_val) / RSI_window_size

    rs = up / down
    RSI[i] = 100 - 100/(1 + rs)

  return RSI



# ************* EXPONENTIAL MOVING AVERAGE ************* #
def EMA(C, EMA_window_size):
  EMA = np.zeros_like(C)
  EMA[:EMA_window_size-1] = MA(C, EMA_window_size)[EMA_window_size] # First EMA value uses MA
  for i in range(EMA_window_size, len(C)):
    EMA[i] = (C[i] * (2/(1 + EMA_window_size))) + (EMA[i-1] * (1 - 2/(1 + EMA_window_size)))

  return EMA



# ************* TRIPLE EXPONENTIAL MOVING AVERAGE ************* #
def TEMA(C, TEMA_window_size):
  EMA1 = EMA(C, TEMA_window_size)
  EMA2 = EMA(EMA1, TEMA_window_size)
  EMA3 = EMA(EMA2, TEMA_window_size)

  TEMA = 3*EMA1 - 3*EMA2 + EMA3 
  TEMA[:TEMA_window_size] = np.nan

  return TEMA



# ************* MOVING AVERAGE CONVERGENCE/DIVERGENCE (MACD) ************* #
# https://www.investopedia.com/terms/m/macd.asp
def MACD(C, EMAfast_window_size, EMAslow_window_size, Signal_window_size):
  EMA_fast = EMA(C, EMAfast_window_size)
  EMA_slow = EMA(C, EMAslow_window_size)
  MACD = EMA_fast - EMA_slow
  MACD_signal = EMA(MACD, Signal_window_size) # Signal Line of MACD
  MACD_histogram = MACD - MACD_signal

  return (-MACD, EMA_fast, EMA_slow, -MACD_signal, MACD_histogram)