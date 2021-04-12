
import csv


class PortfolioGeneartor:
    # Portfolio allocation which automatically generates data
    def generate_allocation(self):
        data = []
        for ca in range(0,21):
            caValue = (ca*5)
            for go in range(0,21):
                goValue = (go*5)
                for pb in range(0,21):
                    pbValue = (pb*5)
                    for cb in range(0,21):
                        cbValue = (cb*5)
                        for st in range(0,21):
                            stValue = (st * 5)
                            if ((pbValue + stValue + cbValue + goValue + caValue) == 100):
                                tuples = (len(data) + 1, pbValue/100, stValue/100, cbValue/100, goValue/100, caValue/100)
                                data.append(tuples)
        return data

    def write_as_csv(self, data):
        filename = 'portfolio_allocations'+'.csv'
        with open(filename, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Asset Alloc.", "ST", "CB", "PB", "GO", "CA"])
            for x in data:
                writer.writerow(x)


portfolio_generator = PortfolioGeneartor()
