from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from database_func import DB

app= Flask(__name__)
CORS(app)
data = DB()

#TEST SERVER
@app.route('/')
def apiCall():
    return jsonify({'success':True , 'message':'BASE URL'  })


#HELPER FUNCTIONS
#blockchain call for user Address
def getUserId():
    #insert web3 here
    return "nobob28y283obibiu182"
#blockchain call for shop Address
def getShopId():
    #insert web3 here
    return "nobob28y283obibiu182"
#generate QR CODE IMAGE
def generateQRImage(qrCode,mailId):
    print(qrCode)
    #put qr image gen fucntion here
    #put send mail here
    return True


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

if __name__ == "__main__":
    app.run(debug=True)