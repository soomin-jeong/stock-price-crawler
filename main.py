
import datetime
from crawler_by_asset import cash_crawler, gold_crawler, sbond_crawler, cbond_crawler, stock_crawler
from portfolio_allocation import portfolio_generator
from trading_methodologies import oneoff, DCA, rebalance


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


#generate portfolio
#portfolio = portfolio_generator.generatePortfolioAllocation()
#portfolio_generator.write_as_csv(portfolio)

#run trading methodology
#one-off
data, message = oneoff(10000, '01/03/2020')
print (message)


#one-off rebalanced
rebalance("oneoff", 3)
#DCA
#print(DCA(10000, '03/02/2020', 3))


#DCA rebalanced