import Constants

import requests
from bs4 import BeautifulSoup
import pyuser_agent


def ens_to_address(ens):
    ua = lambda: pyuser_agent.UA().random

    headers = {
        "User-Agent" : ua()
    }
    proxy = f"http://{Constants.SMART_PROXY_USERNAME}:{Constants.SMART_PROXY_PASSWORD}@gate.smartproxy.com:7000"

    r = requests.get(f'https://etherscan.io/enslookup-search?search={ens}', headers=headers,   proxies={'http': proxy, 'https': proxy})
    soup = BeautifulSoup(r.content, features="html.parser")
    alert_div = soup.find('div', {'class':'alert-secondary'})
    if alert_div is None or alert_div.find('a') is None:
        print(f'{ens} ❌')
        return None
    if "resolves to this Address" in alert_div.text:
        print(f'{ens} ✅')
        return alert_div.find('a').text
    return None
