import time
import os
import csv

from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime

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
        #self.driver = webdriver.Safari()
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        #self.driver = webdriver.Chrome()
        #self.driverdriver = webdriver.Chrome(ChromeDriverManager().install())
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
        print(table)
        time.sleep(1)

        # write data
        data = []
        for row in table:
            value = row.find_elements_by_tag_name("td")
            print(value)
            if (len(value) == 7):
                date = value[0].get_attribute('data-real-value')
                price = value[1].get_attribute('data-real-value')
                date_formatted = time.strftime("%D", time.localtime(int(date)))
                #tuples = {'date': time.strftime("%D", time.localtime(int(date))), 'price' : price}
                tuples = {date_formatted, price}
                print(tuples)
                data.append(tuples)
        return data

    def write_as_csv(self, data): 
        filename = 'crawled_data_' + self.output_name + datetime.now().strftime("%H%M%S") +'.csv'  
        #file_path = os.path.join('crawled_data', self.output_name, '.csv')
        with open(filename, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "price"])
            for x in data:
                writer.writerow(x)
            
        #with open(file_path, "a") as f:
            #f.write(data)

    def close_webdriver(self):
        self.driver.close()

    def run_crawler(self):
        self.start_webdriver()
        data = self.access_the_data()
        self.write_as_csv(data)
        self.close_webdriver()
