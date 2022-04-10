from web3 import Web3

w3 = Web3(Web3.HTTPProvider(
    'https://ropsten.infura.io/v3/45530c1b8ac04f39b9c4890d42b5c493'
))
print(w3.isConnected())
import os
print(os.getcwd())
dir=os.getcwd()
file1 = open(dir+"//algorithms/privatekey.txt", "r")
privKey=file1.read()
file1.close()
# print(w3.eth.default_account)
foundingTitan=w3.eth.account.privateKeyToAccount(privKey)
w3.eth.default_account = foundingTitan.address
print(foundingTitan.address)
# print(w3.eth.default_account)

file2=open(dir+"//algorithms//abi","r")
abi=file2.read()
file2.close()
file3=open(dir+"//algorithms//bytecode","r")
bytecode=file3.read()
file3.close()
# mikoContract = w3.eth.contract(abi=abi, bytecode=bytecode)
# tx_hash = mikoContract.constructor(1000000000).transact()
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

tx_hash="0xa8bb08c6b530a6e747a091e2ae870fd23834bd60ac5d8c1c8d15d50f638fccc1"
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(tx_receipt)
# print(tx_receipt.contractAddress)
miko = w3.eth.contract(
     address="0x5C1701120A15e2c6c221CC6BBFc6A39F138978AC",
     abi=abi
 )
def credit(receiver,amount):
    if(receiver=="0x761a4e3eCcbd68FC81B989202086EE2Bb4156A4A"):
        receiver=foundingTitan.address
    contract_call = miko.functions.transfer(receiver, amount)
    nonce = w3.eth.get_transaction_count(foundingTitan.address)  
    unsigned_txn = contract_call.buildTransaction({'chainId': 3, 'nonce': nonce, 'gasPrice': w3.toWei(100, 'gwei')})
    signed_txn = w3.eth.account.sign_transaction(unsigned_txn, private_key=privKey)
    op=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # print(op)
    return f'{amount} MIKO has been credited to your wallet successfully'

def checkBal(user):
    bal=miko.functions.balanceOf(receiver).call()
    return bal
    
if __name__=="__main__":
    receiver="0x6DE50c1a0569B145f9fC7c831a16517014804584"
    contract_call = miko.functions.transfer(receiver, 1)  
    nonce = w3.eth.get_transaction_count(foundingTitan.address)  
    unsigned_txn = contract_call.buildTransaction({'chainId': 3, 'nonce': nonce, 'gasPrice': w3.toWei(100, 'gwei')})
    signed_txn = w3.eth.account.sign_transaction(unsigned_txn, private_key=privKey)
    op=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(op)
    balence1= miko.functions.balanceOf(foundingTitan.address).call()
    balance2= miko.functions.balanceOf(receiver).call()
    print(balence1)
    print(balance2)





