This project is developed in **Python3.7**

# installation
pip install -r requirements.txt

# Project Description

Please refer to the file 'exercise_statement.pdf' in the repository.

# Task 1
First of all the __init__.py file creates all the relevant Crawler ([cash_crawler, gold_crawler, sbond_crawler, stock_crawler, cbond_crawler]) which includes the CASH_PAGE with the URL and the CASH_OUTPUT with the currency. When a crawler is created an instance of the Crawler class is build which integrates the start_page, an output_name for csv export and the driver for the webscraping. As we all use different systems and webbrowser, the user can choose between Safari, Chrome and Firefox. 
The main function of the Crawler class is the run_crawler function. This uses the generated crawler and generates a filepath which is used to later store the exported csc. Then then crawler is started and the data is accessed. In the access_the_data() function several html elements are accessed to set the timeframe and to then to export the investments from the table. From the data the price and date is joined to a touple and afterwards exported to a csv file. Last, the close_webdriver() function is used to close the session of the web scraping. The csv export is done by the write_as_csv() function of the utils.py file.

For the portfolio allocation the portfolio_generator.py and the PortfolioGenerator class is used to generate. For this, an algorithm (generate_allocation function) sums up all the values in a range of 0 to 20 in different loops to cover all the avaiable options. Afterwards this values are exported as a csv file

Inside the crawled_data folder, the crawled data is stored and saved to the git repository. 
Inside the crawler_by_asset folder, the initiation python file is stored as well as the different stocks with the page and ouput currency. 
Inside the crawler_drivers forlder, an instance of chrome and firefox (gecko) driver are stored so you don't need to download them

# Task 2

# Task 3