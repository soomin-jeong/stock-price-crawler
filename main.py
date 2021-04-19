
import datetime
import pandas as pd
import numpy as np

from performance_analysis import PerformanceAnalyst
from crawler_by_asset import crawlers
from portfolio_allocation.portfolio_generator import portfolio_generator
from trading_methodologies import oneoff, DCA, rebalance, oneoff_rebalance

#*******************************************
#Uncomment these lines to run the crawlers

# Deactivate cralwers as they are complete
# for each in crawlers:
#     each.run_crawler()

# generate portfolio
# portfolio = portfolio_generator.generate_allocation()
# portfolio_generator.write_as_csv(portfolio)

#run trading methodologies
#The performance metrics are based on 1 month, 3 month, 6 month, 9 month and 12 month investment periods starting 01/01/2020
#We will assume we have 100.000 USD to invest

#*******************************************
#uncomment these lines to run all trades for 1 month investment period

# #one-off
# data, message = oneoff(100000, '01/01/2020', 1)
# print(message)
#
# #one-off rebalanced
# #oneoff_rebalance(1)
#
# #DCA
# #setting the flase flag here means we are not rebalancing
# #print(DCA(100000, '01/01/2020', 1, "FALSE"))
# #print ("regular DCA finished")
#
# #DCA rebalanced
# #setting the true flag means we will rebalance
# print(DCA(100000, '01/01/2020', 1, "TRUE"))
# print ("DCA rebal finished")

#*******************************************
#uncomment these lines to run all trades for 3 month investment period

#one-off
#data, message = oneoff(100000, '01/01/2020', 3)
#print(message)

#one-off rebalanced
#oneoff_rebalance(3)

#DCA
#setting the flase flag here means we are not rebalancing
#print(DCA(100000, '01/01/2020', 3, "FALSE"))


#DCA rebalanced
#setting the true flag means we will rebalance
#print(DCA(100000, '01/01/2020', 3, "TRUE"))

#*******************************************
#Uncomment these lines to run analysis of the trades

trading_methodology_filename = 'trading_methodologies.csv'


# Performance Analysis
data = pd.read_csv(trading_methodology_filename, header=0, parse_dates=['Date'], dtype={'#': np.int32})
pa = PerformanceAnalyst(data)
pa.run_performance_analysis()


