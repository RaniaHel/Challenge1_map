import json
from flask import request
from app import app
from .modules import db, States
from .serialisation import State_schema
from .utils import pd, get_coordinates, treating_st_data, treating_pnlt_data


content_type = {'Content-Type': 'application/json'}

@app.route("/", methods=['GET'])
def homepage():
    return 'Welcome to the Challenge 1'

@app.route("/top_plant", methods=['POST'])
def top_plant():
    content = request.get_json()
    result = dict()
    #Read the excel file
    xls = pd.ExcelFile('public/egrid2019_data.xlsx')
    #treating PNLT Data
    pnlt_data = treating_pnlt_data(content, xls)
    # Get the top on N plants and their coordinates
    plants = pnlt_data['Plant name state'].tolist()
    for plant in plants:
        result.update({plant: get_coordinates(plant)})
    return result

@app.route("/states", methods=['GET'])
def states():
    # Read the excel file
    xls = pd.ExcelFile('public/egrid2019_data.xlsx')
    # treating ST Data
    st_data=treating_st_data(xls)
    #Save the States's data to the database in State module
    state_json = json.loads(st_data.to_json(orient="records"))
    for data in state_json:
        newstate = States(state=data['State abbreviation'], annual_net=data['State annual net generation (MWh)'], annual_net_percentage=data['State annual net_percentage %'], lat=data['Coordinates'][0], lon=data['Coordinates'][1])
        if States.query.filter_by(state=data['State abbreviation']).first() is None:
            db.session.add(newstate)
    db.session.commit()
    return json.dumps(state_json), 200, content_type


@app.route("/filter_state", methods=['POST'])
def filter_state():
    #Filter according to the state and display it in Json format using the serializer State_schema()
    content = request.get_json()
    stateobj = States.query.filter_by(state=content["state"]).first()
    stateschema = State_schema()
    return stateschema.dumps(stateobj), 200, content_type


if __name__ == "__main__":
    app.run(debug=True)
