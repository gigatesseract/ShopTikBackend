import json
import yaml
from pprint import pprint as pp
from web3 import Web3
import sys


def get_network_id(build_json_path):
    build_json = get_keys_json(build_json_path)
    for id in build_json['networks']:
        return id
    


def initialise_all_nodes(config_dict, alloted_ids):
    from .node import Node
    nodes = {
        "alloted_ids": [],
        "free_ids": [],
        "addresses": {}
    }
    for id in alloted_ids:
        actual_id = id[0]
        nodes['alloted_ids'].append(actual_id)
    
    keys_file_path = config_dict['DEFAULT']['ACCOUNT_KEYS_PATH']
    abi_path = config_dict['DEFAULT']['ABI_FILE_PATH']
    network_id = config_dict['DEFAULT']['NETWORK_ID']
    keys_json = get_keys_json(keys_file_path)
    pub_priv_keys = get_pub_priv_keys(keys_json)
    w3 = Web3(Web3.HTTPProvider(config_dict['DEFAULT']['GANACHE_URL']))
    w3.eth.defaultAccount = w3.eth.accounts[0]
    js = Node.load_abi(abi_path)
    bytecode = js['bytecode']
    ShopContract = w3.eth.contract(abi=js['abi'], bytecode=bytecode)
    tx_hash = ShopContract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("contact deployed. This is the details----\n")
    pp(tx_receipt)
    for id in nodes['alloted_ids']:
        nodes['addresses'][pub_priv_keys[id]['address']] = Node(pub_priv_keys[id],abi_path,tx_receipt.contractAddress,network_id, config_dict['DEFAULT']['GANACHE_URL'], True)

    for address in pub_priv_keys:
        if address not in nodes['alloted_ids']:
            nodes['free_ids'].append(address)
    return nodes


def get_unique_id(nodes):
    if len(nodes['free_ids']) == 0:
        return (None, nodes)
    else:
        last = nodes['free_ids'].pop()
        nodes['alloted_ids'].append(last)
        return (last, nodes)


def read_config(path):
    with open(path) as o:
        return yaml.load(o)


def get_keys_json(path):
    with open(path) as keys_json:
            return json.load(keys_json)



def convert_buf_to_hex(buffer):
    hex_string = '0x'
    for number in buffer:
        hex_value = hex(number)[2:]
        if len(hex_value) == 1:
            hex_value  = '0' + hex_value
        hex_string += hex_value
    return hex_string

def get_pub_priv_keys(keys_json):
    accounts_details = {}
    address = ''
    accounts = keys_json['addresses']
    for account in accounts.keys():
        # accounts_details[counter] = {}
        account_info = {
            'address': Web3.toChecksumAddress(account),
            'public_key': '',
            'private_key': ''
        }
        address = Web3.toChecksumAddress(account)
        
        account_info['public_key'] = convert_buf_to_hex(accounts[account]['publicKey']['data'])
        account_info['private_key'] = convert_buf_to_hex(accounts[account]['secretKey']['data'])
        accounts_details[address] = account_info
        # counter+=1

    return accounts_details

if __name__ == '__main__':
    network_id = get_network_id(sys.argv[1])
    print(network_id)