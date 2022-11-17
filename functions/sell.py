
import time
import configparser
#import numpy as np
from connection import *
#print("token to buy:" + tokenToBuy)

privatekey = os.environ.get("KEY")

def sell(token, amountToSell):
    tokenToBuy = web3provider.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")  # wbnb contract address
    spend = web3provider.toChecksumAddress(token)
    nonce = web3provider.eth.get_transaction_count(sender_address)
    pancakeswap2_txn = contractbuy.functions.swapExactTokensForTokens(
        amountToSell,
        0,  # set to 0, or specify minimum amount of token you want to receive - consider decimals!!!
        [spend, tokenToBuy],
        sender_address,
        (int(time.time()) + 10000)
    ).buildTransaction({
        'from': sender_address,
        #'value': 1000,
        #'value': web3.toWei(amountToBuy, 'ether'),  # This is the Token(BNB) amount you want to Swap from
        'gasPrice': web3provider.toWei('5', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = web3provider.eth.account.sign_transaction(pancakeswap2_txn,
                                                   private_key=privatekey)
    tx_token = web3provider.eth.send_raw_transaction(signed_txn.rawTransaction)
    transaction_tx = web3provider.toHex(tx_token)
    print("succesfull, sold " + transaction_tx)


    return transaction_tx
