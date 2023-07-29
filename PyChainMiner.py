import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, transactions, proof):
    return hashlib.sha256(f"{index}{previous_hash}{timestamp}{transactions}{proof}".encode('utf-8')).hexdigest()

def create_genesis_block():
    # Manually create the first block with index 0 and arbitrary data
    return Block(0, "0", time.time(), [], 0, calculate_hash(0, "0", time.time(), [], 0))

def create_new_block(previous_block, transactions, proof):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, transactions, proof)
    return Block(index, previous_block.hash, timestamp, transactions, proof, hash)

# Simple proof-of-work implementation
def proof_of_work(last_proof):
    difficulty = 4  # Number of leading zeros required in the hash
    proof = 0
    while not is_valid_proof(last_proof, proof, difficulty):
        proof += 1
    return proof

def is_valid_proof(last_proof, proof, difficulty):
    guess = f"{last_proof}{proof}".encode('utf-8')
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "0" * difficulty

# Simple blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.pending_transactions = []

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({"sender": sender, "receiver": receiver, "amount": amount})

    def mine_block(self, miner_address):
        last_block = self.get_latest_block()
        last_proof = last_block.proof
        proof = proof_of_work(last_proof)
        self.add_transaction(sender="Blockchain Reward", receiver=miner_address, amount=1)  # Reward for mining
        block = create_new_block(last_block, self.pending_transactions, proof)
        self.chain.append(block)
        self.pending_transactions = []

# Testing the blockchain
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add transactions and mine blocks
    blockchain.add_transaction("Alice", "Bob", 5)
    blockchain.mine_block("Miner1")

    blockchain.add_transaction("Bob", "Charlie", 3)
    blockchain.mine_block("Miner2")

    # Display the blockchain
    for block in blockchain.chain:
        print(f"Block #{block.index} - Timestamp: {block.timestamp} - Transactions: {block.transactions} - Proof: {block.proof} - Hash: {block.hash}")
