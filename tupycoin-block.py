import hashlib
import datetime


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.index).encode("utf-8") +
            str(self.timestamp).encode("utf-8") +
            str(self.data).encode("utf-8") +
            str(self.previous_hash).encode("utf-8")
        )
        return sha.hexdigest()

    @classmethod
    def create_genesis_block(cls):
        return cls(0, "Genesis Block", "0")

    @classmethod
    def next_block(cls, last_block):
        this_index = last_block.index + 1
        this_data = "Hey! I'm block " + str(this_index)
        this_hash = last_block.hash
        return cls(this_index, this_data, this_hash)


blockchain = [Block.create_genesis_block()]
previous_block = blockchain[0]
num_of_blocks_to_add = 20

for i in range(num_of_blocks_to_add):
    block_to_add = Block.next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))
