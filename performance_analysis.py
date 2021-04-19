
import pandas as pd
import numpy as np

from statistics import stdev
from utils import write_as_csv


# Columns : 'Date', 'Trading Method.', 'Purchase ID', 'Asset Alloc.', 'Asset',
#        'Amount($)', 'Asset price', '#'],
#       dtype='object'

# ['DCA' 'DCA-rebalance' 'Oneoff' 'oneoff-rebal.']
# ['cash', 'cbonds', 'gold', 'sbonds', 'stocks']


class PerformanceAnalyst:

    def __init__(self, portfolios):
        self.portfolios = portfolios
        self.trade_methods = np.unique(self.portfolios['Trading Method.'])
        self.assets = np.unique(self.portfolios['Asset'])
        self.timeframes = np.unique(self.portfolios['Timeframe'])
        self.portfolio_ids = np.unique(self.portfolios['Purchase ID'])
        # self.portfolio_amount =

        # sort them alphabetically to keep the order
        self.trade_methods.sort()
        self.assets.sort()
        self.cost_per_asset = [0.0, 0.2, 0.1, 0.2, 0.4]
        self.portfolios['total_amount'] = self.portfolios['Asset price'] * self.portfolios['#']
        # though 'max' was picked, all the prices grouped by 'Asset' are the same
        self.current_asset_value = portfolios[portfolios['Date'] == portfolios['Date'].max()].groupby('Asset').max()['Asset price']

    # cost of each asset * weight of each asset
    def calculate_cost(self, portfolio_method_tf):
        total_investment = portfolio_method_tf['total_amount'].sum()
        cost_per_asset = portfolio_method_tf.groupby('Asset')['total_amount'].sum() / total_investment * self.cost_per_asset
        return cost_per_asset.sum()

    def calculate_volatility(self, portfolio_method_tf):
        mean_per_asset = portfolio_method_tf['total_amount'].mean()
        standard_dev = stdev(portfolio_method_tf['total_amount'])
        return standard_dev / mean_per_asset

    # renamed `return` into `asset_return` because it is a predefiend variable
    def calculate_return(self, portfolio_method_tf):
        buy_amount = portfolio_method_tf['total_amount'].sum()
        share_count = portfolio_method_tf[portfolio_method_tf['total_amount'] > 0].groupby('Asset')['#'].sum()
        current_val = (share_count * self.current_asset_value).sum()
        return (current_val - buy_amount) / buy_amount * 100

    def run_performance_analysis(self):
        performance_df = pd.DataFrame(columns=['method', 'timeframe', 'cost', 'volatility', 'return'])
        for each_method in self.trade_methods:
            data_for_method = self.portfolios[self.portfolios['Trading Method.'] == each_method]
            for each_tf in self.timeframes:
                data_method_tf = data_for_method[self.portfolios['Timeframe'] == each_tf]
                cost = self.calculate_cost(data_method_tf)
                volatility = self.calculate_volatility(data_method_tf)
                ret = self.calculate_return(data_method_tf)
                performance_df = performance_df.append({'method': each_method, 'timeframe': each_tf, 'cost': cost, 'volatility': volatility,
                                       'return': ret}, ignore_index=True)
        filepath = 'portfolio_metrics.csv'
        write_as_csv(filepath, performance_df)
        return performance_df

