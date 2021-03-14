from util import Crawler

STOCK_PAGE = 'https://www.investing.com/funds/amundi-msci-wrld-ae-c-historical-data'
STOCK_OUTPUT = 'stock_data.csv'

stock_crawler = Crawler(STOCK_PAGE, STOCK_OUTPUT)
