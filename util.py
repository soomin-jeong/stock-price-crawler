import time
import os

from selenium import webdriver

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
        self.driver = webdriver.Chrome()
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
        time.sleep(1);

        # write data
        data = []
        for row in table:
            value = row.find_elements_by_tag_name("td")
            if (len(value) == 7):
                date = value[0].get_attribute('data-real-value')
                price = value[1].get_attribute('data-real-value')
                tuples = {'date': time.strftime("%D", time.localtime(int(date))), 'price' : price}
                print(tuples)
                data.append(tuples)
        return data

    def write_as_csv(self, data):
        file_path = os.path.join('crawled_data', self.output_name)
        with open(file_path, "a") as f:
            f.write(data)

    def close_webdriver(self):
        self.driver.close()

    def run_crawler(self):
        self.start_webdriver()
        data = self.access_the_data()
        #self.write_as_csv(data)
        self.close_webdriver()
