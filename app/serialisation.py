from .modules import db, States, app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class State_schema(ma.Schema):
    class Meta:
        fields = ('id ','state','annual_net','annual_net_percentage','lat','lon')
        model = States
        sql_session = db.session
