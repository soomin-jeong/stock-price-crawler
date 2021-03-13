import time
import os

from selenium import webdriver

# Date range to search
START_DATE = '01/01/2020'
END_DATE = '12/31/2020'


class Crawler(object):
    def __init__(self, start_page, output_name):
        self.start_page = start_page
        self.output_name = output_name
        self.driver = None

    def start_webdriver(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.start_page)
        time.sleep(3)

    def access_the_data(self):
        # TODO: click calendar Icon
        self.driver.find_element_by_id("datePickerIconWrap")


        # TODO: set timeframe


        # TODO: click button apply


        # TODO: extract info from HTML Table. Need only date and info in column price. All else can be discarded
        data = ''


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
        self.write_as_csv(data)
        self.close_webdriver()
