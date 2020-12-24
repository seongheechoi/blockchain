from hashlib import sha256
import json
from datetime import datetime
import numpy as np

class Block:
    def __init__(self, index, previous_hash, current_transactions, timestamp, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.current_transactions = current_transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        first_hash = sha256(block_string.encode()).hexdigest()
        second_hash = sha256(first_hash.encode()).hexdigest()
        return second_hash

    def __str__(self):
        return str(self.__dict__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.genesis_block()

    def __str__(self):
        return str(self.__dict__)

    def genesis_block(self):
        genesis_block = Block('Genesis', 0x0, [3,4,5,6,7], 'datetime.now().timestamp()', 0)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block.hash)
        self.transactions.append(str(genesis_block.__dict__))
        return genesis_block

    def getLastBlock(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        difficulty = 1
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not (computed_hash.endswith('0' * difficulty) and ('55' * difficulty) in computed_hash):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add(self, data):
        block = Block(len(self.chain), self.chain[-1], data, 'datetime.now().timestamp()', 0)
        block.hash = self.proof_of_work(block)
        self.chain.append(block.hash)
        self.transactions.append(block.__dict__)
        return json.loads(str(block.__dict__).replace('\'','\"'))

    def getTransactions(self, id):
        labels = ['Manufacturer', 'Transportation', 'Retailer']
        while True:
            try:
                if id == 'all':
                    for i in range(len(self.transactions)-1):
                        print('{}\n:{}\n'.format(labels[i], self.transactions[i+1]))
                    break


                elif type(id) == int:
                    print(self.transactions[id])
                    break
            except Exception as e:
                print(e)

def main():
    manufacturer = {
        'transactions':
            [
                {
                'timestamp':datetime.now().timestamp(),
                'product_id':1,
                'product_serial':50001000,
                'name': 'cotton pants',
                'from': 'Manufacturer X',
                'to': 'Transportation X',
                'message': 'This product is in good order',
                'digital signature': 'approved',
                'flagged': 'N'
                },
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 2,
                'product_serial': 50002000,
                'name': 'cotton shirt',
                'from': 'Manufacturer X',
                'to': 'Transportation X',
                'message': 'This product is in good order',
                'digital signature': 'approved',
                'flagged': 'N'
                },
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 2,
                'product_serial': 50002001,
                'name': 'cotton shirt',
                'from': 'Manufacturer X',
                'to': 'Transportation X',
                'message': 'This product is in good order',
                'digital signature': 'approved',
                'flagged': 'N'
                },

            ]
        }

    transportation = {
        'transactions':
            [
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 1,
                'product_serial': 50001000,
                'name': 'cotton pants',
                'from': 'Transportation X',
                'to': 'Retailer X',
                'shipping_id': 100,
                'message': 'Product in good order. Shipped',
                'digital signature': 'approved',
                'flagged': 'N'
                },
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 2,
                'product_serial': 50002000,
                'name': 'cotton shirt',
                'from': 'Transportation X',
                'to': 'Retailer X',
                'shipping_id': 101,
                'message': 'Product in good order. Shipped',
                'digital signature': 'approved',
                'flagged': 'N'
                },
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 2,
                'product_serial': 50002001,
                'name': 'cotton shirt',
                'from': 'Transportation X',
                'to': 'Retailer X',
                'shipping_id': 102,
                'message': 'Product damaged',
                'digital signature': 'retailer review',
                'flagged': 'Y'
                },

            ]
        }

    retailer = {
        'transactions':
            [
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 1,
                'product_serial': 50001000,
                'name': 'cotton pants',
                'from': 'Retailer X',
                'to': 'Retailer Shelf',
                'receiving_id': 400,
                'message': 'Product in good order. Received',
                'digital signature': 'approved',
                'flagged': 'N'
                },
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 2,
                'product_serial': 50002000,
                'name': 'cotton shirt',
                'from': 'Retailer X',
                'to': 'Retailer Shelf',
                'receiving_id': 400,
                'message': 'Product Good',
                'digital signature': 'approved',
                'flagged': 'N'
                },
                {
                'timestamp': datetime.now().timestamp(),
                'product_id': 2,
                'product_serial': 50002001,
                'name': 'cotton shirt',
                'from': 'Retailer X',
                'to': 'RTV',    #RTV : return to vendor
                'receiving_id': 401,
                'message': 'Box Damaged',
                'digital signature': 'rejected',
                'flagged': 'Y'
                },

            ]
    }

    B=Blockchain()
    a=B.add(manufacturer)
    b=B.add(transportation)
    c=B.add(retailer)
    B.getTransactions('all')
    print(b)

if __name__=='__main__':
    main()