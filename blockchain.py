import hashlib
import datetime
import json
from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        """
        Arguments:
            · proof: nonce of current block
            · previous_hash: hash of previous block

        Returns:
            · block: new created block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }

        self.chain.append(block)
        return block

    def get_previous_block(self):
        """
        Returns the previous block from the chain
        """
        previous_block = self.chain[-1]
        return previous_block

    def proof_of_work(self, previous_proof):
        """
        Consensus protocol PoW.

        Receives the nonce of the previous proof and
        returns the new hash obtained with PoW.
        """
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        """
        Calculates the hash of a block.

        Arguments:
            · block: identifies a block in the blockchain

        Returns:
            · hash: returns the block's hash
        """
        encoded_block = json.dumps(block, sort_keys=True, indent=4).encode()
        hash_block = hashlib.sha256(encoded_block).hexdigest()
        return hash_block

    def is_chain_valid(self, chain):
        """
        Determines if the chain is valid.

        Argumens:
            · chain: chain that contains info on all transactions

        Returns:
            · True/False: depending on blockchain validity
        """

        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True


# API with Flask
app = Flask(__name__)
run_with_ngrok(app)

# Create blockchain
blockchain = Blockchain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "You have mined a new block",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "Blockchain is valid"}
    else:
        response = {"message": "Blockchain not valid"}
    return jsonify(response), 200
