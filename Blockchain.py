from uuid import uuid4
from flask import Flask, jsonify, request
from Chain import Blockchain

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """
    Endpoint to mine a new block in the blockchain.

    - Retrieves the last proof of work and computes a new proof of work.
    - Creates a new transaction with a reward for mining.
    - Constructs a new block and adds it to the blockchain.

    Returns:
        Response with the details of the newly forged block.
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Endpoint to create a new transaction.

    - Expects a JSON request with 'sender', 'recipient', and 'amount'.
    - Checks if the sender has sufficient balance.
    - Adds the transaction to the next block.

    Returns:
        Response indicating the block index where the transaction will be added.
    """
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    try:
        amount = int(values['amount'])
    except ValueError:
        amount = 0

    sender_balance = blockchain.get_balance(values['sender'])
    if sender_balance < amount:
        return jsonify({'message': 'Insufficient balance for transaction'}), 403

    index = blockchain.new_transaction(values['sender'], values['recipient'], amount)

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Endpoint to return the full blockchain.

    Returns:
        Response containing the entire blockchain and its length.
    """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/wallet', methods=['GET'])
def get_balance():
    """
    Endpoint to get the balance of the node's wallet.

    Returns:
        Response containing the node identifier and its balance.
    """
    balance = blockchain.get_balance(node_identifier)
    response = {'node_identifier': node_identifier, 'balance': balance}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
