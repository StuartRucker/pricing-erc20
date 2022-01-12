import pandas as pd

from scraping_functions.erc20_balances import get_erc20_balances


df_addresses = pd.read_csv('data/twitter_ens_address.csv')


dfs = []
for i in range(0, len(df_addresses)):
    try:
        df_tokens = get_erc20_balances(df_addresses.iloc[i]['address'], use_proxy=True)
        

        for c in df_addresses.columns:
            df_tokens['Owner_'+c] = df_addresses.iloc[i][c]
            df_tokens['Owner_'+c] = df_addresses.iloc[i][c]
            df_tokens['Owner_'+c] = df_addresses.iloc[i][c]

        dfs.append(df_tokens)
        print(f'{i} {df_addresses.iloc[i]["ens"]} ✅')

    except Exception as e:
        print(f'{i} {df_addresses.iloc[i]["ens"]} ❌')

df = pd.concat(dfs)

df.to_csv('data/aggregated_tokens_4000.csv', index=False)
