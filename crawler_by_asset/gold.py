from util import Crawler

GOLD_PAGE = 'https://www.investing.com/etfs/spdr-gold-trust-historical-data'
GOLD_OUTPUT = 'gold_data.csv'

gold_crawler = Crawler(GOLD_PAGE, GOLD_OUTPUT)
