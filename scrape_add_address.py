import pandas as pd

from scraping_functions.ens_to_address import ens_to_address


df = pd.read_csv('data/twitter_ens.csv')
df = df[[c for c in df.columns if 'Unnamed' not in c]]


df['address'] = df.ens.apply(ens_to_address)


df = df[df.address.apply(lambda x: x is not None)]

df.to_csv('data/twitter_ens_address.csv', index = False)