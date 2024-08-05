from hashlib import sha256
import json
from time import time
import hashlib
from urllib.parse import urlparse
import requests

class BlockChain(object):
    
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        
        
        self.new_block( 100, 1)


    
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

    
    def register_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    


    @staticmethod
    def hash(block):
        ## hashes a block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        ## returns the last block in the chain
        return self.chain[-1]    


    def proof_of_work(self, last_proof):

        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof+= 1
        
        return proof
    
    def valid_proof(self, last_proof, proof):

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True
    
    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


