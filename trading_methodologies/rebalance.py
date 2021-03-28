import csv
import pandas as pd
import datetime
import trading_methodologies.trading_util as trading_util

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
                if initial_date_obj.day < 15:
                    date_of_rebalance, price_of_rebalance_cbonds = trading_util.find_data_point("cbonds", trading_util.add_months(rebalance_initial_date, x))
                    print(price_of_rebalance_cbonds)
                    #if we have reached the end of our available data exit the loop
                    if price_of_rebalance_cbonds == None:
                        break
                else:
                    date_of_rebalance, price_of_rebalance_cbonds = trading_util.find_data_point("cbonds", trading_util.add_months(rebalance_initial_date, x+1))
                
                #date_of_rebalance, price_of_rebalance_stock = trading_util.find_data_point("stocks", trading_util.add_months(rebalance_initial_date, x))

    elif method == "DCA":
        print("DCA")
    return 'rebalance succeeded'