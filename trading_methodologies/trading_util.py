import os
import csv


def write_as_csv(data, write_mode): 
    filename = 'trading_methodologies.csv'  
    #pass overwrite as argument to write the contents fresh
    if write_mode == "overwrite":
        with open(filename, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Trading Method.", "Asset Alloc.", "Asset", "Amount($)", "Asset price", "# shares"])
            for x in data:
                writer.writerow(x)
    #or pass append if you just want to write to the end of the file
    elif write_mode == "append":
        with open(filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Trading Method.", "Asset Alloc.", "Asset", "Amount($)", "Asset price", "# shares"])
            for x in data:
                writer.writerow(x)