import time
import os
import csv
import datetime
import pandas as pd
import math
import calendar

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
    

def DCA(startmoney, investment_date, investment_period):
    
    #load crawler data
    # portfoliodf = pd.read_csv('./portfolio_allocations.csv')
    # #stocksdf = pd.read_csv('./amundi-msci-wrld-ae-c.csv')
    # cbondsdf = pd.read_csv('./ishares-global-corporate-bond-$.csv')
    # print(cbondsdf)
    # sbondsdf = pd.read_csv('./db-x-trackers-ii-global-sovereign-5.csv')
    # golddf = pd.read_csv('./spdr-gold-trust.csv')
    # cashdf = pd.read_csv('./usdollar.csv')

    #floored division to find the amount to be invested per month
    money_per_month = startmoney//investment_period
    #create date object from date string
    date_obj = datetime.datetime.strptime(investment_date, '%d/%m/%Y')
    #test if we have data for the whole time period
    investment_pd_end_obj= add_months(date_obj, investment_period)
    date_obj, price = find_data_point("cbonds", investment_pd_end_obj)
    if (date_obj == None) or (price == None):
        return print("the specified date or investment period are outside of the dataset")
    else:
        find_data_point("cbonds", date_obj)
    # print(investment_pd_end_obj)
    # print(investment_pd_end_obj.strftime('%d/%m/%Y'))


    # try: 
    #     #stockondate = stocksdf.loc[stocksdf['date'] == investment_pd_end_obj.strftime('%d/%m/%Y')]
    #     #stockprice = stocksdf.loc[stocksdf['date'] == '30/12/2020']
    #     cbondondate = cbondsdf.loc[cbondsdf['date'] == investment_pd_end_obj.strftime('%d/%m/%Y')]
    #     print(cbondondate)
    #     cbondprice = cbondondate.iloc[0]['price']
    #     print(cbondprice)
    #     # sbondondate = sbondsdf.loc[sbondsdf['date'] == investment_pd_end_obj.strftime('%d/%m/%Y')]
    #     # sbondprice = sbondondate.iloc[0]['price']
    #     # goldondate = golddf.loc[golddf['date'] == investment_pd_end_obj.strftime('%d/%m/%Y')]
    #     # goldprice = goldondate.iloc[0]['price']

        

    # except:
    #     return print("error, there is not enough data for your investment period")

    #for x in investment_period:

    return 'DCA'



