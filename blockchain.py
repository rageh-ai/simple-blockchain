from hashlib import sha256
import json

from time import time
from uuid import uuid4

from flask import Flask

class BlockChain(object):
    
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        
        self.new_block(self, proof=100, previous_hash=1)


    
    def new_block(self, proof, previous_hash=None):
        ## new block and add to the chain

        block = {
            'index': len(self.chain) + 1,
            'timestamp' :time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])

        }
        self.current_transactions = []
        self.chain.append(block)

        return block


    def new_transaction(self, sender, recipent, amount):
        ## Adds a new transaction to the list of transaction

        self.current_transactions.append({
            'sender' : sender,
            'recipent' : recipent,
            'amount' : amount
        })
        
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        ## hashes a block
        pass

    @property
    def last_block(self):
        ## returns the last block in the chain
        return self.chain[-1]    


    def proof_of_work(self, last_proof):

        proof = 0

        while self.vald_proof(last_proof, proof) is False:
            proof+= 1
        
        return proof
    
    def valid_proof(last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"


## insantiate the node
app = Flask(__name__)

## Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

## Instantiate the blockchain
blockchain = BlockChain()

@app.route('/mine', methods=["GET"])

def mine():
    return "for mining"


@app.route('/transactions/new', methods=["POST"])
def new_transaction():
    return 'we will add a new transaction'


@app.route('/chain', methods=["GET"])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length' : len(blockchain.chain)
    }

    return jsonify(response), 200


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
