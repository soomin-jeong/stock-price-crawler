import time
import os
import csv
import datetime
import pandas as pd
import math
import calendar
import trading_methodologies.trading_util as trading_util
import trading_methodologies.rebalance as rebalancer

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
        data_source = pd.read_csv('./crawled_data/amundi-msci-wrld-ae-c.csv')
        print("loaded stock data")
    elif (asset_class == "cbonds"):
        data_source = pd.read_csv('./crawled_data/ishares-global-corporate-bond-$.csv')
        print("loaded cbond data")
    elif (asset_class == "sbonds"):
        data_source = pd.read_csv('./crawled_data/db-x-trackers-ii-global-sovereign-5.csv')
        print("loaded sbond data")
    elif (asset_class == "gold"):
        data_source = pd.read_csv('./crawled_data/spdr-gold-trust.csv')
        print("loaded gold data")
    elif (asset_class == "cash"):
        data_source = pd.read_csv('./crawled_data/usdollar.csv')
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
    portfoliodf = pd.read_csv('./crawled_data/portfolio_allocations.csv')

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
            DCA_date = stock_date
            cbond_date, cbond_price = find_data_point("cbonds", DCA_date)
            sbond_date, sbond_price = find_data_point("sbonds", DCA_date)
            gold_date, gold_price = find_data_point("gold", DCA_date)
            cash_date  = find_data_point("cash", DCA_date)[0]
            cash_price = 1

            #calculate units we can buy
            stock_units = math.floor(stock_money/stock_price)
            cbond_units = math.floor(cbond_money/cbond_price)
            sbond_units = math.floor(sbond_money/sbond_price)
            gold_units = math.floor(gold_money/gold_price)
            cash_units = math.floor(cash_money/cash_price)
            
            #add data to array for later csv writing
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "ST", portf_alloc, "stocks", stock_money, stock_price, stock_units]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "CB", portf_alloc, "cbonds", cbond_money, cbond_price, cbond_units]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "SB", portf_alloc, "sbonds", sbond_money, sbond_price, sbond_units]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "GO", portf_alloc, "gold", gold_money, gold_price, gold_units]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "CA", portf_alloc, "cash", cash_money, cash_price, cash_units]))
            
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
                #pd.show_versions()
                #typecast to int/float
                #previous_rebalance = previous_rebalance.apply(pd.to_numeric)
                #previous_rebalance[['ST_Q', 'CB_Q']] = previous_rebalance[['ST_Q', 'CB_Q']].apply(pd.to_numeric)
                #above two raise errors
                previous_rebalance["ST_Q"] = pd.to_numeric(previous_rebalance["ST_Q"], errors='coerce')
                previous_rebalance["CB_Q"] = pd.to_numeric(previous_rebalance["CB_Q"], errors='coerce')
                previous_rebalance["SB_Q"] = pd.to_numeric(previous_rebalance["SB_Q"], errors='coerce')
                previous_rebalance["GO_Q"] = pd.to_numeric(previous_rebalance["GO_Q"], errors='coerce')
                previous_rebalance["CA_Q"] = pd.to_numeric(previous_rebalance["CA_Q"], errors='coerce')
                previous_rebalance["Money"] = pd.to_numeric(previous_rebalance["Money"], errors='coerce')
                previous_rebalance["Portf_Val"] = pd.to_numeric(previous_rebalance["Portf_Val"], errors='coerce')

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
                #"DCA rebalance succeeded", final_quant_stock, price_of_rebalance_stocks, final_quant_cbonds, price_of_rebalance_cbonds, final_quant_sbonds, price_of_rebalance_sbonds, final_quant_gold, price_of_rebalance_gold, final_quant_cash, price_of_rebalance_cash, money_from_sales, rebal_portf_value
                result = rebalancer.DCA_rebalance(Rebal_ST_Q, Rebal_CB_Q, Rebal_SB_Q, Rebal_GO_Q, Rebal_CA_Q, stock_percentage, cbond_percentage, sbond_percentage, gold_percentage, cash_percentage, Rebal_Money, DCA_date)
                print(result)

                #if we get an error we only get the error message back 
                message = result[0]
                print(message)
                if message == "there is an error. Has the end of the available asset data been reached?":
                    continue

                #otherwise continue and assign the return values
                stock_units = result[1]
                stock_price = result[2]
                cbond_units = result[3]
                cbond_price = result[4]
                sbond_units = result[5]
                sbond_price = result[6]
                gold_units = result[7]
                gold_price = result[8]
                cash_units = result[9]
                cash_price = result[10]
                Rebal_Money = result[11]
                trade_port_value = result[12]
                date_of_rebalance = result[13]
                
                #Write to dataframe
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
                    'Money': Rebal_Money,
                    'Portf_Val': trade_port_value
                    }

                previous_rebalance = previous_rebalance.append(trade_data, ignore_index=True)
                #Add to data list to be written to CSV
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(portf_alloc) + ".ST", portf_alloc, "stocks", stock_money, stock_price, stock_units]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(portf_alloc) + ".CB", portf_alloc, "cbonds", cbond_money, cbond_price, cbond_units]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(portf_alloc) + ".SB", portf_alloc, "sbonds", sbond_money, sbond_price, sbond_units]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(portf_alloc) + ".GO", portf_alloc, "gold", gold_money, gold_price, gold_units]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(portf_alloc) + ".CA", portf_alloc, "cash", cash_money, cash_price, cash_units]))

        trading_util.write_as_csv(data, "append")
    return 'DCA has succeeded'



