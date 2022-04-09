from web3 import Web3
# from const import *

def give_ether(receiver_address):
    WEBSITE = 'https://ropsten.infura.io/v3/f3ae459709c0486ba056f7b9a37a7b10'
    SENDER_ADDRESS = '0x6DE50c1a0569B145f9fC7c831a16517014804584'
    PRIVATE_KEY = '49424f47f7824846a6c189b2854978b850b16d91c3413499ca00f917761dc5fa'
    w3 = Web3(Web3.HTTPProvider(WEBSITE))
    sender_address = SENDER_ADDRESS
    priv_key = PRIVATE_KEY

    address1 = Web3.toChecksumAddress(sender_address)
    address2 = Web3.toChecksumAddress(receiver_address)

    nonce = w3.eth.getTransactionCount(address1)
    value = w3.toWei(.001, 'ether') 
    tx = {
        'nonce': nonce,
        'to': address2,
        'value': value,
        'gas': 21000,
        'gasPrice': w3.toWei(40, 'gwei')
    }

    signed_tx = w3.eth.account.signTransaction(tx, priv_key)

    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return f'You have received {value} ether for your food donation'