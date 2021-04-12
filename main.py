
import datetime
from crawler_by_asset import crawlers
from portfolio_allocation import portfolio_generator
from trading_methodologies import oneoff, DCA, rebalance

# deactivate cralwers as they are complete
# for each in crawlers:
#     each.run_crawler()

#generate portfolio
#portfolio = portfolio_generator.generatePortfolioAllocation()
#portfolio_generator.write_as_csv(portfolio)

#run trading methodology
#one-off
data, message = oneoff(10000, '01/03/2020')
print (message)


#one-off rebalanced
#oneoff_rebalance("oneoff", 3)
#DCA
#print(DCA(10000, '03/02/2020', 3, "FALSE"))


#DCA rebalanced
print(DCA(10000, '01/03/2020', 2, "TRUE"))