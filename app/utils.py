import pandas as pd
from geopy.geocoders import Nominatim

def get_coordinates(name):
    geolocator = Nominatim(user_agent="app")
    location = geolocator.geocode(name)
    if location:
        result= [location.raw['lat'], location.raw['lon']]
    else:
        result = [None, None]
    return result

def treating_data(xls):
    coor = list()
    st = pd.read_excel(xls, 'ST19')
    st_data = st[["State abbreviation", "State annual net generation (MWh)"]]
    st_data = st_data[st_data['State annual net generation (MWh)'].notna()].drop(labels=0, axis=0)
    st_data["State annual net generation (MWh)"]= st_data["State annual net generation (MWh)"].abs()
    st_data["State annual net_percentage %"] = (st_data["State annual net generation (MWh)"]/st_data["State annual net generation (MWh)"].sum())*100
    for state in st_data["State abbreviation"]:
        coor.append(get_coordinates(state))
    st_data['Coordinates']=coor
    return st_data