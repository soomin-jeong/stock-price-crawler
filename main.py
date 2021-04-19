
import datetime
import pandas as pd
import numpy as np

from performance_analysis import PerformanceAnalyst
from crawler_by_asset import crawlers
from portfolio_allocation.portfolio_generator import portfolio_generator
from trading_methodologies import oneoff, DCA, rebalance, oneoff_rebalance


# set the tasks to run here
RUN_CRAWLER = False
GENERATE_PORTFOLIOS = False
GENERATE_STRATEGIES = False
ANALYZE_PERFORMANCE = True


def main():
    if RUN_CRAWLER:
        for each in crawlers:
            each.run_crawler()

    if GENERATE_STRATEGIES:
        portfolio = portfolio_generator.generate_allocation()
        portfolio_generator.write_as_csv(portfolio)

    if GENERATE_STRATEGIES:
        #one-off
        data, message = oneoff(100000, '01/01/2020', 1)
        print(message)

        #one-off rebalanced
        oneoff_rebalance(1)

        #DCA
        #setting the false flag here means we are not rebalancing
        print(DCA(100000, '01/01/2020', 1, "FALSE"))
        print ("regular DCA finished")

        #DCA rebalanced
        #setting the true flag means we will rebalance
        print(DCA(100000, '01/01/2020', 1, "TRUE"))
        print("DCA rebal finished")

    if ANALYZE_PERFORMANCE:
        trading_methodology_filename = 'trading_methodologies.csv'


        # Performance Analysis
        data = pd.read_csv(trading_methodology_filename, header=0, parse_dates=['Date'], dtype={'#': np.int32})
        pa = PerformanceAnalyst(data)
        pa.run_performance_analysis()

if __name__ == "__main__":
    main()