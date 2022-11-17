import sqlite3

import pandas as pd

#conn = sqlite3.connect('yes.db')
conn = sqlite3.connect(':memory:')
c = conn.cursor()

try:
    c.execute("""CREATE TABLE tokens(
                address text,
                bhoughtAt real,
                threshold real,
                amount real
                )""")
except Exception as e:
    print(e)

#Class
#def insert_token3(token):
#    with conn:
#        c.execute("INSERT INTO tokens VALUES (:address, :bhoughtAt, :threshold, :amount)", {
#                  'address': token.address, 'bhoughtAt': token.bhoughtAt, 'threshold': token.threshold, "amount": token.amount})
#Dict
def insert_token2(token):
    with conn:
        c.execute("INSERT INTO tokens VALUES (:address, :bhoughtAt, :threshold, :amount)", {
                  'address': token["address"], 'bhoughtAt': token['bhoughtAt'], 'threshold' : token["threshold"], "amount": token['amount']})

#List
def insert_token(token):
    with conn:
        c.execute("INSERT INTO tokens VALUES (:address, :bhoughtAt, :threshold, :amount)", {
                  'address': token[0], 'bhoughtAt': token[1], 'threshold' : token[2], "amount": token[3]})


def get_tokens_by_address(address):
    c.execute("SELECT * FROM tokens WHERE address=:address",
              {'address': address})
    return c.fetchall()


def remove_token(address):
    with conn:
        c.execute("DELETE from tokens WHERE address = :address",
                  {'address': address})


def update(token):
    with conn:
        #c.execute("SELECT * FROM tokens")
        #[print(row) for row in c.fetchall()]

        c.execute("UPDATE tokens SET threshold = :threshhold WHERE address = :address", {
                  'address': token[0], 'threshhold': token[1] })

        #c.execute("SELECT * FROM tokens")
        [print(row) for row in c.fetchall()]


def getAllTokens():
    with conn:
        dbToken = []
        c.execute("SELECT * FROM tokens")
        for row in c.fetchall():
            dbToken.append(row)
            #print(row)
        df = pd.DataFrame(dbToken, columns=['key', 'bhoughtAt', 'threshold', 'amount'])
        df.index = list(df["key"])
        df.drop('key', axis=1, inplace=True)
        return df



#insert_token(token_2)



#tokens2 = get_tokens_by_address('Jane')


#c.execute("""DELETE FROM COMPANY WHERE address = :address""")


# remove_token("Jane")
#tokens = get_tokens_by_address('John')
#tokens2 = get_tokens_by_address('Jane')

# print(tokens)
# print(tokens2)

#update("John")
#getAllTokens()
#tokens = get_tokens_by_address('Jane')


