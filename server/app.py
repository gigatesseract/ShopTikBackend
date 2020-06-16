'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from pprint import pprint as pp
import time
import datetime
import smtplib
import pyqrcode
import png
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders
from database_func import DB

app= Flask(__name__)

import lib.utils as u

CONFIG_FILE = 'config.yaml'


'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
CORS(app)
# alloted_ids = []
path = os.getcwd()
config_dict = u.read_config(CONFIG_FILE)
data = DB(config_dict['DB'])
alloted_ids = data.get_all_ids()
nodes = u.initialise_all_nodes(config_dict, alloted_ids)
print("---ALL NODES INITIALISED---")



#TODO: Add all the account addresses for shopkeepers, customers and admin.
#TODO: nodes['shop_keepers'] -> each key is account address
#TODO: nodes['admin'] -> each key is account address
#TODO: nodes['customers'] -> each key is accoutn address



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



#TEST SERVER
@app.route('/')
def apiCall():
	return jsonify({'success':True , 'message':'BASE URL'  })


#HELPER FUNCTIONS
#blockchain call for user Address
def getUserId():
	#TODO: ALLOT UNIQUE ID
		#insert web3 here
		global nodes
		(ele, nodes) = u.get_unique_id(nodes)
		return ele
#blockchain call for shop Address
def getShopId():
	#TODO: ALLOT UNIQUE ID
	global nodes
	(ele, nodes) = u.get_unique_id(nodes)
	return ele
	#insert web3 here
	 
#generate QR CODE IMAGE
def generateQRImage(qrCode,mailId):
	path = os.getcwd()
	print(qrCode,path)
	url = pyqrcode.create(qrCode)
	imageName = qrCode+'.png'
	url.png(imageName,scale=8)
	mail_content = '''Hey ,This is Your token for shop entry.'''
	#The mail addresses and password
	sender_address = 'shoptikmail@gmail.com'
	sender_pass = 'shoptikpw'
	receiver_address = mailId
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'SHOPTIK TOKEN'   #The subject line
	#The body and the attachments for the mail
	message.attach(MIMEText(mail_content, 'plain'))
	filename = path+'/'+ imageName
	attachment = open(filename, "rb") 
	p = MIMEBase('application', 'octet-stream') 
	p.set_payload((attachment).read()) 
	encoders.encode_base64(p) 
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
	message.attach(p) 
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print("MAILED SUCCESS")
	return True

#Track API
# Req JSON : 
# {
#   "customer_id": "cus234234........"
#   "admin_id": "0xBFe892..."
# }

# Response JSON :
# [
#   {
#     "id": 1,
#     "shop_id": "0xBFe892..",
#     "slot_begin": timestamp
#   }...

# ]


@app.route('/api/track', methods=['POST'])
def track_users():
	info =request.json
	admin_id = info['admin_id']
	customer_id = info['customer_id']
	[ids, shop_ids, slot_begins] = nodes[admin_id].get_all_user_data(customer_id)
	track_info = []
	for i in range(len(ids)):
		if shop_ids[i]!='':
			track_info.append({
				"id": ids[i],
				"shop_id": shop_ids[i],
				"slot_begin": datetime.datetime.fromtimestamp(slot_begins[i]).isoformat(),
			})
	pp(track_info)
	return jsonify(track_info)


#Register User API
# Req JSON : 
# {
# 	"name" : "jahnavi",
# 	"email" : "jansri7@gmail.com",
# 	"address" : "Anna Nagar",
# 	"phone" : 7358125151,
# 	"pwd" : "jay123vishaal"
# }

@app.route('/api/user/register',methods = ['POST'])
def user_register():
	info =request.json
	name = info['name']
	email = info['email']
	address = info['address']
	phone = info['phone']
	pwd = info['pwd']
	id_user = getUserId()
	if id_user is None:
		return jsonify({'message': 'No more nodes can be added to the chain', 'success': False})

	if data.check_user_name(email) == True:
			return jsonify({'message':'Email already exists' , 'success':False})

	data.add_user(id_user,name,email,address,phone,pwd)
	return jsonify({'success':True , 'message':'Customer successfully registered'  })


# Register Shop API
# Req JSON : 
# {
# 	"name" : "Reavathi Super Market",
# 	"lat" : 20.09,
# 	"lon" : 78.0987,
# 	"email" : "revSuperMart@gmail.com",
# 	"address" : "Anna Nagar",
# 	"phone" : 7358125151,
# 	"pwd" : "revSuperMart",
# 	"hold" : 65
# }
@app.route('/api/shop/register',methods = ['POST'])
def shop_register():
	info = request.json
	print(info)
	name = info['name']
	lat = info['lat']
	lon = info['lon']
	email = info['email']
	address = info['address']
	phone = info['phone']
	pwd = info['pwd']
	id_shop = getShopId()
	hold = info['hold']
	if data.check_shop_name(email) == True:
			return jsonify({'message':'Email already exists' , 'success':False})

	data.add_shop(id_shop,name,lat,lon,email,address,phone,pwd,hold)
	return jsonify({'success':True , 'message':'Shop successfully registered' })

#LOGIN API

#ADMIN LOGIN get method /api/admin/login/admin@shoptikmail.com/admin@123
@app.route('/api/admin/login/<email>/<pwd>')
def admin_login(email,pwd) :
	print(email,pwd)
	if(email == "admin@shoptikmail.com") :
			if(pwd == "admin@123"):
					return jsonify({'success' : True, 'message' : 'Admin Logged IN'})
			else:
					return jsonify({'success' : False, 'message' : 'Admin Not Logged IN'})
	else:
			return jsonify({'success' : False, 'message' : 'Admin Not Logged IN'})


#USER LOGIN /api/user/login/jansri7@gmail.com/jay123vishaal
@app.route('/api/user/login/<email>/<pwd>',methods = ['GET'])
def user_login(email,pwd):
	if data.check_user_name(email) == False:
			return jsonify({'message':'Email does not exist' , 'success':False})
	user_data = data.get_user_pwd(email)
	print(user_data)
	if user_data[0][0] == pwd:
			return jsonify({'message':'Customer login success' , 'success':True, 'id': user_data[0][1]})

	else:
			return jsonify({'message':'Incorrect User password ' , 'success':False})

#SHOP LOGIN  /api/shop/login/arnold@outlook.com/XTPwmHaZ
@app.route('/api/shop/login/<email>/<pwd>',methods = ['GET'])
def shop_login(email,pwd):
	print(email,pwd)
	if data.check_shop_name(email) == False:
			return jsonify({'message':'Email does not exist' , 'success':False})
	shop_data= data.get_shop_pwd(email)
	print(shop_data)
	if shop_data[0][0] == pwd:
			return jsonify({'message':'Shop login success' , 'success':True , 'id':shop_data[0][1]})

	else:
			return jsonify({'message':'Incorrect Shop password ' , 'success':False})


#SHOP API's
#INSERT STOCK
# {
# 	"product" : "RICE",
# 	"shop_id" : "nobob28y283obibiu182",
# 	"product_id" : "REV001"
# }
@app.route('/api/shop/stock/insert',methods = ['POST'])
def stock_insert():
	info = request.json 
	product = info['product']
	shop_id = info['shop_id']
	product_id = info['product_id']
	stat = data.insert_stock(product,shop_id,product_id)
	if stat==True:
		return jsonify({'success':True , 'message':'Stock successfully updated' })
	else:
		return jsonify({'success':False , 'message':'Stock already exists' })


#DELETE STOCK
@app.route('/api/shop/stock/delete/<shopId>/<productId>',methods = ['GET'])
def stock_delete(shopId,productId):
	print(shopId,productId)
	stat = data.delete_stock(shopId,productId)
	if stat==True:
		return jsonify({'success':True , 'message':'Stock successfully deleted' })
	else:
		return jsonify({'success':False , 'message':'Stock does not exist' })


#GET STOCK
@app.route('/api/shop/products/<shopId>')
def get_products_of_shop(shopId):
	response = data.get_products_of_shop(shopId)
	print(response)
	return jsonify(response)

#GET DETAILS OF SHOP
@app.route('/api/shop/details/<shopId>')
def get_shop_details(shopId):
    shopDetails = data.get_details_of_shop(shopId)
    response = {"shopId":shopId,"name":shopDetails[0],"email":shopDetails[1],"hold_limit":shopDetails[4],"shop_address":shopDetails[2],"image":shopDetails[5]}
    return jsonify(response)

#FOR BOTH <USER AND SHOP>
#API FOR SLOTS NUMBER api/shop/tokens/booked/2020-07-12/ChIJKRiIHAdkUjoRTKyswz_T8Mk
@app.route('/api/shop/tokens/booked/<date>/<shopId>', methods= ['GET'])
def get_stock_list(shopId,date):
	print(shopId)
	res = data.slot_crowding_for_display(date,shopId)
	print(res)
	return jsonify(res)



#USER's API
# API TO GET SHOPS NEARME
@app.route('/api/shop/nearme',methods=['GET'])
def shops_nearme():
	shops=data.get_all_details_of_all_shops()
	print(shops)
	return jsonify(shops)

#API FOR BOOKING TICKET 
# {
# 	"custId" : "cus06eybx",
# 	"shopId" : "ChIJKRiIHAdkUjoRTKyswz_T8Mk",
# 	"slot" : "2020-07-12 08:00:00"
# }
@app.route('/api/book/token', methods=['POST'])
def book_ticket():
	info = request.json
	print(info)
	cust_id = info['custId']
	shop_id = info['shopId']
	slot = info['slot']
	qr = cust_id+shop_id+slot
	stat = data.insert_token_transaction(cust_id,shop_id,slot,qr)
	mailId = data.get_user_mail_id(cust_id)
	#insert qr to image conversion code and mailing code
	if stat == True:
			stat1 = generateQRImage(qr,mailId)
			if stat1 == True:
					return jsonify({'success':True , 'qr':qr })
			else:
					return jsonify({'success':False,'message':"Ticket Booked Mail Failed Pls copy this image on Screen" })
	else:
			return jsonify({'success':False , 'qr': None })

@app.route('/api/user/tokens/<userId>')
def get_user_booked_tokens(userId):
	response = data.get_user_tokens(userId)
	return jsonify(response)

@app.route('/api/tokens/verify/<tokenId>')
def verify_token(tokenId):
	response = data.get_token_verified(tokenId)
	if response == None:
		return jsonify({"allow":False,"message":"Not a valid Token"})
	else:
		print(response)
		#insert block adding code here