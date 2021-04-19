
import pandas as pd
import numpy as np

from performance_analyzer.performance_analysis import PerformanceAnalyst
from crawler_by_asset import crawlers
from portfolio_allocation.portfolio_generator import portfolio_generator
from trading_methodologies import oneoff, DCA, oneoff_rebalance


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
        startmoney = 100000
        investment_date = '01/01/2020'
        timeframe = 1

        oneoff(startmoney, investment_date, timeframe)
        oneoff_rebalance(timeframe)
        DCA(startmoney, investment_date, timeframe)
        DCA(startmoney, investment_date, timeframe, True)

    if ANALYZE_PERFORMANCE:
        trading_methodology_filename = 'trading_methodologies/trading_methodologies.csv'

        # Performance Analysis
        data = pd.read_csv(trading_methodology_filename, header=0, parse_dates=['Date'], dtype={'#': np.int32})
        pa = PerformanceAnalyst(data)
        pa.run_performance_analysis()


if __name__ == "__main__":
    main()