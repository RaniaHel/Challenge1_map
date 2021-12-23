from .utils import *
from flask import request
import json
import pandas as pd
from .serialisation import *

content_type = {'Content-Type': 'application/json'}

@app.route("/", methods=['GET'])
def homepage():
    return 'Welcome to the Challenge 1'

@app.route("/top_plant", methods=['POST'])
def top_plant():
    result = dict()
    content = request.get_json()
    xls = pd.ExcelFile('public/egrid2019_data.xlsx')
    plnt = pd.read_excel(xls, 'PLNT19')
    data = plnt[["Plant state abbreviation", "Plant name", "Plant annual net generation (MWh)"]]
    data = data[data['Plant annual net generation (MWh)'].notna()].drop(labels=0, axis=0)
    df = data.sort_values(by='Plant annual net generation (MWh)', ascending=False,ignore_index=True).head(content["N"])
    df['Plant name state']= df['Plant name'] + ' ' +df['Plant state abbreviation']
    plant_list = df['Plant name state'].tolist()
    for plant in plant_list:
        result.update({plant: get_coordinates(plant)})
    return result

@app.route("/states", methods=['GET'])
def states():
    xls = pd.ExcelFile('public/egrid2019_data.xlsx')
    st_data=treating_data(xls)
    state_json = json.loads(st_data.to_json(orient="records"))
    for data in state_json:
        newstate = States(state=data['State abbreviation'], annual_net=data['State annual net generation (MWh)'], annual_net_percentage=data['State annual net_percentage %'], lat=data['Coordinates'][0], lon=data['Coordinates'][1])
        if States.query.filter_by(state=data['State abbreviation']).first() is None:
            db.session.add(newstate)
    db.session.commit()
    return json.dumps(state_json), 200, content_type



@app.route("/filter_state", methods=['POST'])
def filter_state():
    content = request.get_json()
    stateobj = States.query.filter_by(state=content["state"]).first()
    stateschema = State_schema()
    return stateschema.dumps(stateobj), 200, content_type


if __name__ == "__main__":
    app.run(debug=True)
