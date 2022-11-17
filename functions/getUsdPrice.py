import requests
import os


moralisapi = os.environ.get("MORALIS_API")

headers = {
    "Accept": "application/json",
    "X-API-Key": moralisapi
}


def getUsdPrice(contract):
    url = f"https://deep-index.moralis.io/api/v2/erc20/{contract}/price?chain=bsc"
    response = requests.get(url, headers=headers)
    priceStream = response.json()
    priceFloat = float(priceStream['usdPrice'])
    return priceFloat