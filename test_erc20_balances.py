import pandas as pd


from scraping_functions.erc20_balances import get_erc20_balances


df = get_erc20_balances('0x01b7baA7baA864fEF3CD1C7bc118Cc97cEdCB33f')

df.to_csv('data/gabytokens.csv')

