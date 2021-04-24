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
│   ├── __init__.py                -- initiate the different crawlers with url and currency
│   ├── cash.py                    -- cash crawler instance with page and output
│   ├── corporate_bonds.py         -- corporate bonds crawler instance with page and output
│   ├── crawler.py                 -- a core trigger to run scrawlers in each asset
│   ├── global_stocks.py           -- global stocks crawler instance with page and output
│   ├── gold.py                    -- gold crawler instance with page and output
│   └── soverign_bond.py           -- soreign bond crawler instance with page and output
├── crawler_drivers                -- a set of crawler drivers to offer options for a web browser
│   ├── chromedriver               -- an installed chrome driver for web scraping
│   └── geckodriver                -- an installed firefox driver for web sraping
├── exercise_statement.pdf         -- the description of the exercise from moodle
├── main.py                        -- a core trigger to start crawling, make porfolios, and analyze their performance
├── performance_analysis.py        -- a performance analyzer to evalute cost, volatility, and return
├── portfolio_allocation      
│   ├── portfolio_allocations.csv  -- the generated portfolio as csv export
│   └── portfolio_generator.py     -- a trigger to generate porfolios
├── portfolio_metrics.csv
├── requirements.txt               -- the packages which needs to be installed with pip prior to run
├── trading_methodologies          -- a porfolio developer (DCA, oneoff, rebalance)
│   ├── DCA.py                     -- Defines and executes the logic for DCA trading methodology
│   ├── trading_methodologies.csv  -- Output file which trading methodologies write their actions to
│   ├── __init__.py                -- Makes packages and functions in trading methodologies importable for others
│   ├── oneoff.py                  -- Defines and executes logic for oneoff trading method
│   ├── rebalance.py               -- Defines and executes logic for oneoff rebalance and DCA rebalance trading methods
│   └── trading_util.py            -- Utility function which supports trading methodologies with shared functionalities
└── utils.py
```


# Task Description

## Task 1 (Web Scraping)

To run the task please decide between based on your system. For mac I would recommend webdriver.Safari(). We all had problems with some drivers but one should work for you.
```
self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
self.driverdriver = webdriver.Chrome(ChromeDriverManager().install())      
```

Webdrivers if locally installed
```
self.driver = webdriver.Safari()
self.driver = webdriver.Firefox()
```

Then on main.py uncomment 
```
for each in crawlers:
    each.run_crawler()
```

and all the to be crawled data will generated and stored in the crawled_data directory.

First of all the __init__.py file creates all the relevant Crawler ([cash_crawler, gold_crawler, sbond_crawler, stock_crawler, cbond_crawler]) which includes the CASH_PAGE with the URL and the CASH_OUTPUT with the currency. When a crawler is created an instance of the Crawler class is build which integrates the start_page, an output_name for csv export and the driver for the webscraping. As we all use different systems and webbrowser, the user can choose between Safari, Chrome and Firefox. 
The main function of the Crawler class is the run_crawler function. This uses the generated crawler and generates a filepath which is used to later store the exported csc. Then then crawler is started and the data is accessed. In the access_the_data() function several html elements are accessed to set the timeframe and to then to export the investments from the table. From the data the price and date is joined to a touple and afterwards exported to a csv file. Last, the close_webdriver() function is used to close the session of the web scraping. The csv export is done by the write_as_csv() function of the utils.py file.

For the portfolio allocation the portfolio_generator.py and the PortfolioGenerator class is used to generate. For this, an algorithm (generate_allocation function) sums up all the values in a range of 0 to 20 in different loops to cover all the avaiable options. Afterwards this values are exported as a csv file

Inside the crawled_data folder, the crawled data is stored and saved to the git repository. 
Inside the crawler_by_asset folder, the initiation python file is stored as well as the different stocks with the page and ouput currency. 
Inside the crawler_drivers forlder, an instance of chrome and firefox (gecko) driver are stored so you don't need to download them.

Functionality about web scraping has been addressed in:

```
├── crawler_by_asset                       
│   ├── __init__.py
│   ├── cash.py                   
│   ├── corporate_bonds.py        
│   ├── crawler.py                 
│   ├── global_stocks.py           
│   ├── gold.py                   
│   └── soverign_bond.py
├── crawler_drivers                
│   ├── chromedriver         
│   └── geckodriver       
```

## Task 2 (Data Generation)
In order to execute the trading the user needs to specify the amount of money to be invested, the date of the investment and the investment period in months. They also need to decided which trading strategy to use. 

In order to run the oneoff trading methodology uncomment the following line in main.py:

```
data, message = oneoff(100000, '01/01/2020', 1)
```

The first parameter is the investment amount, the second is the date of the investment and the third is how long the investment will be held in months. The program goes through all the portfolio allocations portfolio_allocations.csv and Trades are executed. For each portfolio the number of each asset bought as well as data such as the price of the asset on the date is written to trading_methodologies.csv.

Note: when the user specifies 1 as the investment period the program deletes trading_methodologies.csv and rewrites the header line. Otherwise the data will always be appended to the CSV

In order to run the oneoff rebalance trading methodology uncomment the following line in main.py:
```
oneoff_rebalance(1)
```

Here the paramater is the holding period in months. Oneoff_rebalance analyzes previous one-off trades with a matching investment period and rebalances these. Therefore oneoff must be run first.

In order to run the DCA trading methodology uncomment the following line in main.py:
```
print(DCA(100000, '01/01/2020', 1 False))
```
Here the first parameter is how much money should be invested, the second is the date of the investment, the third parameter is the investment period in months, and finally the FALSE flag means the DCA trades will not be rebalanced.


In order to run the oneoff trading methodology uncomment the following line in main.py:
```
print(DCA(100000, '01/01/2020', 1))
```

As with DCA the parameters included here are how much money should be invested, the second is the date of the investment, the third parameter is the investment period in months. The TRUE flag means rebalance will be applied to the DCA trades. 

Functionality about trading data generation has been addressed in:
```
├── trading_methodologies          
│   ├── DCA.py                     
│   ├── trading_methodologies.csv  
│   ├── __init__.py                
│   ├── oneoff.py                  
│   ├── rebalance.py               
│   └── trading_util.py           
└── utils.py
```

## Task 3 (Data Analysis)

# Acknowledgment
The dataset was scraped from www.investing.com
