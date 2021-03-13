from utils import Crawler

SBOND_PAGE = 'https://www.investing.com/etfs/db-x-trackers-ii-global-sovereign-5-historical-data'
SBOND_OUTPUT = 'sbond_cash.csv'

sbond_crawler = Crawler(SBOND_PAGE, SBOND_OUTPUT)
