#Create env

python3 -m venv project_env1

#Activate the environment

source project_env1/bin/activate

export FLASK_APP=app

pip install -r requirements.txt

flask db init

flask db migrate

flask db upgrade

#Run the code

flask run

----------------- Example of usage -----------------

Post request (json body format):

(POST) http://127.0.0.1:5000/top_plant

{
    "N":10
}

----------------------------------------------------

GET request:

(GET) http://127.0.0.1:5000/states

----------------------------------------------------

Post request (json body format):

(POST) http://127.0.0.1:5000/filter_state

{
    "state":"OR"
}

----------------------------------------------------
