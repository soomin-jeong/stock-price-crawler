import csv
import pandas as pd
import datetime
import trading_methodologies.trading_util as trading_util
import math


def oneoff_rebalance(investment_period):
    #load our CSV data files
    portfoliodf = trading_util.get_portfolio_dataframe()
    tradedatadf = pd.read_csv('trading_methodologies/trading_methodologies.csv', low_memory=False)
    stocksdf,cbondsdf, sbondsdf, golddf, cashdf =  trading_util.dataframes_from_crawler()
   
    #load all trade data which was made with oneoff method
    oneoff_trades_df = tradedatadf.loc[(tradedatadf['Trading Method.'] == "Oneoff") & (tradedatadf['Timeframe'] == investment_period)]
    
    ##uncomment for debugging
    #print("printing oneoff_trades_df dataframe")
    #print(oneoff_trades_df.head())

    # Get a series of unique values in column 'portfolio ID' of the dataframe
    #returns nparray object whcih we convert to list
    z = oneoff_trades_df['Asset Alloc.'].unique()
    portfolio_allocation_IDs = z.tolist()
    # using list comprehension to perform str to int conversion
    portfolio_allocation_IDs = [int(i) for i in portfolio_allocation_IDs]
    
    ##uncomment for debugging
    # print("printing portfolio_allocation_IDs list")
    # print(portfolio_allocation_IDs[:5])
    # print(len(portfolio_allocation_IDs))

    #prepare data array to write to CSV at the end
    #moved into for loop so the scope is smaller and we can write to csv after every loop. Less efficient if we run the whole thing but if we 
    #dont want to write all 150k lines every time this is better
    data = []

    for i in portfolio_allocation_IDs:
        
        pointer = i-1

        #get target allocation

        ##uncomment for debugging
        # print("the value of i is " + str(i))
        # print("the value of the pointer is " + str(pointer))
        # print("the stored value of the portfolio at pointer is " + str(portfolio_allocation_IDs[pointer]))
        # print(portfolio_allocation_IDs[pointer])

        
        target_alloc_df = portfoliodf.loc[portfoliodf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])]
        target_alloc_stocks = target_alloc_df.iloc[0]['ST']
        target_alloc_cbonds = target_alloc_df.iloc[0]['CB']
        target_alloc_sbonds = target_alloc_df.iloc[0]['PB']
        target_alloc_gold = target_alloc_df.iloc[0]['GO']
        target_alloc_cash = target_alloc_df.iloc[0]['CA']

        #get trade amount for each allocation
        initial_quant_stocks = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "stocks")].iloc[0]['#']
        initial_quant_cbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cbonds")].iloc[0]['#']
        initial_quant_sbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "sbonds")].iloc[0]['#']
        initial_quant_gold = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "gold")].iloc[0]['#']
        initial_quant_cash = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cash")].iloc[0]['#']
        
        ##uncomment for debugging
        #print("Your current portfolio consists of " + str(initial_quant_stocks) + " stock units " + str(initial_quant_cbonds)+ " cbond units " + str(initial_quant_sbonds) +" sbond units " + str(initial_quant_gold) + " gold units " + str(initial_quant_cash) + " cash units")

        #get initial investment date
        initial_date = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cbonds")].iloc[0]['Date']
        initial_date_obj = datetime.datetime.strptime(initial_date, '%d/%m/%Y')
        #rebalance for the first time in the same month on the 15th
        rebalance_initial_date = datetime.date(initial_date_obj.year, initial_date_obj.month, 15)
        
        ##uncomment for debugging
        #print("the date of the first rebalance is " + str(rebalance_initial_date))

        #initialize empty dateframe which can be overwritten with rebalance data 
        #columns =['ST_M', 'ST_Q', 'ST_P', 'CB_M', 'CB_Q', 'CB_P', 'SB_M', 'SB_Q', 'SB_P', 'GO_M', 'GO_Q', 'GO_P', 'CA_M', 'CA_Q', 'CA_P', 'Money', 'Portf_Val']
        empty_df = pd.DataFrame()
        previous_rebalance = empty_df
        # previous_rebalance = pd.DataFrame(index = [0, 1], columns = ['Asset Alloc.', 'Asset', '#'])
        # previous_rebalance = previous_rebalance.fillna(method='ffill')
        # print(previous_rebalance)

        #loop through investment period and rebalance
        for y in range(0, int(investment_period)):
            
            data = []

            #if the initial investment is made after the 15th we dont rebalnce in the current month
            
            ##uncomment for debugging
            # print("the investment period is " + str(investment_period))
            # print("the day of the date of the initial trade is " + str(initial_date_obj.day))
            # print("my y value is " + str(y))
            if initial_date_obj.day > 15:
                y = y + 1
            
            #if we previously rebalanced we need to use that data and not the original trade data
            #get trade amount for each rebalance 
            if previous_rebalance.empty == False:
                initial_quant_stocks = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "stocks")].iloc[0]['#']
                initial_quant_cbonds = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "cbonds")].iloc[0]['#']
                initial_quant_sbonds = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "sbonds")].iloc[0]['#']
                initial_quant_gold = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "gold")].iloc[0]['#']
                initial_quant_cash = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "cash")].iloc[0]['#']
                rebal_value_of_stocks = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "stocks")].iloc[0]['Asset Money']
                rebal_value_of_cbonds = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "cbonds")].iloc[0]['Asset Money']
                rebal_value_of_sbonds = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "sbonds")].iloc[0]['Asset Money']
                rebal_value_of_gold = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "gold")].iloc[0]['Asset Money']
                rebal_value_of_cash = previous_rebalance.loc[(previous_rebalance['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (previous_rebalance['Asset'] == "cash")].iloc[0]['Asset Money']
                ##uncomment for debugging
                #print("Your portfolio was previously rebalanced. It consists of " + str(initial_quant_stocks) + " stock units " + str(initial_quant_cbonds)+ " cbond units " + str(initial_quant_sbonds) +" sbond units " + str(initial_quant_gold) + " gold units " + str(initial_quant_cash) + " cash units")
            
            #we need to write the original trade to the csv as a rebalance trade too so that it will be counted in our performance analysis
            if previous_rebalance.empty == True:
                rebal_value_of_stocks = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "stocks")].iloc[0]['Amount($)']
                price_of_rebalance_stocks = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "stocks")].iloc[0]['Asset price']
                rebal_value_of_cbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cbonds")].iloc[0]['Amount($)']
                price_of_rebalance_cbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cbonds")].iloc[0]['Asset price']
                rebal_value_of_sbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "sbonds")].iloc[0]['Amount($)']
                price_of_rebalance_sbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "sbonds")].iloc[0]['Asset price']
                rebal_value_of_gold = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "gold")].iloc[0]['Amount($)']
                price_of_rebalance_gold = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "gold")].iloc[0]['Asset price']
                rebal_value_of_cash = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cash")].iloc[0]['Amount($)']
                price_of_rebalance_cash = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[pointer])) & (tradedatadf['Asset'] == "cash")].iloc[0]['Asset price']
                
                data.append(tuple([initial_date_obj.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".ST", portfolio_allocation_IDs[pointer], "stocks", rebal_value_of_stocks, price_of_rebalance_stocks, initial_quant_stocks, rebal_value_of_stocks, investment_period]))
                data.append(tuple([initial_date_obj.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".CB", portfolio_allocation_IDs[pointer], "cbonds", rebal_value_of_cbonds, price_of_rebalance_cbonds, initial_quant_cbonds, rebal_value_of_cbonds, investment_period]))
                data.append(tuple([initial_date_obj.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".SB", portfolio_allocation_IDs[pointer], "sbonds", rebal_value_of_sbonds, price_of_rebalance_sbonds, initial_quant_sbonds, rebal_value_of_sbonds, investment_period]))
                data.append(tuple([initial_date_obj.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".GO", portfolio_allocation_IDs[pointer], "gold", rebal_value_of_gold, price_of_rebalance_gold, initial_quant_gold, rebal_value_of_gold, investment_period]))
                data.append(tuple([initial_date_obj.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".CA", portfolio_allocation_IDs[pointer], "cash", rebal_value_of_cash, 1, initial_quant_cash, rebal_value_of_cash, investment_period]))

                pandas_data = {
                'Asset Alloc.': [int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer])],
                'Asset': ['stocks', 'cbonds','sbonds', 'gold', 'cash'],
                'Asset Money' : [rebal_value_of_stocks, rebal_value_of_cbonds, rebal_value_of_sbonds, rebal_value_of_gold, rebal_value_of_cash],
                '#':  [initial_quant_stocks, initial_quant_cbonds, initial_quant_sbonds, initial_quant_gold, initial_quant_cash]
                }
                previous_rebalance = pd.DataFrame (pandas_data, columns = ['Asset Alloc.', 'Asset', 'Asset Money', '#'])
                
            #get the current prices/values of assets
            date_of_rebalance, price_of_rebalance_cbonds = trading_util.find_data_point("cbonds", trading_util.add_months(rebalance_initial_date, y))
            
            #if we have reached the end of our available data exit the loop
            if price_of_rebalance_cbonds == None:
                break
            #make the program more efficient by using date where we know we have data as tested with cbonds above instead of the 15th
            price_of_rebalance_stocks = trading_util.find_data_point("stocks", date_of_rebalance)[1]
            price_of_rebalance_sbonds = trading_util.find_data_point("sbonds", date_of_rebalance)[1]
            price_of_rebalance_gold = trading_util.find_data_point("gold", date_of_rebalance)[1]
            #cash is always valued at 1 USD as per instructions
            price_of_rebalance_cash = 1
            
            #calculate the total value of each asset in our portfolio
            rebal_value_of_cbonds = price_of_rebalance_cbonds*initial_quant_cbonds
            rebal_value_of_stocks = price_of_rebalance_stocks*initial_quant_stocks
            rebal_value_of_sbonds = price_of_rebalance_sbonds*initial_quant_sbonds
            rebal_value_of_gold = price_of_rebalance_gold*initial_quant_gold
            rebal_value_of_cash = 1*initial_quant_cash
            #calculate the current value of our portfolio
            rebal_portf_value =  rebal_value_of_cbonds + rebal_value_of_stocks + rebal_value_of_sbonds + rebal_value_of_gold + rebal_value_of_cash
            
            ##uncomment for debugging
            #print("the current total value of the protfolio is " + str(rebal_portf_value))


            #calculate weights in portfolio
            # weight_stocks = rebal_value_of_stocks/rebal_portf_value
            # weight_cbonds = rebal_value_of_cbonds/rebal_portf_value
            # weight_sbonds = rebal_value_of_sbonds/rebal_portf_value
            # weight_gold = rebal_value_of_gold/rebal_portf_value
            # weight_cash = rebal_value_of_cash/rebal_portf_value

            #calculate the value that should be assigned to each asset
            opt_val_stocks = rebal_portf_value*target_alloc_stocks
            opt_val_cbonds = rebal_portf_value*target_alloc_cbonds
            opt_val_sbonds = rebal_portf_value*target_alloc_sbonds
            opt_val_gold = rebal_portf_value*target_alloc_gold
            opt_val_cash = rebal_portf_value*target_alloc_cash

            #calculate the amount of each asset that we should have in the balanced portfolio
            opt_quant_stocks = math.floor(opt_val_stocks/price_of_rebalance_stocks)
            opt_quant_cbonds = math.floor(opt_val_cbonds/price_of_rebalance_cbonds)
            opt_quant_sbonds = math.floor(opt_val_sbonds/price_of_rebalance_sbonds)
            opt_quant_gold = math.floor(opt_val_gold/price_of_rebalance_gold)
            opt_quant_cash = math.floor(opt_val_cash/1)
            #print reminder of current portfolio composition for debugging
            ##uncomment for debugging
            #print("Your balanced portfolio should have " + str(opt_quant_stocks) + " stock units " + str(opt_quant_cbonds)+ " cbond units " + str(opt_quant_sbonds) +" sbond units " + str(opt_quant_gold) + " gold units " + str(opt_quant_cash) + " cash units " )
            #print("Your current portfolio consists of " + str(initial_quant_stocks) + " stock units " + str(initial_quant_cbonds)+ " cbond units " + str(initial_quant_sbonds) +" sbond units " + str(initial_quant_gold) + " gold units " + str(initial_quant_cash) + " cash units")

            #calculate deltas between optimum and current quantity
            delta_quant_stocks = opt_quant_stocks -initial_quant_stocks 
            delta_quant_cbonds = opt_quant_cbonds -initial_quant_cbonds
            delta_quant_sbonds = opt_quant_sbonds - initial_quant_sbonds
            delta_quant_gold =  opt_quant_gold - initial_quant_gold
            delta_quant_cash = opt_quant_cash - initial_quant_cash


            #if there is no need to rebalance then do not run the rest of the loop
            #still write the first oneoff trade as rebalance
            if delta_quant_stocks == 0 and delta_quant_cbonds==0 and delta_quant_sbonds==0 and delta_quant_gold==0 and delta_quant_cash==0: 
                ##uncomment for debugging
                #print("Your portfolio is balanced")
                trading_util.write_as_csv(data, "append")
                continue

            final_quant_stock = final_quant_cbonds = final_quant_sbonds = final_quant_gold = final_quant_cash = money_from_sales = 0
            purchase_value_stocks = purchase_value_cbonds  = purchase_value_sbonds = purchase_value_gold = purchase_value_cash = float(0)

            #conduct sales if needed
            if delta_quant_stocks < 0:
                purchase_value_stocks = round(delta_quant_stocks*price_of_rebalance_stocks,2)
                money_from_sales = money_from_sales + abs(purchase_value_stocks)
                final_quant_stock = initial_quant_stocks + delta_quant_stocks
                ##uncomment for debugging
                #print("stocks sold. The new amount of stocks held is " + str(final_quant_stock) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_cbonds < 0:
                purchase_value_cbonds = round(delta_quant_cbonds*price_of_rebalance_cbonds,2)
                money_from_sales = money_from_sales + abs(purchase_value_cbonds)
                final_quant_cbonds = initial_quant_cbonds + delta_quant_cbonds
                ##uncomment for debugging
                #print("cbonds sold. The new amount of cbonds held is " + str(final_quant_cbonds) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_sbonds < 0:
                purchase_value_sbonds = round(delta_quant_sbonds*price_of_rebalance_sbonds,2)
                money_from_sales = money_from_sales + abs(purchase_value_sbonds)
                final_quant_sbonds = initial_quant_sbonds + delta_quant_sbonds
                ##uncomment for debugging
                #print("sbonds sold. The new amount of sbonds held is " + str(final_quant_sbonds) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_gold < 0:
                purchase_value_gold = round(delta_quant_gold*price_of_rebalance_gold,2)
                money_from_sales = money_from_sales + abs(purchase_value_gold)
                final_quant_gold = initial_quant_gold + delta_quant_gold
                ##uncomment for debugging
                #print("gold sold. The new amount of gold held is " + str(final_quant_gold) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_cash < 0:
                purchase_value_gold = round(delta_quant_cash*price_of_rebalance_cash,2)
                money_from_sales = money_from_sales + abs(purchase_value_gold)
                final_quant_cash = initial_quant_cash + delta_quant_cash
                ##uncomment for debugging
                #print("cash sold. The new amount of cash held is " + str(final_quant_cash) + " your current spendable balance is " + str(money_from_sales))
            
            #conduct purchases with money_from_sales
            if delta_quant_stocks > 0:
                purchase_value_stocks = round(delta_quant_stocks*price_of_rebalance_stocks,2)
                if purchase_value_stocks < money_from_sales:
                    money_from_sales = money_from_sales - purchase_value_stocks
                    final_quant_stock = initial_quant_stocks + delta_quant_stocks
                    ##uncomment for debugging
                    #print("stocks bought. The new amount of stocks held is " + str(final_quant_stock) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_cbonds > 0:
                purchase_value_cbonds = round(delta_quant_cbonds*price_of_rebalance_cbonds,2)
                if purchase_value_cbonds < money_from_sales:
                    money_from_sales = money_from_sales - purchase_value_cbonds
                    final_quant_cbonds = initial_quant_cbonds + delta_quant_cbonds
                    ##uncomment for debugging
                    #print("cbonds bought. The new amount of cbonds held is " + str(final_quant_cbonds) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_sbonds > 0:
                purchase_value_sbonds = round(delta_quant_sbonds*price_of_rebalance_sbonds,2)
                if purchase_value_sbonds < money_from_sales:
                    money_from_sales = money_from_sales - purchase_value_sbonds
                    final_quant_sbonds = initial_quant_sbonds + delta_quant_sbonds
                    ##uncomment for debugging
                    #print("sbonds bought. The new amount of sbonds held is " + str(final_quant_sbonds) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_gold > 0:
                purchase_value_gold = round(delta_quant_gold*price_of_rebalance_gold,2)
                if purchase_value_gold < money_from_sales:
                    money_from_sales = money_from_sales - purchase_value_gold
                    final_quant_gold = initial_quant_gold + delta_quant_gold
                    ##uncomment for debugging
                    #print("gold bought. The new amount of gold held is " + str(final_quant_gold) + " your current spendable balance is " + str(money_from_sales))
            if delta_quant_cash > 0:
                purchase_value_cash = round(delta_quant_cash*price_of_rebalance_cash,2)
                if purchase_value_cash < money_from_sales:
                    money_from_sales = money_from_sales - purchase_value_cash
                    final_quant_cash = initial_quant_cash + delta_quant_cash
                    ##uncomment for debugging
                    #print("cash bought. The new amount of cash held is " + str(final_quant_cash) + " your current spendable balance is " + str(money_from_sales))
            
            #add final quanitity for whole portfolio
            if delta_quant_stocks == 0:
                final_quant_stock = initial_quant_stocks
            if delta_quant_cbonds == 0:
                final_quant_cbonds = initial_quant_cbonds
            if delta_quant_sbonds == 0:
                final_quant_sbonds = initial_quant_sbonds
            if delta_quant_gold == 0:
                final_quant_gold = initial_quant_gold
            if delta_quant_cash == 0:
                final_quant_cash = initial_quant_cash
            
            #Only buys are used in calculating the return so we get rid of negative values
            purchase_value_stocks=0 if purchase_value_stocks < 0 else purchase_value_stocks
            purchase_value_cbonds=0 if purchase_value_cbonds < 0 else purchase_value_cbonds
            purchase_value_sbonds=0 if purchase_value_sbonds < 0 else purchase_value_sbonds
            purchase_value_gold=0 if purchase_value_gold < 0 else purchase_value_gold
            purchase_value_cash=0 if purchase_value_cash < 0 else purchase_value_cash

            #calculate the amount weve spent on each asset
            final_val_stocks = rebal_value_of_stocks + purchase_value_stocks
            final_val_cbonds = rebal_value_of_cbonds + purchase_value_cbonds
            final_val_sbonds = rebal_value_of_sbonds + purchase_value_sbonds
            final_val_gold = rebal_value_of_gold + purchase_value_gold
            final_val_cash = rebal_value_of_cash + purchase_value_cash

            #Write rebalance to Pandas DF so we can reuse it in the next loop
            pandas_data = {
            'Asset Alloc.':  [int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer]), int(portfolio_allocation_IDs[pointer])],
            'Asset': ['stocks', 'cbonds','sbonds', 'gold', 'cash'],
            'Asset Money' : [final_val_stocks, final_val_cbonds, final_val_sbonds, final_val_gold, final_val_cash],
            '#':  [final_quant_stock, final_quant_cbonds, final_quant_sbonds, final_quant_gold, final_quant_cash] 
            }
            #columns = ['ST_M', 'ST_Q', 'ST_P', 'CB_M', 'CB_Q', 'CB_P', 'SB_M', 'SB_Q', 'SB_P', 'GO_M', 'GO_Q', 'GO_P', 'CA_M', 'CA_Q', 'CA_P', 'Money', 'Portf_Val']
            
            previous_rebalance = pd.DataFrame (pandas_data, columns = ['Asset Alloc.', 'Asset', 'Asset Money', '#'])
        

            
        
            #Write trade to data list for later writing to CSV
            ##uncomment for debugging
            #print(final_quant_stock, final_quant_cbonds, final_quant_sbonds, final_quant_gold, final_quant_cash)
            
            data.append(tuple([date_of_rebalance.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".ST", int(portfolio_allocation_IDs[pointer]), "stocks", rebal_value_of_stocks, price_of_rebalance_stocks, final_quant_stock, purchase_value_stocks, investment_period]))
            data.append(tuple([date_of_rebalance.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".CB", int(portfolio_allocation_IDs[pointer]), "cbonds", rebal_value_of_cbonds, price_of_rebalance_cbonds, final_quant_cbonds, purchase_value_cbonds, investment_period]))
            data.append(tuple([date_of_rebalance.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".SB", int(portfolio_allocation_IDs[pointer]), "sbonds", rebal_value_of_sbonds, price_of_rebalance_sbonds, final_quant_sbonds, purchase_value_sbonds, investment_period]))
            data.append(tuple([date_of_rebalance.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".GO", int(portfolio_allocation_IDs[pointer]), "gold", rebal_value_of_gold, price_of_rebalance_gold, final_quant_gold, purchase_value_gold, investment_period]))
            data.append(tuple([date_of_rebalance.strftime("%d/%m/%Y"), "oneoff-rebal.", str(portfolio_allocation_IDs[pointer]) +"."+ str(y) + ".CA", int(portfolio_allocation_IDs[pointer]), "cash", rebal_value_of_cash, 1, final_quant_cash, purchase_value_cash, investment_period]))
            trading_util.write_as_csv(data, "append")

    #if we where to run this to get all 150k lines every time it would be more efficient to take write csv out of the for loop (unindent one lvl)
        #write trade data to csv 
        ##uncomment for debugging
        #print("Now writing to CSV")
        #just in case remove any duplicates
        # data = list(dict.fromkeys(data))
        # trading_util.write_as_csv(data, "append")
        # ##uncomment for debugging
        #print("finished writing trade to CSV")
    print("[SUCCESS] Oneoff Rebalance")


def DCA_rebalance(Rebal_ST_Q, Rebal_CB_Q, Rebal_SB_Q, Rebal_GO_Q, Rebal_CA_Q, stock_percentage, cbond_percentage, sbond_percentage, gold_percentage, cash_percentage, Rebal_Money, DCA_date):
    Rebal_ST_Q = Rebal_ST_Q 
    Rebal_CB_Q = Rebal_CB_Q
    Rebal_SB_Q = Rebal_SB_Q
    Rebal_GO_Q = Rebal_GO_Q
    Rebal_CA_Q = Rebal_CA_Q
    stock_percentage = stock_percentage
    cbond_percentage = cbond_percentage
    sbond_percentage = sbond_percentage
    gold_percentage = gold_percentage
    cash_percentage = cash_percentage
    Rebal_Money = Rebal_Money
    DCA_date = DCA_date
    ##uncomment for debugging
    # print("dca date is ")
    # print(DCA_date)
    #rebalance in the same month on the 15th
    rebalance_date = datetime.date(DCA_date.year, DCA_date.month, 15)
    #get price of assets on date
    #get the current prices/values of assets
    try:
        date_of_rebalance, price_of_rebalance_cbonds = trading_util.find_data_point("cbonds", rebalance_date)
    except:
        return ("there is an error. Has the end of the available asset data been reached?")
    price_of_rebalance_stocks = trading_util.find_data_point("stocks", date_of_rebalance)[1]
    price_of_rebalance_sbonds = trading_util.find_data_point("sbonds", date_of_rebalance)[1]
    price_of_rebalance_gold = trading_util.find_data_point("gold", date_of_rebalance)[1]
    #cash is always valued at 1 USD as per instructions
    price_of_rebalance_cash = 1

    #calculate total portfolio value
    #calculate the total value of each asset in our portfolio
    rebal_value_of_cbonds = price_of_rebalance_cbonds*Rebal_CB_Q
    rebal_value_of_stocks = price_of_rebalance_stocks*Rebal_ST_Q
    rebal_value_of_sbonds = price_of_rebalance_sbonds*Rebal_SB_Q
    rebal_value_of_gold = price_of_rebalance_gold*Rebal_GO_Q
    rebal_value_of_cash = 1*Rebal_CA_Q
    
    #calculate the current value of our portfolio
    rebal_portf_value =  rebal_value_of_cbonds + rebal_value_of_stocks + rebal_value_of_sbonds + rebal_value_of_gold + rebal_value_of_cash
    ##uncomment for debugging
    #print("the current total value of the protfolio is " + str(rebal_portf_value))

    #calculate optimum quantity of assets 
    #current portfolio value * asset weight in portfolio / asset price
    #use floored division to get whole units of assets
    opt_quant_stocks = math.floor((rebal_portf_value*stock_percentage)/price_of_rebalance_stocks)
    opt_quant_cbonds = math.floor((rebal_portf_value*cbond_percentage)/price_of_rebalance_cbonds)
    opt_quant_sbonds = math.floor((rebal_portf_value*sbond_percentage)/price_of_rebalance_sbonds)
    opt_quant_gold = math.floor((rebal_portf_value*gold_percentage)/price_of_rebalance_gold)
    opt_quant_cash = math.floor((rebal_portf_value*cash_percentage)/1)
    ##uncomment for debugging
    #print("Your balanced portfolio should have " + str(opt_quant_stocks) + " stock units " + str(opt_quant_cbonds)+ " cbond units " + str(opt_quant_sbonds) +" sbond units " + str(opt_quant_gold) + " gold units " + str(opt_quant_cash) + " cash units " )
   
    #calculate deltas
    #calculate deltas between optimum and current quantity
    delta_quant_stocks = opt_quant_stocks - Rebal_ST_Q 
    delta_quant_cbonds = opt_quant_cbonds - Rebal_CB_Q
    delta_quant_sbonds = opt_quant_sbonds - Rebal_SB_Q
    delta_quant_gold =  opt_quant_gold - Rebal_GO_Q
    delta_quant_cash = opt_quant_cash - Rebal_CA_Q

    #if there is no need to rebalance then do not run the rest of the loop
    # if delta_quant_stocks == 0 and delta_quant_cbonds==0 and delta_quant_sbonds==0 and delta_quant_gold==0 and delta_quant_cash==0: 
    #     print("Your portfolio is balanced")
    #     continue
    final_quant_stock = 0
    final_quant_cbonds = 0
    final_quant_sbonds = 0
    final_quant_gold = 0
    final_quant_cash = 0
    #use starting money from previous rebalances
    money_from_sales = 0 + Rebal_Money

    #if we buy we need to return this later for calculating the return
    invest_buy_stocks = float(0)
    invest_buy_cbonds = float(0)
    invest_buy_sbonds = float(0)
    invest_buy_gold = float(0)
    invest_buy_cash = float(0)

    #conduct sales if needed
    if delta_quant_stocks < 0:
        money_from_sales = money_from_sales + abs(delta_quant_stocks*price_of_rebalance_stocks)
        final_quant_stock = Rebal_ST_Q + delta_quant_stocks
        ##uncomment for debugging
        #print("stocks sold. The new amount of stocks held is " + str(final_quant_stock) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_cbonds < 0:
        money_from_sales = money_from_sales + abs(delta_quant_cbonds*price_of_rebalance_cbonds)
        final_quant_cbonds = Rebal_CB_Q + delta_quant_cbonds
        ##uncomment for debugging
        #print("cbonds sold. The new amount of cbonds held is " + str(final_quant_cbonds) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_sbonds < 0:
        money_from_sales = money_from_sales + abs(delta_quant_sbonds*price_of_rebalance_sbonds)
        final_quant_sbonds = Rebal_SB_Q + delta_quant_sbonds
        ##uncomment for debugging
        #print("sbonds sold. The new amount of sbonds held is " + str(final_quant_sbonds) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_gold < 0:
        money_from_sales = money_from_sales + abs(delta_quant_gold*price_of_rebalance_gold)
        final_quant_gold = Rebal_GO_Q + delta_quant_gold
        ##uncomment for debugging
        #print("gold sold. The new amount of gold held is " + str(final_quant_gold) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_cash < 0:
        money_from_sales = money_from_sales + abs(delta_quant_cash*price_of_rebalance_cash)
        final_quant_cash = Rebal_CA_Q + delta_quant_cash
        ##uncomment for debugging
        #print("cash sold. The new amount of cash held is " + str(final_quant_cash) + " your current spendable balance is " + str(money_from_sales))
    
    #conduct purchases with money_from_sales
    if delta_quant_stocks > 0:
        purchase_value = delta_quant_stocks*price_of_rebalance_stocks
        if purchase_value < money_from_sales:
            money_from_sales = money_from_sales - purchase_value
            final_quant_stock = Rebal_ST_Q + delta_quant_stocks
            invest_buy_stocks = round(purchase_value,2)
            ##uncomment for debugging
            #print("stocks bought. The new amount of stocks held is " + str(final_quant_stock) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_cbonds > 0:
        purchase_value = delta_quant_cbonds*price_of_rebalance_cbonds
        if purchase_value < money_from_sales:
            money_from_sales = money_from_sales - purchase_value
            final_quant_cbonds = Rebal_CB_Q + delta_quant_cbonds
            invest_buy_cbonds = round(purchase_value,2)
            ##uncomment for debugging
            #print("cbonds bought. The new amount of cbonds held is " + str(final_quant_cbonds) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_sbonds > 0:
        purchase_value = delta_quant_sbonds*price_of_rebalance_sbonds
        if purchase_value < money_from_sales:
            money_from_sales = money_from_sales - purchase_value
            final_quant_sbonds = Rebal_SB_Q + delta_quant_sbonds
            invest_buy_sbonds = round(purchase_value,2)
            ##uncomment for debugging
            #print("sbonds bought. The new amount of sbonds held is " + str(final_quant_sbonds) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_gold > 0:
        purchase_value = delta_quant_gold*price_of_rebalance_gold
        if purchase_value < money_from_sales:
            money_from_sales = money_from_sales - purchase_value
            final_quant_gold = Rebal_GO_Q + delta_quant_gold
            invest_buy_gold = round(purchase_value,2)
            ##uncomment for debugging
            #print("gold bought. The new amount of gold held is " + str(final_quant_gold) + " your current spendable balance is " + str(money_from_sales))
    if delta_quant_cash > 0:
        purchase_value = delta_quant_cash*price_of_rebalance_cash
        if purchase_value < money_from_sales:
            money_from_sales = money_from_sales - purchase_value
            final_quant_cash = Rebal_CA_Q + delta_quant_cash
            invest_buy_cash = round(purchase_value,2)
            ##uncomment for debugging
            #print("cash bought. The new amount of cash held is " + str(final_quant_cash) + " your current spendable balance is " + str(money_from_sales))
    
    #if neither purchase or sale is needed keep the original quanitity
    if delta_quant_stocks == 0:
        final_quant_stock = Rebal_ST_Q
    if delta_quant_cbonds == 0:
        final_quant_cbonds = Rebal_CB_Q
    if delta_quant_sbonds == 0:
        final_quant_sbonds = Rebal_SB_Q
    if delta_quant_gold == 0:
        final_quant_gold = Rebal_GO_Q
    if delta_quant_cash == 0:
        final_quant_cash = Rebal_CA_Q

    #the changed quantity needs to go back to DCA to be written into the previous trades df
    diff_start_fin_stocks = final_quant_stock - Rebal_ST_Q
    diff_start_fin_cbonds = final_quant_cbonds - Rebal_CB_Q
    diff_start_fin_sbonds = final_quant_sbonds - Rebal_SB_Q
    diff_start_fin_gold = final_quant_gold - Rebal_GO_Q
    diff_start_fin_cash = final_quant_cash - Rebal_CA_Q

    return "DCA rebalance succeeded", final_quant_stock, price_of_rebalance_stocks, final_quant_cbonds, price_of_rebalance_cbonds, final_quant_sbonds, price_of_rebalance_sbonds, final_quant_gold, price_of_rebalance_gold, final_quant_cash, price_of_rebalance_cash, money_from_sales, rebal_portf_value, date_of_rebalance, invest_buy_stocks, invest_buy_cbonds, invest_buy_sbonds, invest_buy_gold, invest_buy_cash, diff_start_fin_stocks, diff_start_fin_cbonds, diff_start_fin_sbonds, diff_start_fin_gold, diff_start_fin_cash