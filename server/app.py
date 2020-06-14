'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from pprint import pprint as pp
import time
import datetime

import lib.utils as u

CONFIG_FILE = 'config.yaml'


'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
CORS(app)


config_dict = u.read_config(CONFIG_FILE)
nodes, pub_priv_keys = u.initialise_all_nodes(config_dict)
#TODO: Add all the account addresses for shopkeepers, customers and admin.
#TODO: nodes['shop_keepers'] -> each key is account address
#TODO: nodes['admin'] -> each key is account address
#TODO: nodes['customers'] -> each key is accoutn address


@app.route('/api/items')
def items():
  return jsonify([{'title': 'A'}, {'title': 'B'}])

##
# DEFAULT VIEW ROUTE
##
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/transact')
def add_user_data():
  '''Given user_id, shopkeeper_id, slot time information, add
      details to the chain.
  '''
  #TODO : GET account address from backend, for given user and shop
  user_dict = {
    'customer_id':pub_priv_keys[2]['address'],
    'slot_begin': int(time.time()),
    'slot_end': int(time.time())
  }

  user_dict_2 = {
    'customer_id': pub_priv_keys[3]['address'],
    'slot_begin': int(time.time()),
    'slot_end': int(time.time())
  }
  

  #TODO: SHOPKEEPER_ID holds the contract address of user sending request to add. (MUST BE SHOPKEEPER)
  shopkeeper_id_1 = pub_priv_keys[0]['address']
  shopkeeper_id_2 = pub_priv_keys[1]['address']
  print(nodes)
  if shopkeeper_id_1 in nodes['shop_keepers']:
    tx_receipt = nodes['shop_keepers'][shopkeeper_id_1].add_user_data(user_dict)

  if shopkeeper_id_2 in nodes['shop_keepers']:
    tx_receipt = nodes['shop_keepers'][shopkeeper_id_2].add_user_data(user_dict_2)

    print("Data added, \n")
    return jsonify(200)
  else:
    print("PERSON NOT SHOPKEEPER. ABORTING....")
    return jsonify(400)


@app.route('/api/track')
def track_users():
   #TODO: USER ID holds the contract address of user sending request
   #TODO: CUSTOMER ID holds the address of the customer needed to track

   user_id = pub_priv_keys[4]['address']
   customer_id = pub_priv_keys[2]['address']
   if user_id in nodes['admin']:
     [ids, shop_ids, slot_begins, slot_ends] = nodes['admin'][user_id].get_all_user_data(customer_id)
     track_info = []
     for i in range(len(ids)):
       if shop_ids[i]!='':
        track_info.append({
          "id": ids[i],
          "shop_id": shop_ids[i],
          "slot_begin": datetime.datetime.fromtimestamp(slot_begins[i]).isoformat(),
          "slot_ends": datetime.datetime.fromtimestamp(slot_ends[i]).isoformat()
        })

     pp(track_info)

     return jsonify(track_info)
   else:
     print("PERSON NOT ADMIN. ABORTING....")
     return jsonify(400)





  







