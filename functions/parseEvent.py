import re


def parseEvent(tokenData):
    trimmedData = tokenData.replace('\n', "")
    print(trimmedData)
    lp_size = re.search(r'Liquidity: (.*?)Token contract', trimmedData, re.IGNORECASE).group(1)
    print(lp_size)
    liquidity = lp_size.translate({ord('$'): None}).translate({ord(','): None})
    liquidity = int(liquidity)
    extractToken = re.compile('token contract:', re.IGNORECASE)
    regexToken = extractToken.search(trimmedData)
    end = regexToken.end()
    tokenAddress = trimmedData[end:end + 42]
    print("Incomming Token: " + tokenAddress)
    return tokenAddress, liquidity