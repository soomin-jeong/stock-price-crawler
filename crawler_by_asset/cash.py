from util import Crawler

CASH_PAGE = 'https://www.investing.com/indices/usdollar-historical-data'
CASH_OUTPUT = 'cash_data_'

cash_crawler = Crawler(CASH_PAGE, CASH_OUTPUT)