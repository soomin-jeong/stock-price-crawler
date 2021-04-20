
import pandas as pd
import numpy as np
from pandas.tseries.offsets import BMonthEnd
import datetime
import calendar

from statistics import stdev
from utils import write_as_csv
import trading_methodologies.trading_util as trading_util 


class PerformanceAnalyst:

    def __init__(self, portfolios):
        self.portfolios = portfolios
        self.trade_methods = np.unique(self.portfolios['Trading Method.'])
        self.assets = np.unique(self.portfolios['Asset'])
        self.timeframes = np.unique(self.portfolios['Timeframe'])
        self.portfolio_ids = np.unique(self.portfolios['Purchase ID'])
        self.asset_alloc = np.unique(self.portfolios['Asset Alloc.'])
        # self.portfolio_amount =

        # sort them alphabetically to keep the order
        self.trade_methods.sort()
        self.assets.sort()
        self.cost_per_asset = [0.0, 0.2, 0.1, 0.2, 0.4]
        self.portfolios['purchased_amount'] = self.portfolios['Asset price'] * self.portfolios['Purchase_num']
        # though 'max' was picked, all the prices grouped by 'Asset' are the same
        
    # def get_current_asset_values(self, portfolio_data):
    #     current_asset_values = []
    #     for each in self.assets:
    #         # value of asset in the last date in the data
    #         print(portfolio_data['Date'].max())
    #         last_value = portfolio_data[portfolio_data['Asset'] == each][portfolio_data['Date'] == portfolio_data['Date'].max()]['Asset price'].iloc[0]
    #         current_asset_values.append(last_value)
    #     return current_asset_values

    def get_current_asset_values(self, portfolio_data):
        current_asset_values = []
        for each in self.assets:
            # value of asset in the last date in the data
            day_max = max(calendar.monthcalendar(2020, self.timeframes[0])[-1:][0][:5])
            date_max = datetime.datetime(2020, self.timeframes[0], day_max)
            data_point = trading_util.find_data_point(each, date_max)[1]
            if (data_point is None):
                data_point = 1.0
            current_asset_values.append(data_point)
        return current_asset_values

    # cost of each asset * weight of each asset
    def calculate_cost(self, portfolio_method_tf):
        total_investment = portfolio_method_tf['purchased_amount'].sum()
        cost_per_asset = portfolio_method_tf.groupby('Asset')['purchased_amount'].sum() / total_investment * self.cost_per_asset
        return cost_per_asset.sum()

    def calculate_volatility(self, portfolio_method_tf):
        mean_per_asset = portfolio_method_tf['purchased_amount'].mean()
        standard_dev = stdev(portfolio_method_tf['purchased_amount'])
        return standard_dev / mean_per_asset

    # renamed `return` into `asset_return` because it is a predefiend variable
    def calculate_return(self, portfolio_method_tf):
        buy_amount = portfolio_method_tf['purchased_amount'].sum()
        #share_count = portfolio_method_tf[portfolio_method_tf['purchased_amount'] > 0].groupby('Asset')['Purchase_num'].sum()
        share_count = portfolio_method_tf.groupby('Asset')['Purchase_num'].sum()
        current_asset_value = self.get_current_asset_values(portfolio_method_tf)
        current_val = (share_count * current_asset_value[0:len(share_count)]).sum()
        return (current_val - buy_amount) / buy_amount * 100
    
    #def calculate_portfolio_return(self, portfolio_method_tf):

    def run_performance_analysis(self):
        performance_df = pd.DataFrame(columns=['method', 'timeframe', 'cost', 'volatility', 'return'])
        for each_method in self.trade_methods:
            data_for_method = self.portfolios[self.portfolios['Trading Method.'] == each_method]
            for each_tf in self.timeframes:
                data_method_tf = data_for_method[self.portfolios['Timeframe'] == each_tf]
                cost = self.calculate_cost(data_method_tf)
                volatility = self.calculate_volatility(data_method_tf)
                ret = self.calculate_return(data_method_tf)
                performance_df = performance_df.append({'method': each_method,
                                                        'timeframe': each_tf,
                                                        'cost': "{:.10f}".format(cost),
                                                        'volatility': "{:.10f}".format(volatility),
                                                        'return': "{:.10f}".format(ret)}, ignore_index=True)
        filepath = 'performance_analyzer/portfolio_metrics.csv'
        write_as_csv(filepath, performance_df)
        return performance_df

    def run_performance_analysis_portfolio(self):
        performance_df = pd.DataFrame(columns=['asset alloc', 'method', 'timeframe', 'cost', 'volatility', 'return'])
        for each_portfolios in self.asset_alloc:
            data_for_method2 = self.portfolios[self.portfolios['Asset Alloc.'] == each_portfolios]
            for each_method in self.trade_methods:
                data_for_method = data_for_method2[self.portfolios['Trading Method.'] == each_method]
                for each_tf in self.timeframes:
                    data_method_tf = data_for_method[self.portfolios['Timeframe'] == each_tf]
                    cost = self.calculate_cost(data_method_tf)
                    volatility = self.calculate_volatility(data_method_tf)
                    ret = self.calculate_return(data_method_tf)
                    performance_df = performance_df.append({'asset alloc': each_portfolios, 'method': each_method,
                                                            'timeframe': each_tf,
                                                            'cost': "{:.10f}".format(cost),
                                                            'volatility': "{:.10f}".format(volatility),
                                                            'return': "{:.10f}".format(ret)}, ignore_index=True)
        filepath = 'performance_analyzer/portfolio_metrics_portfolio.csv'
        write_as_csv(filepath, performance_df)
        return performance_df

