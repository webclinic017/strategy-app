import pandas as pd
import numpy as np

import streamlit as st

from utils.processing import AKData
from utils.plot import plot_pf

class BaseStrategy(object):
    '''base strategy'''
    _name = "base"
    param_dict = {}
    param_def = {}
    stock_dfs = []
    pf_kwargs = dict(fees=0.001, slippage=0.001, freq='1D')


    def __init__(self, symbolsDate_dict:dict):
        market = symbolsDate_dict['market']
        symbols = symbolsDate_dict['symbols']
        self.start_date = symbolsDate_dict['start_date']
        self.end_date = symbolsDate_dict['end_date']
        self.datas = AKData(market)
        self.stock_dfs = []
        for symbol in symbols:
            if symbol!='':
                stock_df = self.datas.get_stock(symbol, self.start_date, self.end_date)
                if stock_df.empty:
                    st.warning(f"Warning: stock '{symbol}' is invalid or missing. Ignore it", icon= "⚠️")
                else:
                    self.stock_dfs.append((symbol, stock_df))

        # initialize param_dict using default param_def
        for param in self.param_def:
            if param["step"] == 0:
                self.param_dict[param["name"]] = [int((param["min"] + param['max'])/ 2)]
            else:
                self.param_dict[param["name"]] = np.arange(param["min"], param["max"], param["step"])
        
    def log(self, txt, dt=None, doprint=False):
        pass

    def maxSR(self, param, output_bool=False):
        self.param_dict = param
        if self.run(output_bool):
            if output_bool:
                plot_pf(self.pf)
            return True
        else:
            return False

    def update(self, param_dict:dict):
        """
            update the strategy with the param dictiorary saved in portfolio
        """
        self.param_dict = {}
        for k, v in param_dict.items():
            self.param_dict[k] = [v]

        self.run()
        return self.pf    
        
