import time
import os
import csv
import datetime
import pandas as pd
import math

import trading_methodologies.trading_util as trading_util
from datetime import datetime

#one-off takes the amount of money to be spent, the date on which the investment is made and the portfolio as it should be balanced
# def write_as_csv(data): 
#     filename = 'trading_methodologies.csv'  
#     #file_path = os.path.join('crawled_data', self.output_name, '.csv')
#     with open(filename, 'w+', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Trading Method.", "Asset Alloc.", "Asset", "Amount($)", "Asset price", "# shares"])
#         for x in data:
#             writer.writerow(x)

def oneoff(startmoney, investment_date, timeframe):
    portfoliodf = trading_util.get_portfolio_dataframe()
    stocksdf, cbondsdf, sbondsdf, golddf, cashdf  = trading_util.dataframes_from_crawler()
    date_obj = datetime.strptime(investment_date, '%d/%m/%Y')
    money = startmoney
    timeframe = timeframe
   
    #testing with head
    # print("printing stocks dataframe")
    # print(stocksdf.head())
    # print("printing corporate bonds dataframe")
    # print(cbondsdf.head())
    # print("printing sovereign bonds dataframe")
    # print(sbondsdf.head())
    # print("printing gold dataframe")
    # print(golddf.head())
    # print("printing cash dataframe")
    # print(cashdf.head())
    # print("printing portfoliodf")
    # print(portfoliodf.head())


    
    stocksondate, stockprice = trading_util.find_data_point("stocks", date_obj)
    cbondondate, cbondprice = trading_util.find_data_point("cbonds", date_obj)
    sbondondate, sbondprice = trading_util.find_data_point("sbonds", date_obj)
    goldondate,  goldprice = trading_util.find_data_point("gold", date_obj)
    #cash price is 1 as per instructions
    cashprice = 1
    

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

        #set real spent money
        stock_money = round(stock_units*stockprice,2)
        cbond_money = round(cbond_units*cbondprice,2)
        sbond_money = round(sbond_units*sbondprice,2)
        gold_money = round(gold_units*goldprice,2)
        cash_money = round(cash_units*cashprice,2)
        
        #add data to array for later csv writing
        #Date, Trading Method.,Purchase ID,Asset Alloc.,Asset,Amount($),Asset price,#, Timeframe
        data = []
        data.append(tuple([date_obj.strftime('%d/%m/%Y'), "Oneoff", str(index+1) + ".ST", int(portf_alloc), "stocks", stock_money, stockprice, stock_units, stock_money, timeframe]))
        data.append(tuple([date_obj.strftime('%d/%m/%Y'), "Oneoff", str(index+1) + ".CB", int(portf_alloc), "cbonds", cbond_money, cbondprice, cbond_units, cbond_money, timeframe]))
        data.append(tuple([date_obj.strftime('%d/%m/%Y'), "Oneoff", str(index+1) + ".SB", int(portf_alloc), "sbonds", sbond_money, sbondprice, sbond_units, sbond_money, timeframe]))
        data.append(tuple([date_obj.strftime('%d/%m/%Y'), "Oneoff", str(index+1) + ".GO", int(portf_alloc), "gold", gold_money, goldprice, gold_units, gold_money, timeframe]))
        data.append(tuple([date_obj.strftime('%d/%m/%Y'), "Oneoff", str(index+1) + ".CA", int(portf_alloc), "cash", cash_money, cashprice, cash_units, cash_money, timeframe]))

        #write trading methodologies to CSV
        if timeframe == 12 and index == 0:
            trading_util.write_as_csv(data, "overwrite")
        else:
            trading_util.write_as_csv(data, "append")

    print("[SUCCESS] Oneoff")
