
import datetime
from crawler_by_asset import cash_crawler, gold_crawler, sbond_crawler, cbond_crawler, stock_crawler
from portfolio_allocation import portfolio_generator
from trading_methodologies import oneoff, DCA


#asset classes
#cash
#cash_crawler.run_crawler()

# corporate bonds
#cbond_crawler.run_crawler()


#gold
#gold_crawler.run_crawler()

#stocks
#stock_crawler.run_crawler()

#sovereign bonds
#sbond_crawler.run_crawler()


# #generate portfolio
#portfolio = portfolio_generator.generatePortfolioAllocation()
#portfolio_generator.write_as_csv(portfolio)

#run trading methodology
#one-off
#print(oneoff(10000, '30/12/2020'))
#one-off rebalanced

#DCA
print(DCA(10000, '03/02/2020', 3))


#DCA rebalanced