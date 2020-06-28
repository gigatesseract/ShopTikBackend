## Setting up the app :rocket:  

cd ShopTikBackend
`npm install --no-optional`    
`virtualenv env` (Creeating a virtual env for dependency management)    
`source env/bin/activate`    
`pip install -r requirements.txt`    

## Setting up the blockchain :link: 

After installing the dependencies, inside `ShopTikBackend` folder, run   
* `source env/bin/activate` (Activate the virtual environment)
* Run this in a separate terminal - `ganache-cli --account_keys_path='./server/blockchain/keys'` (This sets up a local blockchain)
* `chmod +x setup.sh` (Give permissions for setup script)
* `./setup.sh build` (Deploys the contracts)
* Take a look at `config.yaml`. It has info on which URL the blockchain is running, the ID of the network, etc.


## Quickstart :tomato:  

Change directory into `server` and run `flask run`
Make sure that the environment is activated. If not, run `source env/bin/activate`
For documentation on the routes, refer [this Postman Docs](https://www.getpostman.com/collections/dad0fa04781c17fa4fb7)