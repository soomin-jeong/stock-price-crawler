
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
        self.portfolio_names = np.unique(self.portfolios['Trading Method.'])
        self.assets = np.unique(self.portfolios['Asset'])
        # sort them alphabetically to keep the order
        self.portfolio_names.sort()
        self.assets.sort()
        self.cost_per_asset = [0.0, 0.2, 0.1, 0.2, 0.4]
        self.portfolios['total_amount'] = self.portfolios['Asset price'] * self.portfolios['#']
        # though 'max' was picked, all the prices grouped by 'Asset' are the same
        self.current_asset_value = portfolios[portfolios['Date'] == portfolios['Date'].max()].groupby('Asset').max()['Asset price']

    # cost of each asset * weight of each asset
    @property
    def cost(self):
        portfolio_cost = []
        for each_method in self.portfolio_names:
            data_for_method = self.portfolios[self.portfolios['Trading Method.'] == each_method]
            total_investment = data_for_method['total_amount'].sum()
            costs = data_for_method.groupby('Asset')['total_amount'].sum() / total_investment * self.cost_per_asset
            portfolio_cost.append(costs.sum())
        return portfolio_cost

    @property
    def volatility(self):
        portfolio_volatility = []
        for each_method in self.portfolio_names:
            data_for_method = self.portfolios[self.portfolios['Trading Method.'] == each_method]
            mean_per_asset = data_for_method['total_amount'].mean()
            standard_dev = stdev(data_for_method['total_amount'])
            volatility = standard_dev / mean_per_asset
            portfolio_volatility.append(volatility)
        return portfolio_volatility

    # renamed `return` into `asset_return` because it is a predefiend variable
    @property
    def asset_return(self):
        portfolio_return = []
        for each_method in self.portfolio_names:
            data_for_method = self.portfolios[self.portfolios['Trading Method.'] == each_method]
            buy_amount = data_for_method['total_amount'].sum()
            share_count = data_for_method[data_for_method['total_amount'] > 0].groupby('Asset')['#'].sum()
            current_val = (share_count * self.current_asset_value).sum()
            ret = (current_val - buy_amount) / buy_amount * 100
            portfolio_return.append(ret)
        return portfolio_return

    def run_performance_analysis(self):
        performance_df = pd.DataFrame(columns=['cost', 'volatility', 'return'])
        performance_df['cost'] = self.cost
        performance_df['volatility'] = self.volatility
        performance_df['return'] = self.asset_return
        performance_df.index = list(self.portfolio_names)

        filepath = 'portfolio_metrics.csv'
        write_as_csv(filepath, performance_df)
        return performance_df


