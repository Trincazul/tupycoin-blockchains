import hashlib
import json
import sys
import random


def hashMe(msg=""):
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    elif not isinstance(msg, bytes):
        msg = json.dumps(msg, sort_keys=True).encode('utf-8')

    return hashlib.sha256(msg).hexdigest()


def makeTransaction(max_value=3):
    sign = random.choice([-1, 1])   # escolhe randomicamente 1 ou -1
    amount = random.randint(1, max_value)
    alice_pays = sign * amount
    bob_pays = -1 * alice_pays

    return {'Alice': alice_pays, 'Bob': bob_pays}


txn_buffer = [makeTransaction() for _ in range(30)]


def updateState(txn, state):
    state = state.copy()

    for key in txn:
        if key in state:
            state[key] += txn[key]
        else:
            state[key] = txn[key]

    return state


def is_valid_txn(txn, state):
    if sum(txn.values()) != 0:
        return False

    for key in txn:
        if key in state:
            account_balance = state[key]
        else:
            account_balance = 0

        if (account_balance + txn[key]) < 0:
            return False

    return True


def makeBlock(txns, chain):
    parent_block = chain[-1]
    parent_hash = parent_block['hash']
    block_number = parent_block['contents']['blockNumber'] + 1
    txn_count = len(txns)
    block_contents = {'blockNumber': block_number, 'parentHash': parent_hash,
                      'txnCount': len(txns), 'txns': txns}
    block_hash = hashMe(block_contents)
    block = {'hash': block_hash, 'contents': block_contents}

    return block
