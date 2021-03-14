from util import Crawler

CBOND_PAGE = 'https://www.investing.com/etfs/ishares-global-corporate-bond-$-historical-data'
CBOND_OUTPUT = 'cbond_data.csv'

cbond_cralwer = Crawler(CBOND_PAGE, CBOND_OUTPUT)
