
import csv


def write_as_csv(filepath, data):
    if filepath.split('.')[-1] != 'csv':
        filepath = filepath.split('.')[:-1] + '.csv'

    with open(filepath, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "price"])
        for x in data:
            writer.writerow(x)
