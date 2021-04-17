This project is developed in **Python3.7**

# Installation
pip install -r requirements.txt

# Project Description
Please refer to the file 'exercise_statement.pdf' in the repository.

# Architecture
```
├── README.md
├── crawled_data                   -- craweled dattaset from www.investing.com
│   ├── amundi-msci-wrld-ae-c.csv
│   ├── db-x-trackers-ii-global-sovereign-5.csv
│   ├── ishares-global-corporate-bond-$.csv
│   ├── spdr-gold-trust.csv
│   └── usdollar.csv
├── crawler_by_asset               -- crawlers          
│   ├── __init__.py
│   ├── cash.py
│   ├── corporate_bonds.py
│   ├── crawler.py                 -- a core trigger to run scrawlers in each asset
│   ├── global_stocks.py
│   ├── gold.py
│   └── soverign_bond.py
├── crawler_drivers                -- a set of crawler drivers to offer options for a web browser
│   ├── chromedriver
│   └── geckodriver
├── exercise_statement.pdf    
├── main.py                        -- a core trigger to start crawling, make porfolios, and analyze their performance
├── performance_analysis.py        -- a performance analyzer to evalute cost, volatility, and return
├── portfolio_allocation      
│   ├── portfolio_allocations.csv
│   └── portfolio_generator.py     -- a trigger to generate porfolios
├── portfolio_metrics.csv
├── requirements.txt
├── trading_methodologies          -- a porfolio developer (DCA, oneoff, rebalance)
│   ├── DCA.py
│   ├── trading_methodologies.csv
│   ├── __init__.py
│   ├── oneoff.py
│   ├── rebalance.py
│   └── trading_util.py
└── utils.py
```

# Acknowledgment
The dataset was scraped from www.investing.com
