from geopy import distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
# from flask_sqlalchemy import SQLAlchemy
# from flask import current_app as app
# from datetime import datetime

# db = SQLAlchemy(app)

# class StreetData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     streetName = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id

geolocator = Nominatim(user_agent="Bloembollenverdeler")

class Street:

    def __init__(self, name, town):
        self.name = name
        self.town = town

        self.__addressToCoordinates()

    def __addressToCoordinates(self):
        #try except make sure service timeouts aren't taken into account and simply retries the method until proper callback is made
        try:
            locationData = geolocator.geocode((self.name + " " + self.town), timeout=10000)
            self.latitude = locationData.latitude
            self.longitude = locationData.longitude

            return locationData
        except GeocoderTimedOut:
            print("Error: geocode failed on input %s with message %s"%(self.name))