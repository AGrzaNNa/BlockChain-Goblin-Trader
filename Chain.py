import hashlib
import json
from time import time


class Blockchain(object):
    """
    A simple implementation of a blockchain.

    Attributes:
        chain (list): A list to store the blockchain.
        pending_transactions (list): A list to store transactions that are to be added to the blockchain.
    """

    def __init__(self):
        """
        Initializes the blockchain with an empty chain and pending transactions.

        Also creates the genesis block.
        """
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="The Times 19/May/2024 Increasing gold trading between distributions.",
                       proof=100)

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work algorithm:

        - Find a number `proof` such that hash(last_proof, proof) contains 4 leading zeroes.

        Args:
            last_proof (int): The proof of the previous block.

        Returns:
            int: The proof for the new block.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        Args:
            last_proof (int): The proof of the previous block.
            proof (int): The current proof to be validated.

        Returns:
            bool: True if the proof is valid, False otherwise.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block and adds it to the chain.

        Args:
            proof (int): The proof given by the Proof of Work algorithm.
            previous_hash (str): Hash of the previous block.

        Returns:
            dict: The new block.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        """
        Returns the last block in the chain.

        Returns:
            dict: The last block in the blockchain.
        """
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block.

        Args:
            sender (str): Address of the sender.
            recipient (str): Address of the recipient.
            amount (int): Amount to be transferred.

        Returns:
            int: The index of the block that will hold this transaction.
        """
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
        """
        Creates a SHA-256 hash of a block.

        Args:
            block (dict): Block to be hashed.

        Returns:
            str: The hash of the block.
        """
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    def get_balance(self, address):
        """
        Calculates the balance of a given address.

        Args:
            address (str): The address to query the balance for.

        Returns:
            int: The balance of the address.
        """
        balance = 0
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['recipient'] == address:
                    balance += transaction['amount']
        return balance


blockchain = Blockchain()
blockchain.new_block(12345)
