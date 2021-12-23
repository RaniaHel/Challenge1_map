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
