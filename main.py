
import datetime
import pandas as pd
from performance_analysis import PerformanceAnalyst
from crawler_by_asset import crawlers
from portfolio_allocation.portfolio_generator import portfolio_generator
from trading_methodologies import oneoff, DCA, rebalance, oneoff_rebalance

# dDeactivate cralwers as they are complete
# for each in crawlers:
#     each.run_crawler()

# generate portfolio
# portfolio = portfolio_generator.generate_allocation()
# portfolio_generator.write_as_csv(portfolio)

# #run trading methodology
# #one-off
# data, message = oneoff(10000, '01/03/2020')
# print(message)
#
#
# #one-off rebalanced
# oneoff_rebalance(3)
# # DCA
# print(DCA(10000, '03/02/2020', 3, "FALSE"))
#
#
# #DCA rebalanced
# print(DCA(10000, '01/03/2020', 2, "TRUE"))
trading_methodology_filename = 'trading_methodologies.csv'


# Performance Analysis
aggr_data = pd.read_csv(trading_methodology_filename, header=0, parse_dates=['Date'])
pa = PerformanceAnalyst(aggr_data)
pa.run_performance_analysis()


