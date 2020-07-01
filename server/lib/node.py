import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time



class Node:
    CONTRACT_NAME = "UserDatas"

    def __init__(self, w3, address, private_key, abi_path, contract_address, network_id, provider_url):
        self.w3 = w3
        self.address = Web3.toChecksumAddress(address)
        self.contract_abi = Node.load_abi(abi_path)
        contract_address = self.contract_abi["networks"][str(network_id)]['address']
        self.contract = self.w3.eth.contract(contract_address, abi=self.contract_abi['abi'])
        self.private_key = private_key
        self.w3.eth.defaultAccount = self.w3.eth.account.privateKeyToAccount(self.private_key);


    @staticmethod
    def load_abi(filepath):
        with open(filepath + '/' + Node.CONTRACT_NAME + '.json') as abi:
            return json.load(abi)

    def add_user_data(self, user_dict):
        time.sleep(5)
        nonce = self.w3.eth.getTransactionCount(self.address)
        shoptik_txn = self.contract.functions.addUser(
         user_dict['shop_id'], user_dict['customer_id'], user_dict['slot_begin']
         ).buildTransaction({
             'chainId':  15001,
             'nonce': nonce,
             })
        private_key = Web3.toBytes(hexstr=self.private_key)
        signed_txn = self.w3.eth.account.sign_transaction(shoptik_txn, private_key=private_key)
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.w3.toHex(self.w3.keccak(signed_txn.rawTransaction))

    def get_all_user_data(self, customer_address):
        receipt = self.contract.functions.getAllUserDatas(customer_address).call({'from': self.w3.eth.defaultAccount.address})
        return receipt




