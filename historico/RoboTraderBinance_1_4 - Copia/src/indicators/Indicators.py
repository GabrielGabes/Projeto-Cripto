# indicators/Indicators.py
from .rsi import rsi
from .macd import macd
from .vortex import vortex
from .atr import atr
from .stochastic_rsi import stochastic_rsi
from .bollinger_bands import bollinger_bands
from .williams_r import williams_r
from .kdj import kdj
from .ichimoku import ichimoku
from .supertrend import supertrend


class Indicators:
    @staticmethod
    def getRSI(series, window=14, period=None, last_only=True):
        actual_window = period if period is not None else window
        return rsi(series, actual_window, last_only)

    @staticmethod
    def getMACD(series, fast_window=12, slow_window=26, signal_window=9):
        return macd(series, fast_window, slow_window, signal_window)

    @staticmethod
    def getVortex(series, window=14, positive=True):
        return vortex(series, window, positive)

    @staticmethod
    def getAtr(series, window=14):
        return atr(series, window)
        
    @staticmethod
    def getStochasticRSI(series, rsi_period=14, stoch_period=14, k_period=3, d_period=3):
        return stochastic_rsi(series, rsi_period, stoch_period, k_period, d_period)
    
    @staticmethod
    def getBollingerBands(df, window=20, num_std=2.0):
        return bollinger_bands(df['close'], window, num_std)
    
    @staticmethod
    def getWilliamsR(df, period=14):
        return williams_r(df, period)
    
    @staticmethod
    def getKDJ(df, k_period=9, d_period=3, j_period=3):
        return kdj(df, k_period, d_period, j_period)
    
    @staticmethod
    def getIchimoku(df, tenkan_period=9, kijun_period=26, senkou_span_b_period=52, displacement=26):
        return ichimoku(df, tenkan_period, kijun_period, senkou_span_b_period, displacement)
    
    @staticmethod
    def getSupertrend(df, atr_period=10, multiplier=3.0):
        return supertrend(df, atr_period, multiplier)
