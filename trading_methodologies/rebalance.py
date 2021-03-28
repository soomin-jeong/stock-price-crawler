import csv
import pandas as pd
import datetime
import trading_methodologies.trading_util as trading_util
import math

def rebalance(method, investment_period):
    #load our CSV data files
    portfoliodf = pd.read_csv('./portfolio_allocations.csv')
    tradedatadf = pd.read_csv('./trading_methodologies.csv')
    stocksdf = pd.read_csv('./amundi-msci-wrld-ae-c.csv')
    cbondsdf = pd.read_csv('./ishares-global-corporate-bond-$.csv')
    sbondsdf = pd.read_csv('./db-x-trackers-ii-global-sovereign-5.csv')
    golddf = pd.read_csv('./spdr-gold-trust.csv')
    cashdf = pd.read_csv('./usdollar.csv')

    if method == "oneoff":
        #load all trade data which was made with oneoff method
        oneoff_trades_df = tradedatadf[tradedatadf['Trading Method.'] == "Oneoff"]
        print("printing oneoff_trades_df dataframe")
        print(oneoff_trades_df.head())

        # Get a series of unique values in column 'portfolio ID' of the dataframe
        #returns nparray object whcih we convert to list
        x = oneoff_trades_df['Asset Alloc.'].unique()
        portfolio_allocation_IDs = x.tolist()

        print("printing portfolio_allocation_IDs list")
        print(portfolio_allocation_IDs[:5])

        for x in portfolio_allocation_IDs:
            #get target allocation
            #print(str(portfolio_allocation_IDs[x-1]))
            print(portfolio_allocation_IDs[3])
            #print(portfoliodf.head())
            #target_alloc_df = portfoliodf.loc[portfoliodf['Asset Alloc.'] == 2]
            target_alloc_df = portfoliodf.loc[portfoliodf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])]
            target_alloc_stocks = target_alloc_df.iloc[0]['ST']
            target_alloc_cbonds = target_alloc_df.iloc[0]['CB']
            target_alloc_sbonds = target_alloc_df.iloc[0]['PB']
            target_alloc_gold = target_alloc_df.iloc[0]['GO']
            target_alloc_cash = target_alloc_df.iloc[0]['CA']

            #get trade amount for each allocation
            initial_quant_stocks = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])) & (tradedatadf['Asset'] == "stocks")].iloc[0]['#']
            print(initial_quant_stocks) 
            initial_quant_cbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])) & (tradedatadf['Asset'] == "cbonds")].iloc[0]['#']
            initial_quant_sbonds = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])) & (tradedatadf['Asset'] == "sbonds")].iloc[0]['#']
            initial_quant_gold = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])) & (tradedatadf['Asset'] == "gold")].iloc[0]['#']
            initial_quant_cash = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])) & (tradedatadf['Asset'] == "cash")].iloc[0]['#']

            #get initial investment date
            initial_date = tradedatadf.loc[(tradedatadf['Asset Alloc.'] == int(portfolio_allocation_IDs[x-1])) & (tradedatadf['Asset'] == "cbonds")].iloc[0]['Date']
            initial_date_obj = datetime.datetime.strptime(initial_date, '%d/%m/%Y')
            #rebalance for the first time in the same month on the 15th
            rebalance_initial_date = datetime.date(initial_date_obj.year, initial_date_obj.month, 15)
            print(rebalance_initial_date)

            #loop through investment period and rebalance
            for x in range(0, int(investment_period)):
                #print("test")
                #if the initial investment is made after the 15th we dont rebalnce in the current month
                if initial_date_obj.day > 15:
                    x = x + 1
                
                #get the current prices/values of assets
                date_of_rebalance, price_of_rebalance_cbonds = trading_util.find_data_point("cbonds", trading_util.add_months(rebalance_initial_date, x))
                
                #if we have reached the end of our available data exit the loop
                if price_of_rebalance_cbonds == None:
                    break
                price_of_rebalance_stocks = trading_util.find_data_point("stocks", trading_util.add_months(rebalance_initial_date, x))[1]
                price_of_rebalance_sbonds = trading_util.find_data_point("sbonds", trading_util.add_months(rebalance_initial_date, x))[1]
                price_of_rebalance_gold = trading_util.find_data_point("gold", trading_util.add_months(rebalance_initial_date, x))[1]
                price_of_rebalance_cash = 1
                
                rebal_value_of_cbonds = price_of_rebalance_cbonds*initial_quant_cbonds
                rebal_value_of_stocks = price_of_rebalance_stocks*initial_quant_stocks
                rebal_value_of_sbonds = price_of_rebalance_sbonds*initial_quant_sbonds
                rebal_value_of_gold = price_of_rebalance_gold*initial_quant_gold
                rebal_value_of_cash = 1*initial_quant_cash
                #calculate the current value of our portfolio
                rebal_portf_value =  rebal_value_of_cbonds + rebal_value_of_stocks + rebal_value_of_sbonds + rebal_value_of_gold + rebal_value_of_cash

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
                opt_quant_cash = math.floor(opt_val_gold/1)

                #calculate deltas between optimum and current quantity
                delta_quant_stocks = initial_quant_stocks - opt_quant_stocks
                delta_quant_cbonds = initial_quant_cbonds - opt_quant_cbonds
                delta_quant_sbonds = initial_quant_sbonds - opt_quant_sbonds
                delta_quant_gold = initial_quant_gold - opt_quant_gold
                delta_quant_cash = initial_quant_cash - opt_quant_cash

                final_quant_stock = None
                final_quant_cbonds = None
                final_quant_sbonds = None
                final_quant_gold = None
                final_quant_cash = None
                money_from_sales = 0

                #conduct sales
                if delta_quant_stocks < 0:
                    money_from_sales = money_from_sales + abs(delta_quant_stocks*price_of_rebalance_stocks)
                    final_quant_stock = initial_quant_stocks - delta_quant_stocks
                if delta_quant_cbonds < 0:
                    money_from_sales = money_from_sales + abs(delta_quant_cbonds*price_of_rebalance_cbonds)
                    final_quant_cbonds = initial_quant_cbonds - delta_quant_cbonds
                if delta_quant_sbonds < 0:
                    money_from_sales = money_from_sales + abs(delta_quant_sbonds*price_of_rebalance_sbonds)
                    final_quant_sbonds = initial_quant_sbonds - delta_quant_sbonds
                if delta_quant_gold < 0:
                    money_from_sales = money_from_sales + abs(delta_quant_gold*price_of_rebalance_gold)
                    final_quant_gold = initial_quant_gold - delta_quant_gold
                if delta_quant_cash < 0:
                    money_from_sales = money_from_sales + abs(delta_quant_cash*price_of_rebalance_cash)
                    final_quant_cash = initial_quant_cash - delta_quant_cash
                
                #conduct purchases with money_from_sales
                if delta_quant_stocks > 0:
                    purchase_value = delta_quant_stocks*price_of_rebalance_stocks
                    if purchase_value < money_from_sales:
                        money_from_sales = money_from_sales - purchase_value
                        final_quant_stock = initial_quant_stocks + delta_quant_stocks
                if delta_quant_cbonds > 0:
                    purchase_value = delta_quant_cbonds*price_of_rebalance_cbonds
                    if purchase_value < money_from_sales:
                        money_from_sales = money_from_sales - purchase_value
                        final_quant_cbonds = initial_quant_cbonds + delta_quant_cbonds
                if delta_quant_sbonds > 0:
                    purchase_value = delta_quant_sbonds*price_of_rebalance_sbonds
                    if purchase_value < money_from_sales:
                        money_from_sales = money_from_sales - purchase_value
                        final_quant_sbonds = initial_quant_sbonds + delta_quant_sbonds
                if delta_quant_gold > 0:
                    purchase_value = delta_quant_gold*price_of_rebalance_gold
                    if purchase_value < money_from_sales:
                        money_from_gold = money_from_gold - purchase_value
                        final_quant_gold = initial_quant_gold + delta_quant_gold
                if delta_quant_cash > 0:
                    purchase_value = delta_quant_cash*price_of_rebalance_cash
                    if purchase_value < money_from_sales:
                        money_from_sales = money_from_sales - purchase_value
                        final_quant_cash = initial_quant_cash + delta_quant_cash
            
            #write to CSV

    elif method == "DCA":
        print("DCA")
    return 'rebalance succeeded'