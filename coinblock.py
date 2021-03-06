import hashlib, json, sys
import random

def hashMe(msg=""):
    
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True) 
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

random.seed(0)

def makeTransaction(maxValue=3):
    # ele vai criar uma transação valida no valor de 1
    sign      = int(random.getrandbits(1))*2 - 1   # randomicamente ele vai escolher 1 ou -1
    amount    = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays   = -1 * alicePays

    return {u'Alice':alicePays,u'Bob':bobPays}

txnBuffer = [makeTransaction() for i in range(30)]

def updateState(txn, state):

    # NOTE: isso não é uma transação valida
    
    # se a transação for invalida, então ele atualiza o state
    state = state.copy() # show.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state

def isValidTxn(txn,state):
    if sum(txn.values()) is not 0:
        return False
    
    for key in txn.keys():
        if key in state.keys(): 
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False
    
    return True