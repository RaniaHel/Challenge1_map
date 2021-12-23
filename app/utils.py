import pandas as pd
from geopy.geocoders import Nominatim

def get_coordinates(name):
    #Get the coordinates (latitude, longitude) of plants and states
    geolocator = Nominatim(user_agent="app")
    location = geolocator.geocode(name)
    if location:
        result= [location.raw['lat'], location.raw['lon']]
    else:
        result = [None, None]
    return result

def treating_st_data(xls):
    coor = list()
    #Read sheet ST19
    st = pd.read_excel(xls, 'ST19')
    st_data = st[["State abbreviation", "State annual net generation (MWh)"]]
    #Delete Nan rows
    st_data = st_data[st_data['State annual net generation (MWh)'].notna()].drop(labels=0, axis=0)
    # Get value absolute of State annual net generation
    st_data["State annual net generation (MWh)"]= st_data["State annual net generation (MWh)"].abs()
    # Get percentage of state annual net
    st_data["State annual net_percentage %"] = (st_data["State annual net generation (MWh)"]/st_data["State annual net generation (MWh)"].sum())*100
    #Add the coordinates to the dataframe
    for state in st_data["State abbreviation"]:
        coor.append(get_coordinates(state))
    st_data['Coordinates']=coor
    return st_data

def treating_pnlt_data(content, xls):
    # Read sheet PLNT19
    plnt = pd.read_excel(xls, 'PLNT19')
    data = plnt[["Plant state abbreviation", "Plant name", "Plant annual net generation (MWh)"]]
    # Delete Nan rows
    data = data[data['Plant annual net generation (MWh)'].notna()].drop(labels=0, axis=0)
    #Sort the plant according to the annual net generation of plants Descending and the N top plants
    df = data.sort_values(by='Plant annual net generation (MWh)', ascending=False,ignore_index=True).head(content["N"])
    # Add plant and state name to the dataframe
    df['Plant name state']= df['Plant name'] + ' ' +df['Plant state abbreviation']
    return df