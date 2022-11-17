from telethon import TelegramClient, events
from functions.getTradedAmount import getTradedAmount
from functions.getUsdPrice import *
from functions.honeypot import *
from functions.buy import *
from functions.parseEvent import *
from functions.sell import *
from sql.connect import *
from telethon.sessions import StringSession

# Reading Configs

conf = configparser.ConfigParser()
conf.read("conf.ini")

moralisapi = os.environ.get("MORALIS_API")
headers = {
    "Accept": "application/json",
    "X-API-Key": moralisapi
#    "X-API-Key": conf['moralis']['x-api-key']
}
# Setting configuration values

#phone = conf['telegram']['phone']
phone = os.environ.get('PHONE')
#username = conf['telegram']['username']
username = os.environ.get('USERNAME')
#string = conf['telegram']['stringsession']
string_session = os.environ.get('STRINGSESSION')
#api_id = conf['telegram']['api_id']
api_id = os.environ.get("API_ID")
#api_hash = conf['telegram']['api_hash']
api_hash = os.environ.get('API_HASH')
#api_hash = str(api_hash)
client = TelegramClient(StringSession(string_session), api_id, api_hash)

client.start()
channel = 'https://t.me/DEXTNewPairsBotBSC'





def updateDb():
    try:
        df = getAllTokens()
        print("WATCHING THESE TOKENS:")
        print(df)
    except Exception as e:
        print(e)
    return df


updateDb()

async def main():
   await updatingPrices()

#token contract is used as idx/index
async def updatingPrices():
    while True:
        df = getAllTokens()
        if df.empty:
            print('DataFrame is empty!')
            await asyncio.sleep(15)

        else:
            for idx, val in df['threshold'].items():
                contract = idx
                priceFloat = getUsdPrice(contract)
                await asyncio.sleep(2.5)
                checkIfSell(idx, priceFloat)

def checkIfSell(idx, priceStream):
    df = getAllTokens()
    startprice = df.at[idx, 'bhoughtAt']
    threshold = df.at[idx,'threshold']
    df['tsl'] = df['threshold'] * 0.7
    stop = df.at[idx, 'tsl']
    df['tp'] = df['bhoughtAt'] * 2.7
    tp = df.at[idx, 'tp']
    amountToSell = df.at[idx, 'amount']
    print(df)

    if threshold < priceStream:
        print(f"price stream:{priceStream}...threshold:{threshold}")
        #df.at[idx,'threshold'] = priceStream
        threshold = priceStream
        updateIt = [idx, threshold]
        print(updateIt)
        update(updateIt)
        print(f"threshold updated: {threshold} for token: {idx}")

    elif threshold > priceStream < stop:
        print(f"STOPPED OUT AT: {stop} profit: {tp-startprice}$ Token:  {idx}")
        try:
            sell(idx, amountToSell)
            df.drop(idx, inplace=True)
            remove_token(idx)
            print(f"removed succesfully: {idx}")
        except Exception as e:
            print(e)

    elif threshold > priceStream:
        pass
        #print(f"start price{startprice}: Threshold: {threshold} Stop:{stop} TP: {tp}")

    elif tp < priceStream:
        print(f"start price:{startprice}: Sold: {tp} profit: {tp-startprice}$")
        try:
            sell(idx, amountToSell)
            df.drop(idx, inplace=True)
            remove_token(idx)
            print(f"removed succesfully: {idx}")
        except Exception as e:
            print(e)

@client.on(events.NewMessage(chats=channel))
async def handler(event):
    tokenData = event.message.message
    tokenAddress, liquidity = parseEvent(tokenData)
    tokenAddress = tokenAddress.lower() #taking care of mixed case comparisons
    honeyCheck = await honeypot(tokenAddress) #returns webscrapped string
    # honeyCheck = "Does not seem like a honeypot." # test string
    if honeyCheck == "Does not seem like a honeypot." and liquidity > 99000:
        transaction_tx = buy(tokenAddress, 0.00000001)
        amount = getTradedAmount(tokenAddress, transaction_tx)
        print(f"amount used for honey test: {amount}")
        try:
            sell(tokenAddress, amount)
            sniped_tx = None
            second = 0
            while sniped_tx is None and second < 20:
                try:
                    sniped_tx = buy(tokenAddress, 0.000000008)
                    status = True
                except Exception as e:
                    print(e)
                    second +=1
                    print(f"cant snipe {second}sec")
                    await asyncio.sleep(1)

            if status:
                snipeAmount = None
                second = 0
                while snipeAmount is None and second < 20:
                    try:
                        snipeAmount = getTradedAmount(tokenAddress, sniped_tx)
                        print(f"snipe amount parsed: {snipeAmount}")

                    except Exception as e:
                        print(e)
                        second +=1
                        print(f"transaction tx cant be found {second}sec")
                        await asyncio.sleep(1)
                initPrice = None
                while initPrice is None:
                    try:
                        initPrice = getUsdPrice(tokenAddress)
                        purchaseData = [tokenAddress, initPrice, initPrice, snipeAmount]
                        insert_token(purchaseData)
                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)
            second =+1
            print("Honeypot: Could not sell")

    elif honeyCheck == "Yup, honeypot. Run the fuck away.":
        print(honeyCheck)
    else:
        print("liquidity to low:")
        print(liquidity)

client.loop.run_until_complete(main())
