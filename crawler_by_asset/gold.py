from crawler_by_asset.crawler import Crawler

GOLD_PAGE = 'https://www.investing.com/etfs/spdr-gold-trust-historical-data'
GOLD_OUTPUT = 'spdr-gold-trust'

gold_crawler = Crawler(GOLD_PAGE, GOLD_OUTPUT)
