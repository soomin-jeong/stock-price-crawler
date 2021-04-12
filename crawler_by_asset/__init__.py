
from .cash import cash_crawler
from .gold import gold_crawler
from .soverign_bond import sbond_crawler
from .global_stocks import stock_crawler
from .corporate_bonds import cbond_crawler

crawlers = [cash_crawler, gold_crawler, sbond_crawler, stock_crawler, cbond_crawler]