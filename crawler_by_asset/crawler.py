import time
import os
import pandas as pd
from selenium import webdriver

#use webdriver_manager to ensure support for different driver types in all our dev environments
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils import write_as_csv

# Date range to search
START_DATE = '01/01/2020'
END_DATE = '12/31/2020'
COMBINED_DATE = '01/01/2020 - 12/31/2020'


class Crawler(object):
    def __init__(self, start_page, output_name):
        self.start_page = start_page
        self.output_name = output_name
        self.driver = None

    def start_webdriver(self):
        ##Webdrivers managed by webdriver-manager. Preferred use.

        #self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        #self.driverdriver = webdriver.Chrome(ChromeDriverManager().install())
        
        ##Webdrivers if locally installed

        self.driver = webdriver.Safari()
        #self.driver = webdriver.Firefox()
        self.driver.get(self.start_page)
        time.sleep(2)

    def access_the_data(self):
        self.driver.maximize_window()

        # accept cookies
        self.driver.find_element_by_id("onetrust-accept-btn-handler").click()
    
        # set timeframe
        self.driver.execute_script("document.getElementById('widgetFieldDateRange').innerHTML = '01/01/2020 - 12/31/2020'")
        self.driver.execute_script("document.getElementById('picker').value = '01/01/2020 - 12/31/2020'")
        self.driver.execute_script("document.getElementsByClassName('datePickerIcon')[1].click()")
        time.sleep(1)
        self.driver.find_elements_by_id("applyBtn")[0].click()

        # get values from table
        table = self.driver.find_element_by_id("results_box").find_elements_by_tag_name("tr")
        time.sleep(1)
        # write data given a header
        data = pd.DateFrame(columns=["date", "price"])
        for row in table:
            value = row.find_elements_by_tag_name("td")
            if (len(value) in (6, 7)):
                date = value[0].get_attribute('data-real-value')
                date_formatted = time.strftime('%d/%m/%Y', time.localtime(int(date)))
                price = value[1].get_attribute('data-real-value')
                data = data.append({'date': date_formatted, 'price': price})
        return data

    def close_webdriver(self):
        self.driver.close()

    def run_crawler(self):
        filepath = os.path.join('../crawled_data', self.output_name, '.csv')

        self.start_webdriver()
        # gets the data
        data = self.access_the_data()
        # write the data
        write_as_csv(filepath, data)
        # close the driver
        self.close_webdriver()
