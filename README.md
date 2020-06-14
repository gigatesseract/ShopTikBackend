# Flask React Boilerplate taken from [here](https://github.com/YaleDHLab/flask-react-boilerplate)


Simple boilerplate for a Flask backend and React client including:

* ES6 transpiling via Webpack
* Hot module reloading via Webpack Dev Server
* State management via Redux
* Tests via Pytest and Jest
* Linting via Pylint and Eslint
* Travis CI for automatic testing and linting

## Setting up the app

cd ShopAhead
`npm install --no-optional`    
`virtualenv env` (Creeating a virtual env for dependency management)    
`source env/bin/activate`    
`pip install -r requirements.txt`    

## Setting up the blockchain

After installing the dependencies, inside `ShopAhead` folder, run   
* `source env/bin/activate` (Activate the virtual environment)
* Run this in a separate terminal - `ganache-cli --account_keys_path='./server/blockchain/keys'` (This sets up a local blockchain)
* `chmod +x setup.sh` (Give permissions for setup script)
* `./setup.sh build` (Migrates the contracts)
* Take a look at `config.yaml`. It has info on which URL the blockchain is running, which accounts are shopkeepers, admin etc.


## Quickstart

Change directory into `server` and run `flask run`

The app exposes two routes:
* `api/transact` -> For shopkeeper to transact with chain. For now, dummy data is added once this route is called.    
(GET, no params)

* `api/track` -> For admin to query the chain with customer address. For now, the dummy data is queried.    
(GET, no params)    

For frontend:

```bash
npm run production
```

That will start the server on port 7082. To run the development server with hot module reloading, run:

```bash
npm run start
```

That will start the webpack dev server on port 7081.

## Tests

To run the Javascript tests (located in `src/tests/`), run:

```bash
npm run jest
```

To run the Python tests (located in `server/tests/`), run:

```bash
pytest
```

## Linting

To lint the Javascript files (located in `src`), run:

```bash
npm run lint-js
```

To lint the Python files (located in `server`), run:

```bash
npm run lint-py
```