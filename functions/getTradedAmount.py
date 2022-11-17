import json
from ast import literal_eval
import time
from web3 import Web3
from web3.exceptions import TransactionNotFound

from connection import web3provider
from functions.convertHex import convertHex


def getTradedAmount(tokenAddress, transaction_tx):
    receipt = None
    while receipt is None:
        second = +1
        try:
            receipt = web3provider.eth.getTransactionReceipt(transaction_tx)
            print("receipt parsed")
            print(receipt)
        except TransactionNotFound:

            print(f"transaction tx cant be found {second}sec")
            time.sleep(1)

    tx_json = Web3.toJSON(receipt)
    json_obj = json.loads(tx_json)
    log = json_obj['logs']
    length = len(log)
    convertedAmountData = []
    #range starts with 0
    for t in range(length):
        dec = literal_eval(log[t]['data'])
        print(f"log data converted to decimal number: {dec}")
        if log[t]['address'].lower() == tokenAddress:
            amountData = log[t]['data']
            convertedAmountData = convertHex(amountData)
            print("comverting from hex:")
            print(convertedAmountData)
    # swapAmount = findSwapData(transaction_tx, tokenAddress)
    amount = convertedAmountData[0]
    return amount


