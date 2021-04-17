from crawler_by_asset.crawler import Crawler

CASH_PAGE = 'https://www.investing.com/indices/usdollar-historical-data'
CASH_OUTPUT = 'usdollar'

cash_crawler = Crawler(CASH_PAGE, CASH_OUTPUT)