
from crawler_by_asset import cash_crawler, gold_crawler, sbond_crawler, cbond_crawler, stock_crawler

# crawlers = [cash_crawler, gold_crawler, sbond_crawler, cbond_cralwer]
#
# for each in crawlers:
#     each.run_cralwer()
#


# asset classes
# cash
cash_crawler.run_crawler()

# corporate bonds
cbond_crawler.run_crawler()


#gold
gold_crawler.run_crawler()

#stocks
stock_crawler.run_crawler()

#sovereign bonds
sbond_crawler.run_crawler()

