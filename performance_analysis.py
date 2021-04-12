
import pandas as pd
import numpy as np
from statistics import stdev

filename = 'trading_methodologies.csv'

# Columns : 'Date', 'Trading Method.', 'Purchase ID', 'Asset Alloc.', 'Asset',
#        'Amount($)', 'Asset price', '#'],
#       dtype='object'

# ['DCA' 'DCA-rebalance' 'Oneoff' 'oneoff-rebal.']
# ['cash', 'cbonds', 'gold', 'sbonds', 'stocks']


class PerformanceAnalyst:

    def __init__(self, aggregated_data):
        self.data = aggregated_data
        self.trade_methods = np.unique(self.data['Trading Method.'])
        self.assets = np.unique(self.data['Asset'])
        # sort them alphabetically to keep the order
        self.trade_methods.sort()
        self.assets.sort()
        self.cost = [0.0, 0.2, 0.1, 0.2, 0.4]
        self.data['total_amount'] = self.data['Asset price'] * self.data['#']

    # cost of each asset * weight of each asset
    def get_cost(self):
        portfolio_cost = []
        for each_method in self.trade_methods:
            data_for_method = self.data[self.data['Trading Method.'] == each_method]
            total_investment = data_for_method['total_amount'].sum()
            costs = data_for_method.groupby('Asset')['total_amount'].sum() / total_investment * self.cost
            portfolio_cost.append(costs.sum())
        return portfolio_cost

    def get_volatility(self):
        portfolio_volatility = []
        for each_method in self.trade_methods:
            data_for_method = self.data[self.data['Trading Method.'] == each_method]
            mean_per_asset = data_for_method.groupby('Asset')['total_amount'].mean()
            standard_dev = data_for_method.groupby('Asset')['total_amount'].apply(stdev)
            volatility = standard_dev / mean_per_asset
            portfolio_volatility.append(volatility)
        return portfolio_volatility

    def get_return(self):
        portfolio_return = []
        for each_method in self.trade_methods:
            data_for_method = self.data[self.data['Trading Method.'] == each_method]
            buy_amount = data_for_method['total_amount'].sum()
            share_count = data_for_method[data_for_method['total_amount'] > 0].groupby('Asset')['#'].sum()
            last_date = data_for_method['Date'][:-len(self.assets)]
            current_val = 0
            ret = (current_val - buy_amount) / buy_amount * 100
            portfolio_return.append(ret)
        return portfolio_return


aggregated_data = pd.read_csv(filename, header=0)
pa = PerformanceAnalyst(aggregated_data)
pa.get_return()

