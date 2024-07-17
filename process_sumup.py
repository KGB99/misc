import os
import argparse
import pandas as pd # type: ignore

# this program is to process the sumup sales reports into a readable report
# the program processes *.csv into *_processed.csv
# besides total profit it lists the categories of items sold, nr of items sold per category and revenue per category
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--csv_file", required=True, type=str)
    args = parser.parse_args()
    file_name = args.csv_file

    # read csv and keep only relevant columns
    df = pd.read_csv(file_name)    
    df = df[['Quantity', 'Description', 'Price (Net)', 'Transaction refunded']]
    
    # list the unique sales items
    items = df['Description'].unique()
    
    # create dictionary of df's where each df has only one unique item as sales item
    # for a filter that ignores refunds: dfs = {item : df[(df['Description'] == item) & (df['Transaction refunded'].isna())] for item in items}
    # currently i'll leave refunds in, as im not too sure how to handle them best
    dfs = {item : df[df['Description'] == item] for item in items}

    result_array = []
    for key, df_item in dfs.items():
        
        quantity = df_item['Quantity'].sum()
        revenue = df_item['Price (Net)'].sum()
        result_array.append([key, quantity, revenue])
    
    column_names = ['Item' , 'Quantity', 'Revenue']
    result_df = pd.DataFrame(result_array, columns=column_names)
    
    result_df.to_csv(file_name.split(".csv")[0] + "_processed.csv")
    print("OK!")