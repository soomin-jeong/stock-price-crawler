import time
import os
import csv
import datetime
import pandas as pd
import math
import calendar
import trading_methodologies.trading_util as trading_util
import trading_methodologies.rebalance as rebalancer

def DCA(startmoney, investment_date, investment_period, rebal=False):

    #floored division to find the amount to be invested per month
    money_per_month = math.floor(startmoney/investment_period)

    #create date object from date string
    date_obj = datetime.datetime.strptime(investment_date, '%d/%m/%Y')

    #test if we have data for the whole time period
    #If we enter an investment period of 1 we would expect DCA to run only for that one month so we shouldnt add 1
    investment_pd_end_obj= trading_util.add_months(date_obj, (investment_period-1))
    date_obj, price = trading_util.find_data_point("cbonds", investment_pd_end_obj)
    if (date_obj == None) or (price == None):
        return print("the specified date or investment period are outside of the dataset")
    
    #reset date object to original investment date
    date_obj = datetime.datetime.strptime(investment_date, '%d/%m/%Y')

    #if we have the data we can continue
    #load the portfolio logic file
    portfoliodf = trading_util.get_portfolio_dataframe()

    #initialze empty list to recieve tuple of trading info
    #uncomment if you only want to write once at the end
    #data = []

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
        columns =['ST_M', 'ST_Q', 'ST_P', 'CB_M', 'CB_Q', 'CB_P', 'SB_M', 'SB_Q', 'SB_P', 'GO_M', 'GO_Q', 'GO_P', 'CA_M', 'CA_Q', 'CA_P', 'Money', 'Portf_Val']
        previous_trades =  pd.DataFrame(columns = columns)

        #execute trade with portfolio logic for every month of investment period
        for x in range(0,investment_period):
            
            #print("DCA iterator value is: " + str(x))
            stock_date, stock_price = trading_util.find_data_point("stocks", trading_util.add_months(date_obj, x))
            DCA_date = stock_date
            cbond_date, cbond_price = trading_util.find_data_point("cbonds", DCA_date)
            sbond_date, sbond_price = trading_util.find_data_point("sbonds", DCA_date)
            gold_date, gold_price = trading_util.find_data_point("gold", DCA_date)
            cash_date  = trading_util.find_data_point("cash", DCA_date)[0]
            cash_price = 1

            #calculate units we can buy
            stock_units = math.floor(stock_money/stock_price)
            cbond_units = math.floor(cbond_money/cbond_price)
            sbond_units = math.floor(sbond_money/sbond_price)
            gold_units = math.floor(gold_money/gold_price)
            cash_units = math.floor(cash_money/cash_price)

            #set the actual money spent
            stock_money = round(stock_price*stock_units,2)
            cbond_money = round(cbond_price*cbond_units,2)
            sbond_money = round(sbond_price*sbond_units,2)
            gold_money = round(gold_price*gold_units,2)
            cash_money = round(1*cash_units,2)
            
            #add the current DCA trade to DF 
            trade_port_value = stock_units*stock_price + cbond_units*cbond_price + sbond_price*sbond_units + gold_units*gold_price + cash_units*cash_price
            trade_data = {
                'ST_M': stock_money,
                'ST_Q': stock_units,
                'ST_P': stock_price,
                'CB_M': cbond_money,
                'CB_Q': cbond_units,
                'CB_P': cbond_price,
                'SB_M': sbond_money,
                'SB_Q': sbond_units,
                'SB_P': sbond_price,
                'GO_M': gold_money,
                'GO_Q': gold_units,
                'GO_P': gold_price,
                'CA_M': cash_money,
                'CA_Q': cash_units,
                'CA_P': cash_price,
                'Money': 0,
                'Portf_Val': trade_port_value
                }

            previous_trades = previous_trades.append(trade_data, ignore_index=True)
            #typecast to int/float
            previous_trades["ST_Q"] = pd.to_numeric(previous_trades["ST_Q"], errors='coerce')
            previous_trades["CB_Q"] = pd.to_numeric(previous_trades["CB_Q"], errors='coerce')
            previous_trades["SB_Q"] = pd.to_numeric(previous_trades["SB_Q"], errors='coerce')
            previous_trades["GO_Q"] = pd.to_numeric(previous_trades["GO_Q"], errors='coerce')
            previous_trades["CA_Q"] = pd.to_numeric(previous_trades["CA_Q"], errors='coerce')
            previous_trades["Money"] = pd.to_numeric(previous_trades["Money"], errors='coerce')
            previous_trades["Portf_Val"] = pd.to_numeric(previous_trades["Portf_Val"], errors='coerce')

            #calculate current holdings for one portfolio
            DCA_ST_M = previous_trades['ST_M'].sum()
            DCA_ST_Q = previous_trades['ST_Q'].sum()
            #DCA_ST_P = previous_trades['ST_P'].sum()
            DCA_CB_M = previous_trades['CB_M'].sum()
            DCA_CB_Q = previous_trades['CB_Q'].sum()
            #DCA_CB_P = previous_trades['CB_P'].sum()
            DCA_SB_M = previous_trades['SB_M'].sum()
            DCA_SB_Q = previous_trades['SB_Q'].sum()
            #DCA_SB_P = previous_trades['SB_P'].sum()
            DCA_GO_M = previous_trades['GO_M'].sum()
            DCA_GO_Q = previous_trades['GO_Q'].sum()
            #DCA_GO_P = previous_trades['GO_P'].sum()
            DCA_CA_M = previous_trades['CA_M'].sum()
            DCA_CA_Q = previous_trades['CA_Q'].sum()
            #DCA_CA_P = previous_trades['CA_P'].sum()
            DCA_Money = previous_trades['Money'].sum()
            DCA_Portf_Val = previous_trades['Portf_Val'].sum()

            #depending on what type of trade this is the trade methodology needs to be changed for the csv so we can identify it later
            if rebal:
                trade_type = "DCA-rebalance"
            else:
                trade_type = "DCA"
            #add data to array for later csv writing
            data = []
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), trade_type, str(int(portf_alloc)) + ".ST", int(portf_alloc), "stocks", round(DCA_ST_M,2), stock_price, DCA_ST_Q, stock_money, investment_period]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), trade_type, str(int(portf_alloc)) + ".CB", int(portf_alloc), "cbonds", round(DCA_CB_M,2), cbond_price, DCA_CB_Q, cbond_money, investment_period]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), trade_type, str(int(portf_alloc)) + ".SB", int(portf_alloc), "sbonds", round(DCA_SB_M,2), sbond_price, DCA_SB_Q, sbond_money, investment_period]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), trade_type, str(int(portf_alloc)) + ".GO", int(portf_alloc), "gold", round(DCA_GO_M,2), gold_price, DCA_GO_Q, gold_money, investment_period]))
            data.append(tuple([DCA_date.strftime('%d/%m/%Y'), trade_type, str(int(portf_alloc)) + ".CA", int(portf_alloc), "cash", round(DCA_CA_M,2), cash_price, DCA_CA_Q, cash_money, investment_period]))
            trading_util.write_as_csv(data, "append")

            #write all data to a single line
            #data.append(tuple([date_obj.strftime('%d/%m/%Y'), "Oneoff", str(index+1) + ".ST", int(portf_alloc), "stocks", stock_money, stockprice, stock_units, "cbonds", cbond_money, cbondprice, cbond_units, "sbonds", sbond_money, sbondprice, sbond_units, "gold", gold_money, goldprice, gold_units, "cash", cash_money, cashprice, cash_units, timeframe]))
            #data.append(tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "ST", portf_alloc, "stocks", stock_money, stock_price, stock_units, "cbonds", cbond_money, cbond_price, cbond_units, "sbonds", sbond_money, sbond_price, sbond_units, "gold", gold_money, gold_price, gold_units, "cash", cash_money, cash_price, cash_units, investment_period]))
            #write to csv now 
            #data = (tuple([DCA_date.strftime('%d/%m/%Y'), "DCA", str(portf_alloc) + "ST", portf_alloc, "stocks", stock_money, stock_price, stock_units, "cbonds", cbond_money, cbond_price, cbond_units, "sbonds", sbond_money, sbond_price, sbond_units, "gold", gold_money, gold_price, gold_units, "cash", cash_money, cash_price, cash_units, investment_period]))
            
            #if we want to rebalance then we need to make sure to rebalance the whole portfolio
            if rebal:
                
                #to-do: get rid of this but only write additions/subtractions of rebal
                #The previous rebalance will be the sum of all previous trades in portfolio alloc so drop all the other trade except the last
                #print("The dataframe length is" + str(len(previous_trades)))
                if len(previous_trades) == 4:
                    previous_trades = previous_trades.drop(previous_trades.index[0])

                #Sum of the columns
                Rebal_ST_Q = previous_trades['ST_Q'].sum()
                #Rebal_ST_P = previous_trades['ST_P'].sum()
                Rebal_CB_Q = previous_trades['CB_Q'].sum()
                #Rebal_CB_P = previous_trades['CB_P'].sum()
                Rebal_SB_Q = previous_trades['SB_Q'].sum()
                #Rebal_SB_P = previous_trades['SB_P'].sum()
                Rebal_GO_Q = previous_trades['GO_Q'].sum()
                #Rebal_GO_P = previous_trades['GO_P'].sum()
                Rebal_CA_Q = previous_trades['CA_Q'].sum()
                #Rebal_CA_P = previous_trades['CA_P'].sum()
                Rebal_Money = previous_trades['Money'].sum()
                Rebal_Portf_Val = previous_trades['Portf_Val'].sum()
                #print("The sum of the portfolio value is " + str(Rebal_Portf_Val))
                
                #Execute rebalance
                #"DCA rebalance succeeded", final_quant_stock, price_of_rebalance_stocks, final_quant_cbonds, price_of_rebalance_cbonds, final_quant_sbonds, price_of_rebalance_sbonds, final_quant_gold, price_of_rebalance_gold, final_quant_cash, price_of_rebalance_cash, money_from_sales, rebal_portf_value
                result = rebalancer.DCA_rebalance(Rebal_ST_Q, Rebal_CB_Q, Rebal_SB_Q, Rebal_GO_Q, Rebal_CA_Q, stock_percentage, cbond_percentage, sbond_percentage, gold_percentage, cash_percentage, Rebal_Money, DCA_date)
                #print(result)

                #if we get an error we only get the error message back 
                message = result[0]
                #print(message)
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
                invest_buy_stocks = result[14]
                invest_buy_cbonds = result[15]
                invest_buy_sbonds = result[16]
                invest_buy_gold = result[17]
                invest_buy_cash = result[18]
                
                #to-do
                #Write to dataframe
                trade_data = {
                    'ST_M': 0,
                    'ST_Q': stock_units,
                    'ST_P': stock_price,
                    'CB_M': 0,
                    'CB_Q': cbond_units,
                    'CB_P': cbond_price,
                    'SB_M': 0,
                    'SB_Q': sbond_units,
                    'SB_P': sbond_price,
                    'GO_M': 0,
                    'GO_Q': gold_units,
                    'GO_P': gold_price,
                    'CA_M': 0,
                    'CA_Q': cash_units,
                    'CA_P': cash_price,
                    'Money': Rebal_Money,
                    'Portf_Val': trade_port_value
                    }

                previous_trades = previous_trades.append(trade_data, ignore_index=True)
                #Add to data list to be written to CSV
                data = []
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(int(portf_alloc)) + ".ST", int(portf_alloc), "stocks", stock_money, stock_price, int(stock_units), invest_buy_stocks, investment_period]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(int(portf_alloc)) + ".CB", int(portf_alloc), "cbonds", cbond_money, cbond_price, int(cbond_units), invest_buy_cbonds, investment_period]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(int(portf_alloc)) + ".SB", int(portf_alloc), "sbonds", sbond_money, sbond_price, int(sbond_units), invest_buy_sbonds, investment_period]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(int(portf_alloc)) + ".GO", int(portf_alloc), "gold", gold_money, gold_price, int(gold_units), invest_buy_gold, investment_period]))
                data.append(tuple([date_of_rebalance.strftime('%d/%m/%Y'), "DCA-rebalance", str(int(portf_alloc)) + ".CA", int(portf_alloc), "cash", cash_money, cash_price, int(cash_units), invest_buy_cash, investment_period]))
                ##uncomment for debugging
                #print("current portfolio ID is" + str(portf_alloc))
                ##for testing it may be helpful to write to the csv within the loop
                #trading_util.write_as_csv(data, "append")
                trading_util.write_as_csv(data, "append")
    return 'DCA has succeeded'



