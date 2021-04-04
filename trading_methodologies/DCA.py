import time
import os
import csv
import datetime
import pandas as pd
import math
import calendar
import trading_methodologies.trading_util as trading_util
import trading_methodologies.rebalance as previous_rebalance

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

def DCA(startmoney, investment_date, investment_period, rebal):

    #floored division to find the amount to be invested per month
    money_per_month = math.floor(startmoney/investment_period)

    #create date object from date string
    date_obj = datetime.datetime.strptime(investment_date, '%d/%m/%Y')

    #test if we have data for the whole time period
    investment_pd_end_obj= add_months(date_obj, investment_period)
    date_obj, price = find_data_point("cbonds", investment_pd_end_obj)
    if (date_obj == None) or (price == None):
        return print("the specified date or investment period are outside of the dataset")
    
    #if we have the data we can continue
    #load the portfolio logic file
    portfoliodf = pd.read_csv('./portfolio_allocations.csv')

    #initialze empty list to recieve tuple of trading info
    data = []

    #iterate through every row of the portfolio file to get portfolio logic
    for index, row in portfoliodf.iterrows():
        #get portfolio logic data
        portf_alloc = row['Asset Alloc.']
        stock_percentage = row['ST']
        cbond_percentage = row['CB']
        sbond_percentage = row['PB']
        gold_percentage = row['GO']
        cash_percentage = row['CA']

        #calculate how much of money should be spent on each asset
        stock_money = money_per_month*stock_percentage
        cbond_money = money_per_month*cbond_percentage
        sbond_money = money_per_month*sbond_percentage
        gold_money = money_per_month*gold_percentage
        cash_money = money_per_month*cash_percentage

        #initialize empty dateframe to store previous trades if we need to access for rebalancing 
        columns =['ST_Q', 'ST_P', 'CB_Q', 'CB_P', 'SB_Q', 'SB_P', 'GO_Q', 'GO_P', 'CA_Q', 'CA_P', 'Money', 'Portf_Val']
        previous_rebalance =  pd.DataFrame(columns = columns)

        #execute trade with portfolio logic for every month of investment period
        for x in range(0,investment_period):
            
            print("DCA iterator value is: " + str(x))
            stock_date, stock_price = find_data_point("stocks", add_months(date_obj, x))
            cbond_date, cbond_price = find_data_point("cbonds", add_months(date_obj, x))
            sbond_date, sbond_price = find_data_point("sbonds", add_months(date_obj, x))
            gold_date, gold_price = find_data_point("gold", add_months(date_obj, x))
            cash_date  = find_data_point("cash", add_months(date_obj, x))[0]
            DCA_date = stock_date
            cash_price = 1

            #calculate units we can buy
            stock_units = math.floor(stock_money/stock_price)
            cbond_units = math.floor(cbond_money/cbond_price)
            sbond_units = math.floor(sbond_money/sbond_price)
            gold_units = math.floor(gold_money/gold_price)
            cash_units = math.floor(cash_money/cash_price)
            
            #add data to array for later csv writing
            data.append(tuple(["DCA", portf_alloc, stock_money, stock_price, stock_units]))
            data.append(tuple(["DCA", portf_alloc, cbond_money, cbond_price, cbond_units]))
            data.append(tuple(["DCA", portf_alloc, sbond_money, sbond_price, sbond_units]))
            data.append(tuple(["DCA", portf_alloc, gold_money, gold_price, gold_units]))
            data.append(tuple(["DCA", portf_alloc, cash_money, cash_price, cash_units]))
            
            #if we want to rebalance then we need to make sure to rebalance the whole portfolio
            if rebal == "TRUE":
                #add the current DCA trade to DF 
                print("entered if block for rebalance")
                trade_port_value = stock_units*stock_price + cbond_units*cbond_price + sbond_price*sbond_units + gold_units*gold_price + cash_units*cash_price
                trade_data = {
                    'ST_Q': stock_units,
                    'ST_P': stock_price,
                    'CB_Q': cbond_units,
                    'CB_P': cbond_price,
                    'SB_Q': sbond_units,
                    'SB_P': sbond_price,
                    'GO_Q': gold_units,
                    'GO_P': gold_price,
                    'CA_Q': cash_units,
                    'CA_P': cash_price,
                    'Money': 0,
                    'Portf_Val': trade_port_value
                    }

                previous_rebalance = previous_rebalance.append(trade_data, ignore_index=True)

                #The previous rebalance will be the sum of all previous trades in portfolio alloc so drop all the other trade except the last
                print("The dataframe length is" + str(len(previous_rebalance)))
                if len(previous_rebalance) == 4:
                    previous_rebalance = previous_rebalance.drop(previous_rebalance.index[0])

                #Sum of the columns
                Rebal_ST_Q = previous_rebalance['ST_Q'].sum()
                #Rebal_ST_P = previous_rebalance['ST_P'].sum()
                Rebal_CB_Q = previous_rebalance['CB_Q'].sum()
                #Rebal_CB_P = previous_rebalance['CB_P'].sum()
                Rebal_SB_Q = previous_rebalance['SB_Q'].sum()
                #Rebal_SB_P = previous_rebalance['SB_P'].sum()
                Rebal_GO_Q = previous_rebalance['GO_Q'].sum()
                #Rebal_GO_P = previous_rebalance['GO_P'].sum()
                Rebal_CA_Q = previous_rebalance['CA_Q'].sum()
                #Rebal_CA_P = previous_rebalance['CA_P'].sum()
                Rebal_Money = previous_rebalance['Money'].sum()
                Rebal_Portf_Val = previous_rebalance['Portf_Val'].sum()
                print("The sum of the portfolio value is " + str(Rebal_Portf_Val))
                
                #Execute rebalance
                rebalance.DCA_rebalance(Rebal_ST_Q, Rebal_CB_Q, Rebal_SB_Q, Rebal_GO_Q, Rebal_CA_Q, stock_percentage, cbond_percentage, sbond_percentage, gold_percentage, cash_percentage, Rebal_Money, DCA_date)
                #Write to dataframe

                #Add to data list to be written to CSV

        trading_util.write_as_csv(data, "append")
    return 'DCA has succeeded'



