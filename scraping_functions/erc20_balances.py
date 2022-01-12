"""
Get ERC20 Balanes of person
"""
import requests
import pyuser_agent
import pandas as pd
from bs4 import BeautifulSoup
import random
import Constants


def get_erc20_balances_raw(address, use_proxy=False):
    ua = lambda: pyuser_agent.UA().random

    url = 'https://etherscan.io/tokenholdingsnew.aspx/GetAssetDetails'
    data = '{"dataTableModel":{"draw":2,"columns":[{"data":"TokenName","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"Symbol","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"ContractAddress","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"Balance","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"Price","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"Change24H","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"Value","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"More","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}}],"order":[{"column":6,"dir":"desc"}],"start":0,"length":1000,"search":{"value":"","regex":false}},"model":{"address":"' + address + '","hideZeroAssets":false,"filteredContract":"","showEthPrice":false}}'
    headers = {
        "User-Agent" : ua(),
        'authority': 'etherscan.io',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?',
        'origin': 'https://etherscan.io',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://etherscan.io/tokenholdings?a={address}',
        'accept-language': 'en-US,en;q=0.9'
    }
    

    proxy = f"http://{Constants.SMART_PROXY_USERNAME}:{Constants.SMART_PROXY_PASSWORD}@gate.smartproxy.com:7000"
    proxy_obj = {'http': proxy, 'https': proxy}
    r = requests.post(url, data=data, headers=headers, proxies=proxy_obj) if use_proxy else requests.post(url, data=data, headers=headers)


    return r.json()['d']['data']

def extract_text(content):
    soup = BeautifulSoup(content, features="html.parser")
    return soup.text

def get_erc20_balances(address, use_proxy=False):
    raw_data = get_erc20_balances_raw(address, use_proxy)
    df = pd.DataFrame(raw_data)
    df = df[[c for c in df.columns if c != "More" ]]
    for c in df.columns:
        df[c] = df[c].apply(extract_text)
    return df