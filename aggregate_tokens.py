import pandas as pd

from scraping_functions.erc20_balances import get_erc20_balances


df_addresses = pd.read_csv('data/df_addresses.csv')


dfs = []
for i in range(0, len(df_addresses)):
    try:
        df_tokens = get_erc20_balances(df_addresses.iloc[i]['Address'], use_proxy=True)
        print(df_tokens.shape)
        df_tokens['Ens'] = df_addresses.iloc[i]['Ens']
        df_tokens['Address'] = df_addresses.iloc[i]['Address']
        df_tokens['Followers'] = df_addresses.iloc[i]['Followers']

        dfs.append(df_tokens)
    except:
        print('failed')

df = pd.concat(dfs)

df.to_csv('data/aggregated_tokens_xl.csv')