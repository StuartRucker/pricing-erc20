import pandas as pd

from scraping_functions.twitter_ens import get_following_raw, perform_search

mega_df = pd.read_csv('woloski.csv')



output_df = perform_search(mega_df)
output_df.to_csv('search_output.csv', index = False)