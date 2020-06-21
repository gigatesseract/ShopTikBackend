cd /home/praveen/ShopAhead
source env/bin/activate
cd server
uwsgi --http 127.0.0.1:5000 --module app:app

