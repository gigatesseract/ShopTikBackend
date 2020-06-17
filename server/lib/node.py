import json
from web3 import Web3


class Node:
    CONTRACT_NAME = "UserDatas"

    def __init__(self, account_dict, abi_path, contract_address, network_id, provider_url, unlock = False):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.address = Web3.toChecksumAddress(account_dict['address'])
        self.private_key = account_dict['private_key']
        self.contract_abi = Node.load_abi(abi_path)
        contract_address = self.contract_abi["networks"][str(network_id)]['address']
        self.contract = self.w3.eth.contract(address = contract_address, abi = self.contract_abi['abi'])
        if unlock:
            self.unlock_account()
        # self.w3.parity.personal.unlock_account(self.address, self.private_key, None)

    @staticmethod
    def load_abi(filepath):
        with open(filepath + '/' + Node.CONTRACT_NAME + '.json') as abi:
            return json.load(abi)

    def unlock_account(self):
        self.w3.parity.personal.unlock_account(self.address, self.private_key, None)

    def add_user_data(self, user_dict):
        receipt = self.contract.functions.addUser(
            self.address, user_dict['customer_id'], user_dict['slot_begin']
        ).transact({"from": self.address})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(receipt)
        return tx_receipt

    def get_all_user_data(self, customer_address):
        receipt = self.contract.functions.getAllUserDatas(customer_address).call()
        return receipt




