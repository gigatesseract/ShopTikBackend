import mysql.connector as MySQLdb

class DB:
    def __init__(self, db_dict):
        # db_dict = config_dict['DB']
        self.host = db_dict['HOST']
        self.user = db_dict['USER']
        self.pswd = db_dict['PASSWORD']
        self.db = db_dict['DB']
        self.conn =	None
        self.cur = None

    def db_connect(self):
        self.conn = MySQLdb.connect(user=self.user, password=self.pswd,host=self.host,database=self.db)
        self.cur = self.conn.cursor()


    def get_all_ids(self):
        self.db_connect()
        query = "select `id` from shop where 1"
        self.cur.execute(query)
        unique_ids = self.cur.fetchall()
        query = "select `id` from admin where 1"
        self.cur.execute(query)
        unique_ids += self.cur.fetchall()
        return unique_ids

    def add_user(self,id,name,email,address,phone,pwd):
            self.db_connect()
            print(phone)
            print(type(phone))
            query = "INSERT INTO customer (id,name,email,address,phone,password) VALUES('{0}','{1}','{2}','{3}',{4},'{5}')".format(id,name,email,address,phone,pwd)
            self.cur.execute(query)
            self.conn.commit()
            # return id

    def check_user_name(self,email):
        self.db_connect()
        query = "SELECT * FROM customer WHERE email = '{0}'".format(email)
        self.cur.execute(query)
        count = len(self.cur.fetchall())
        if count == 0:
            return False
        else:
            return True
    
    def get_user_pwd(self,email):
        self.db_connect()
        query = "SELECT password,id FROM customer WHERE email = '{0}'".format(email)
        self.cur.execute(query)
        return self.cur.fetchall()


    def check_shop_name(self,email):
        self.db_connect()
        query = "SELECT * FROM shop WHERE email = '{0}'".format(email)
        self.cur.execute(query)
        count = len(self.cur.fetchall())
        if count == 0:
            return False
        else:
            return True

    def add_shop(self, id, name, lat, lon, email, address, phone, pwd, hold, image_url):
            self.db_connect()
            query = "INSERT INTO shop (id,name,lat,lng,email,address,phone,password,hold_limit, image_url) VALUES('{0}','{1}',{2},{3},'{4}','{5}',{6},'{7}',{8}, '{9}')".format(id,name,lat,lon,email,address,phone,pwd,hold, image_url)
            self.cur.execute(query)
            self.conn.commit()
    
    def get_shop_pwd(self,email):
        self.db_connect()
        query = "SELECT password,id FROM shop WHERE email = '{0}'".format(email)
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def insert_stock(self,product,shop_id,product_id):
        self.db_connect()
        query = "SELECT * FROM stock WHERE product_id= '{0}' AND shop_id='{1}'".format(product_id,shop_id)
        self.cur.execute(query)
        count = len(self.cur.fetchall())
        if count == 0:
            query= "INSERT INTO stock(product,shop_id,product_id) VALUES('{0}','{1}','{2}')".format(product,shop_id,product_id)
            self.cur.execute(query)
            self.conn.commit()
            return True
        else:
            return False

    
    def delete_stock(self,shop_id,product_id):
        self.db_connect()
        query = "SELECT * FROM stock WHERE product_id= '{0}' AND shop_id='{1}'".format(product_id,shop_id)
        self.cur.execute(query)
        count = len(self.cur.fetchall())
        if count != 0:
            query= "DELETE FROM stock WHERE product_id= '{0}' AND shop_id='{1}'".format(product_id,shop_id)
            self.cur.execute(query)
            self.conn.commit()
            return True
        else:
            return False
    
    def slot_crowding(self,slot,shop_id):
        self.db_connect()
        query = "SELECT * FROM transactions WHERE slot= '{0}' AND shop_id='{1}'".format(slot,shop_id)
        self.cur.execute(query)
        count = len(self.cur.fetchall())
        query2="SELECT hold_limit FROM shop WHERE id= '{0}' ".format(shop_id)
        self.cur.execute(query2)
        limit=self.cur.fetchone()
        print("LIMIT",limit[0])
        limit = count/limit[0]
        return count,limit
    
    #date  ' YYYY-MM-DD hh:mm:ss ' 
    def slot_crowding_for_display(self,date,shop_id):
        self.db_connect()
        slots = ["8:00","08:45","09:30","10:15","11:00","11:45","12:30","13:15","14:00","14:45"]
        response=[]
        for i in slots:
            slot = date + " " + i +":00"
            print(self.slot_crowding(slot, shop_id))
            result= self.slot_crowding(slot, shop_id)
            count = result[0]
            limit = result[1]
            if(limit > 0.75):
                limitd = "danger"
            elif(limit > 0.35):
                limitd = "warning"
            else:
                limitd = "success"
            response.append({"slot":i,"count":count,"class":limitd})
        return response

    def insert_token_transaction(self,customer_id,shop_id,slot,QR):
        self.db_connect()
        query= "INSERT INTO transactions (customer_id,shop_id,slot,QR) VALUES('{0}','{1}','{2}','{3}')".format(customer_id,shop_id,slot,QR)
        self.cur.execute(query)
        self.conn.commit()
        return True

    def get_shops_nearme(self):
        self.db_connect()
        query= "SELECT id,name,address,phone,image_url FROM shop"
        self.cur.execute(query)
        response=self.cur.fetchall()
        return response
    
    def get_products_of_shop(self,shopId):
        self.db_connect()
        query="SELECT product, product_id from stock where shop_id= '{0}'".format(shopId)
        self.cur.execute(query)
        response=self.cur.fetchall()
        return response

    def get_all_details_of_all_shops(self):
        shop= self.get_shops_nearme()
        response=[]
        for i in shop:
            products=self.get_products_of_shop(i[0])
            response.append({"shop":{"id":i[0],"name":i[1],"address":i[2],"phone":i[3],"image":i[4]} , "products":products})
        return response
    
    def get_user_mail_id(self,custId):
        self.db_connect()
        query="SELECT email FROM customer WHERE id= '{0}'".format(custId)
        self.cur.execute(query)
        response = self.cur.fetchall()[0][0]
        return response
    
    # def add_report_against_shop(self,shopId,slot,message):
    #     self.db_connect()
    #     query = "INSERT INTO report () VALUES('{0}','{1}','{2}','{3}')".format(customer_id,shop_id,slot,QR)

    def get_details_of_shop(self,shopId):
        self.db_connect()
        query="select name,email,address,phone,hold_limit,image_url from shop where id='{0}'".format(shopId)
        self.cur.execute(query)
        return self.cur.fetchall()[0]

    def get_user_tokens(self,userId):
        self.db_connect()
        query="select shop_id,slot,qr from transactions where customer_id='{0}'".format(userId)
        self.cur.execute(query)
        responses = []
        response = self.cur.fetchall()
        print("DET OF USER",response)
        for i in response:
            shopDetails = self.get_details_of_shop(i[0])
            print("SHOP DETAILS : ",shopDetails)
            responses.append({"shopId":i[0],"name":shopDetails[0],"email":shopDetails[1],"hold_limit":shopDetails[4],"shop_address":shopDetails[2],"image":shopDetails[5],"slot":i[1],"qr":i[2]})
            print("RES",responses)
        return responses

    def get_all_customer_names(self):
        self.db_connect()
        query = "select  `id`, `name`, `email` from customer where 1"
        self.cur.execute(query)
        unique_ids = self.cur.fetchall()
        return unique_ids

    def get_shop_name(self, id):
        self.db_connect()
        query = "select name from `shop` where `id` = '{0}'".format(id)
        self.cur.execute(query)
        response = self.cur.fetchall()
        return response[0]


    def get_token_verified(self,tokenId):
        self.db_connect()
        query= "select customer_id,shop_id from transactions where QR ='{0}'".format(tokenId)
        self.cur.execute(query)
        response = self.cur.fetchall()
        if len(response) > 0 :
            return response[0]
        else:
            return None
        
