import pandas as pd

from scraping_functions.twitter_ens import get_following_raw, perform_search

seed_df = pd.read_csv('data/twitter_searchseed.csv')



output_df = perform_search(seed_df, 99999)
output_df.to_csv('data/final_search.csv', index = False)