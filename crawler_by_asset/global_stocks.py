from crawler import Crawler

STOCK_PAGE = 'https://www.investing.com/funds/amundi-msci-wrld-ae-c-historical-data'
STOCK_OUTPUT = 'amundi-msci-wrld-ae-c'

stock_crawler = Crawler(STOCK_PAGE, STOCK_OUTPUT)
