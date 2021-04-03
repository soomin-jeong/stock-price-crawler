import os
import csv
import time
import datetime
import pandas as pd
import math
import calendar

def write_as_csv(data, write_mode): 
    filename = 'trading_methodologies.csv'  
    #pass overwrite as argument to write the contents fresh
    if write_mode == "overwrite":
        with open(filename, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Trading Method.", "Purchase ID", "Asset Alloc.", "Asset", "Amount($)", "Asset price", "#"])
            for x in data:
                writer.writerow(x)
    #or pass append if you just want to write to the end of the file
    elif write_mode == "append":
        with open(filename, 'a+', newline='') as file:
            writer = csv.writer(file)
            for x in data:
                writer.writerow(x)

#add months adds months while dealing with end of the month cases where 31/30th is given as days input
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    end_date = datetime.date(year, month, day)
    return end_date

#add days adds days while dealing with changes in months    
def add_days(sourcedate, days_delta):
    #date_1 = datetime.datetime.strptime(sourcedate, "%d/%m/%Y")
    end_date = sourcedate + datetime.timedelta(days=days_delta)
    return end_date

def find_data_point(asset_class, sourcedate):
    date_on_date = None
    price_on_date = None
    data_source = None
    if (asset_class == "stocks"):
        data_source = pd.read_csv('./amundi-msci-wrld-ae-c.csv')
        print("loaded stock data")
    elif (asset_class == "cbonds"):
        data_source = pd.read_csv('./ishares-global-corporate-bond-$.csv')
        print("loaded cbond data")
    elif (asset_class == "sbonds"):
        data_source = pd.read_csv('./db-x-trackers-ii-global-sovereign-5.csv')
        print("loaded sbond data")
    elif (asset_class == "gold"):
        data_source = pd.read_csv('./spdr-gold-trust.csv')
        print("loaded gold data")
    elif (asset_class == "cash"):
        data_source = pd.read_csv('./usdollar.csv')
        print("loaded cash data")

    try: 
        info_for_date = data_source.loc[data_source['date'] == sourcedate.strftime('%d/%m/%Y')]
        price_on_date =  info_for_date.iloc[0]['price']
        date_on_date = sourcedate
        print ("on the date " + sourcedate.strftime('%d/%m/%Y') + " the asset " + str(asset_class) + " cost " + str(price_on_date))
    except: 
        #because there is no trading on the weekend if our investment is on the weekend we might not get data so we will try 
        #incrementing days till we arrive at monday 
        print("there is no data for " + sourcedate.strftime('%d/%m/%Y' + " this date may fall on the weekend. We will try to get data for Monday"))
        new_date = None
        for i in range(1, 4):
            try:
                #becuase incrementing dates could pring us to the next month we call add days function
                print("We incremented your date by:" + str(i))
                new_date = add_days(sourcedate,i)
                info_for_date = data_source.loc[data_source['date'] == new_date.strftime('%d/%m/%Y')]
                price_on_date =  info_for_date.iloc[0]['price']
                date_on_date = new_date
                print ("The date you're looking for may be on the weekend. On the date " + new_date.strftime('%d/%m/%Y') + " the asset " + str(asset_class) + " cost " + str(price_on_date))
                break
            except:
                print("there is no data for " + new_date.strftime('%d/%m/%Y'))

    return date_on_date, price_on_date
