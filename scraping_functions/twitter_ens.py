import Constants

import requests
import os
import json
import re
import pandas as pd
import time

def create_url(twitter_id, pagination_token=None):
    usernames = "usernames=TwitterDev,TwitterAPI"
    user_fields = "user.fields=description,created_at"
    url = f"https://api.twitter.com/2/users/{twitter_id}/following?max_results=1000&user.fields=public_metrics"
    url = url + f'&pagination_token={pagination_token}' if pagination_token else url
    return url


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {Constants.TWITTER_BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    return response.json()


def get_following_raw(twitter_id, pagination_token=None):
  time.sleep(60)
  url = create_url(twitter_id, pagination_token)
  json_response = connect_to_endpoint(url)
  return json_response

def extract_ens(s):
    m = re.search('[\w.]+\.eth',s)
    return m.group(0) if m else None

 
def perform_search(mega_df, rounds=10):
    
    for i in range(rounds):

        if i % 15 == 0: #CHANGE
            mega_df.to_csv(f'data/ens_checkpoint/round_{i}.csv')
        #get best   
        try:
            not_yet_searched = mega_df[mega_df.visited != True]
            if not_yet_searched.shape[0] < 2:
                return mega_df
    
            search_id = not_yet_searched[not_yet_searched.followers_count == not_yet_searched.followers_count.max()].id.iloc[0]
            
            print(f'searching {search_id}')

            all_responses = []
            response = get_following_raw(search_id)
            all_responses += response['data']
            while 'next_token' in response['meta']:
                response = get_following_raw(search_id, response['meta']['next_token'])
                all_responses += response['data']


            search_df = pd.DataFrame(all_responses)
            for stat in ['followers_count', 'following_count', 'tweet_count', 'listed_count']:
                search_df[stat] = search_df['public_metrics'].apply(lambda x: x[stat])
            search_df = search_df[[c for c in search_df.columns if c != 'public_metrics']]

            
            
            search_df['ens'] = search_df.name.apply(extract_ens)
            search_df['visited'] = False

            search_df = search_df.dropna(subset=['ens'])
            
            search_df['False'] = False


            mega_df = pd.concat([mega_df, search_df]).drop_duplicates(subset=['id'])
            mega_df.visited = mega_df.apply(lambda row: True if row['id'] == search_id else row['visited']  , axis=1)


        except:
            print("failed")
            time.sleep(60)
    return mega_df
