
import pandas as pd
import numpy as np
import datetime
import calendar

from statistics import stdev
from utils import write_as_csv
import trading_methodologies.trading_util as trading_util 


TRADING_METHOD_ARG = 'Trading Method.'
ASSET_ARG = 'Asset'
TIMEFRAME_ARG = 'Timeframe'
PURCHASE_ID_ARG = 'Purchase ID'
ASSET_ALLOC_ARG = 'Asset Alloc.'
PURCHASED_AMOUNT_ARG = 'purchased_amount'
ASSET_PRICE_ARG = 'Asset price'
PURCHASE_NUM = 'Purchase_num'

STRATEGY_OUTPUT_PATH = 'performance_analyzer/portfolio_metrics.csv'
PORTFOLIO_OUTPUT_PATH = 'performance_analyzer/portfolio_metrics_portfolio.csv'



class PerformanceAnalyst:

    def __init__(self, portfolios):
        self.portfolios = portfolios
        self.trade_methods = np.unique(self.portfolios[TRADING_METHOD_ARG])
        self.assets = np.unique(self.portfolios[ASSET_ARG])
        self.timeframes = np.unique(self.portfolios[TIMEFRAME_ARG])
        self.portfolio_ids = np.unique(self.portfolios[PURCHASE_ID_ARG])
        self.asset_alloc = np.unique(self.portfolios[ASSET_ALLOC_ARG])

        # sort them alphabetically to keep the order
        self.trade_methods.sort()
        self.assets.sort()
        self.cost_per_asset = [0.0, 0.2, 0.1, 0.2, 0.4]
        self.portfolios[PURCHASED_AMOUNT_ARG] = self.portfolios[ASSET_PRICE_ARG] * self.portfolios[PURCHASE_NUM]
        # though 'max' was picked, all the prices grouped by ASSET_ARG are the same

    def get_current_asset_values(self):
        current_asset_values = []
        for each in self.assets:
            # value of asset in the last date in the data
            day_max = max(calendar.monthcalendar(2020, self.timeframes[0])[-1:][0][:5])
            date_max = datetime.datetime(2020, self.timeframes[0], day_max)
            data_point = trading_util.find_data_point(each, date_max)[1]
            if (data_point is None):
                data_point = 1.0
            current_asset_values.append(data_point)
        current_asset_values[4] = 1.0
        return current_asset_values

    # cost of each asset * weight of each asset
    def calculate_cost(self, portfolio_method_tf):
        total_investment = portfolio_method_tf[PURCHASED_AMOUNT_ARG].sum()
        cost_per_asset = portfolio_method_tf.groupby(ASSET_ARG)[PURCHASED_AMOUNT_ARG].sum() / total_investment * self.cost_per_asset
        return cost_per_asset.sum()

    def calculate_volatility(self, portfolio_method_tf):
        mean_per_asset = portfolio_method_tf[PURCHASED_AMOUNT_ARG].mean()
        standard_dev = stdev(portfolio_method_tf[PURCHASED_AMOUNT_ARG])
        return standard_dev / mean_per_asset

    # renamed `return` into `asset_return` because it is a predefiend variable
    def calculate_return(self, portfolio_method_tf):
        #buy_amount = portfolio_method_tf[PURCHASED_AMOUNT_ARG].sum()
        #purchase num is a dollar amount and not a unit! It wouldnt make sense to have the unit either because you would need to get the cost at the time of purchase not the current cost
        buy_amount = portfolio_method_tf[PURCHASE_NUM].sum()
        #print("buy amount is " + str(buy_amount))
        #print(portfolio_method_tf)
        #share_count = portfolio_method_tf[portfolio_method_tf[PURCHASED_AMOUNT_ARG] > 0].groupby(ASSET_ARG)[PURCHASE_NUM].sum()
        #share_count = portfolio_method_tf.groupby(ASSET_ARG)[PURCHASE_NUM].sum()

        Assets = ['stocks', 'cbonds', 'sbonds', 'gold', 'cash']
        share_count = [] 
        final_prices = []
        for asset in Assets:
            try:
                share_count.append(portfolio_method_tf[portfolio_method_tf[ASSET_ARG] == asset][portfolio_method_tf['Date'] == portfolio_method_tf['Date'].max()]['#'].iloc[0])
            except:
                print("exception here")
                try: 
                    pointer = portfolio_method_tf[portfolio_method_tf[ASSET_ARG] == asset] -1
                    print("try block with asset search")
                    print(portfolio_method_tf[portfolio_method_tf[ASSET_ARG] == asset])
                except: 
                    print("faked a zero here because I dont know whats going on")
                    share_count.append(float(0))
                    continue
                share_count.append(portfolio_method_tf[portfolio_method_tf[ASSET_ARG] == asset]['#'].iloc[pointer])
        #print("share count is " + str(share_count))

        #calculate the current portfolio value by taking end asset amounts in units times their value on day of analysis
        current_asset_value = self.get_current_asset_values()
        #print("current asset values are " + str(current_asset_value))
        
        for num1, num2 in zip(share_count, current_asset_value):
            final_prices.append(num1 * num2)
        current_val = sum(final_prices)
        return (current_val - buy_amount) / buy_amount * 100
    

    def run_performance_analysis(self):
        performance_df = pd.DataFrame(columns=['method', 'timeframe', 'cost', 'volatility', 'return'])
        for each_method in self.trade_methods:
            data_for_method = self.portfolios[self.portfolios[TRADING_METHOD_ARG] == each_method]
            for each_tf in self.timeframes:
                data_method_tf = data_for_method[self.portfolios[TIMEFRAME_ARG] == each_tf]
                cost = self.calculate_cost(data_method_tf)
                volatility = self.calculate_volatility(data_method_tf)
                ret = self.calculate_return(data_method_tf)
                performance_df = performance_df.append({'method': each_method,
                                                        'timeframe': each_tf,
                                                        'cost': "{:.2f}".format(cost),
                                                        'volatility': "{:.2f}".format(volatility),
                                                        'return': "{:.2f}".format(ret)}, ignore_index=True)
        write_as_csv(STRATEGY_OUTPUT_PATH, performance_df)
        return performance_df

    def run_performance_analysis_portfolio(self):
        performance_df = pd.DataFrame(columns=['asset alloc', 'method', 'timeframe', 'volatility', 'return'])
        for each_portfolios in self.asset_alloc:
            data_for_method2 = self.portfolios[self.portfolios[ASSET_ALLOC_ARG] == each_portfolios]
            for each_method in self.trade_methods:
                data_for_method = data_for_method2[self.portfolios[TRADING_METHOD_ARG] == each_method]
                for each_tf in self.timeframes:
                    data_method_tf = data_for_method[self.portfolios[TIMEFRAME_ARG] == each_tf]
                    ret = self.calculate_return(data_method_tf)
                    volatility = self.calculate_volatility(data_method_tf)
                    performance_df = performance_df.append({'asset alloc': each_portfolios, 
                                                            'method': each_method,
                                                            'timeframe': each_tf,
                                                            'volatility': "{:.2f}".format(volatility),
                                                            'return': "{:.10f}".format(ret)}, ignore_index=True)
        write_as_csv(PORTFOLIO_OUTPUT_PATH, performance_df)
        return performance_df

