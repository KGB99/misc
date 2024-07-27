import os
import argparse
import pandas as pd # type: ignore

# this program is to process the sumup sales reports into a readable report
# the program processes *.csv into *_processed.csv
# besides total profit it lists the categories of items sold, nr of items sold per category and revenue per category
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--csv_file", required=True, type=str, help="Path to csv file of sales report from sumup")
    parser.add_argument("--german", required=False, type=bool, default=True, help="Bool flag whether the sumup return is in german or english, default is True")
    parser.add_argument("--process_refunds", required=False, type=bool, default=False, help="Bool flag whether refunds should be processed, default is False")
    parser.add_argument("--people", required=False, type=int, default=-1, help="Number of people for the calculation of averages, avgs are only calculated if this value is provided")
    args = parser.parse_args()
    FILE_NAME = args.csv_file
    GERMAN = args.german
    PROCESS_REFUNDS = args.process_refunds
    PEOPLE = args.people
    CALC_AVGS = (PEOPLE > -1)

    if (GERMAN):
        quantity_str = "Menge"
        desc_str = "Beschreibung"
        price_str = "Preis (netto)"
        refunded = "" # ?? dunno what this is as it doesnt exist in the german ones so far
    else:
        quantity_str = "Quantity"
        desc_str = "Description"
        price_str = "Price (Net)"
        refunded_str = "Transaction refunded"

    # read csv and keep only relevant columns
    df = pd.read_csv(FILE_NAME)
    if (PROCESS_REFUNDS):
        df = df[[quantity_str, desc_str, price_str, refunded]]
    else:
        df = df[[quantity_str, desc_str, price_str]]
    
    # list the unique sales items
    items = df[desc_str].unique()
    
    # create dictionary of df's where each df has only one unique item as sales item
    # for a filter that ignores refunds: dfs = {item : df[(df['Description'] == item) & (df['Transaction refunded'].isna())] for item in items}
    # currently i'll leave refunds in, as im not too sure how to handle them best
    dfs = {item : df[df[desc_str] == item] for item in items}

    result_array = []
    for key, df_item in dfs.items():
        quantity = df_item[quantity_str].sum()
        revenue = df_item[price_str].sum()
        if (CALC_AVGS):
            avg_consumption = round(quantity/PEOPLE, 2)
        result_array.append([key, quantity, revenue, avg_consumption] if CALC_AVGS else [key, quantity, revenue])
    
    column_names = ['Item' , 'Quantity', 'Revenue', 'avg_consumption'] if CALC_AVGS else ['Item' , 'Quantity', 'Revenue']
    result_df = pd.DataFrame(result_array, columns=column_names)
    
    result_df.to_csv(FILE_NAME.split(".csv")[0] + "_processed.csv", decimal=',')
    print("OK!")