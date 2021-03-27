
from crawler_by_asset import cash_crawler, gold_crawler, sbond_crawler, cbond_crawler, stock_crawler
from portfolio_allocation import portfolio_generator
from trading_methodologies import oneoff


#asset classes
#cash
#cash_crawler.run_crawler()

#@lena you can try running this and you will see it writes the data correctly to the csv file ishares-global-corporate-bond-$
#https://www.investing.com/etfs/ishares-global-corporate-bond-$-historical-data
# corporate bonds
cbond_crawler.run_crawler()


#gold
#gold_crawler.run_crawler()

#@lena this is the one that does not work. No data is written to the csv file amundi-msci-wrld-ae-c.csv. The function runs
#https://www.investing.com/funds/amundi-msci-wrld-ae-c-historical-data
#stocks
stock_crawler.run_crawler()

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

#DCA rebalanced