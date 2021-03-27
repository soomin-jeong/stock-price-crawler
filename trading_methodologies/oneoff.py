import time
import os
import csv
import datetime
import pandas as pd
import math

from datetime import datetime

#one-off takes the amount of money to be spent, the date on which the investment is made and the portfolio as it should be balanced
def write_as_csv(data): 
    filename = 'trading_methodologies.csv'  
    #file_path = os.path.join('crawled_data', self.output_name, '.csv')
    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Asset Alloc.", "Asset", "Amount($)", "Asset price", "# shares"])
        for x in data:
            writer.writerow(x)

def oneoff(startmoney, investment_date):
    portfoliodf = pd.read_csv('./portfolio_allocations.csv')
    stocksdf = pd.read_csv('./amundi-msci-wrld-ae-c.csv')
    cbondsdf = pd.read_csv('./ishares-global-corporate-bond-$.csv')
    sbondsdf = pd.read_csv('./db-x-trackers-ii-global-sovereign-5.csv')
    golddf = pd.read_csv('./spdr-gold-trust.csv')
    cashdf = pd.read_csv('./usdollar.csv')
    date_obj = datetime.strptime(investment_date, '%d/%m/%Y')
    money = startmoney
    #create trading_methodologies.csv
    #testing with head
    print("printing stocks dataframe")
    print(stocksdf.head())
    print("printing corporate bonds dataframe")
    print(cbondsdf.head())
    print("printing sovereign bonds dataframe")
    print(sbondsdf.head())
    print("printing gold dataframe")
    print(golddf.head())
    print("printing cash dataframe")
    print(cashdf.head())
    print("printing portfoliodf")
    print(portfoliodf.head())


    stockondate = stocksdf.loc[stocksdf['date'] == date_obj.strftime('%d/%m/%Y')]
    stockprice = stockondate.iloc[0]['price']
    #stockprice = stocksdf.loc[stocksdf['date'] == '30/12/2020']
    cbondondate = cbondsdf.loc[cbondsdf['date'] == date_obj.strftime('%d/%m/%Y')]
    cbondprice = cbondondate.iloc[0]['price']
    sbondondate = sbondsdf.loc[sbondsdf['date'] == date_obj.strftime('%d/%m/%Y')]
    sbondprice = sbondondate.iloc[0]['price']
    goldondate = golddf.loc[golddf['date'] == date_obj.strftime('%d/%m/%Y')]
    goldprice = goldondate.iloc[0]['price']
    # cashondate = cashdf.loc[cashdf['date'] == date_obj.strftime('%d/%m/%Y')]
    # cashprice = cashondate.iloc[0]['price']
    #cash price is 1 as per instructions
    cashprice = 1
    data = []

    for index, row in portfoliodf.iterrows():
        #get percent of each asset in portfolio
        portf_alloc = row['Asset Alloc.']
        stock_percentage = row['ST']
        cbond_percentage = row['CB']
        sbond_percentage = row['PB']
        gold_percentage = row['GO']
        cash_percentage = row['CA']

        #calculate how much of money should be spent on each asset
        stock_money = startmoney*stock_percentage
        cbond_money = startmoney*cbond_percentage
        sbond_money = startmoney*sbond_percentage
        gold_money = startmoney*gold_percentage
        cash_money = startmoney*cash_percentage

        #calculate units we can buy
        stock_units = math.floor(stock_money/stockprice)
        cbond_units = math.floor(cbond_money/cbondprice)
        sbond_units = math.floor(sbond_money/sbondprice)
        gold_units = math.floor(gold_money/goldprice)
        cash_units = math.floor(cash_money/cashprice)
        
        #add data to array for later csv writing
        data.append(tuple(["Oneoff", portf_alloc, stock_money, stockprice, stock_units]))
        data.append(tuple(["Oneoff", portf_alloc, cbond_money, cbondprice, cbond_units]))
        data.append(tuple(["Oneoff", portf_alloc, sbond_money, sbondprice, sbond_units]))
        data.append(tuple(["Oneoff", portf_alloc, gold_money, goldprice, gold_units]))
        data.append(tuple(["Oneoff", portf_alloc, cash_money, cashprice, cash_units]))

    #write trading methodologies to CSV
    write_as_csv(data)
    #print("stockprice on the date was " + str(stockprice) + " cbond price was " + str(cbondprice) + " the sbond price was  " +str(sbondprice))
    return 'Oneoff succeeded'