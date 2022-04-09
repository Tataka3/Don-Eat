from posts import constants
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(constants.WEBSITE))

sender_address = constants.SENDER_ADDRESS
receiver_address = constants.RECEVER_ADDRESS
priv_key = constants.PRIVATE_KEY

address1 = Web3.toChecksumAddress(sender_address)
address2 = Web3.toChecksumAddress(receiver_address)

nonce = w3.eth.getTransactionCount(address1)

tx = {
    'nonce': nonce,
    'to': address2,
    'value': w3.toWei(.001, 'ether'),
    'gas': 21000,
    'gasPrice': w3.toWei(40, 'gwei')
}

signed_tx = w3.eth.account.signTransaction(tx, priv_key)

tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)