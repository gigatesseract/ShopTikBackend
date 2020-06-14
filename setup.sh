# Run this inside server/
# THis script performs the following steps:
# if "build", then sets up the server, with the running ganache. (deploys migrations, gets the network id)
# if "run", then runs the server
if [ "$1" = "build" ]; then
    { 
        echo "Starting blockchain configuration" &&
        cd server &&
        cd blockchain &&
        rm -rf build &&
        truffle migrate &&
        cd ../lib &&
        network_id=$(python utils.py ../blockchain/build/contracts/UserDatas.json) &&
        echo "Network ID after transaction", $network_id &&
        cd .. &&
        sed -ri "s/^(\s*)(NETWORK_ID\s*:\s*.*\s*$)/\1NETWORK_ID : $network_id/" config.yaml &&
        echo "Contracts deployed! Ready to run backend server. Go into server directory and do 'flask run'"

    } || { 
        echo "Some problem occured. Unable to deploy."
    }
       
elif [ "$1" = "setup" ]; then
    {
        echo "Creating virtual env, Instaling requirements"
        pip install virtualenv
        virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
        deactivate
        echo "setup done. Activate virtual env using './setup.sh activate'"
    } || {
        echo "Unable to setup."
    }
else 
    echo "Invalid instruction. Exiting..."
fi    