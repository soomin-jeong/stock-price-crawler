import os
import csv


def write_as_csv(data): 
    filename = 'trading_methodologies1.csv'  
    #file_path = os.path.join('crawled_data', self.output_name, '.csv')
    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Trading Method.", "Asset Alloc.", "Asset", "Amount($)", "Asset price", "# shares"])
        for x in data:
            writer.writerow(x)