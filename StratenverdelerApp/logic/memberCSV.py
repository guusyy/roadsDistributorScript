from geopy.geocoders import Nominatim
from geopy import distance
from geopy.exc import GeocoderTimedOut
from datetime import datetime, timedelta

from logic.myCSV import MyCSV
from logic.member import Member

geolocator = Nominatim(user_agent="Bloembollenverdeler")

class MemberCSV(MyCSV):

    def __init__(self, csvFilePath, firstNameClm, middleNameClm, lastNameClm, birthDateClm, groupClm,streetClm, streetNumbrClm, postalCodeClm, townClm):
        super(MemberCSV, self).__init__(csvFilePath)

        self.firstNameClm = firstNameClm
        self.middleNameClm = middleNameClm
        self.lastNameClm = lastNameClm
        self.birthDateClm = birthDateClm
        self.groupClm = groupClm
        self.streetClm = streetClm
        self.streetNumbrClm = streetNumbrClm
        self.postalCodeClm = postalCodeClm
        self.townClm = townClm

    def getMembers(self):
        membersData = self.read()
        members = []

        for row in membersData:
            fullName = '{} {}'.format(row[self.firstNameClm],row[self.lastNameClm]) if row[self.middleNameClm] == '-' else '{} {} {}'.format(row[self.firstNameClm],row[self.middleNameClm],row[self.lastNameClm]) #sets First and Last name and if middle name isn't "-" will add that
            address = '{} {} {} {}'.format(row[self.streetClm],row[self.streetNumbrClm],row[self.postalCodeClm],row[self.townClm])
            ageInDays = self.__calculateAgeInDays(row[self.birthDateClm])
            group = row[self.groupClm]

            #calculate coordinates from address
            locationData = self.__addressToCoordinates(address)

            print(row)
            #create member object
            members.append(Member(fullName, address, ageInDays, group, locationData.latitude, locationData.longitude))
        
        return members

    def __calculateAgeInDays(self, birthDate):
        
        dateOfBirth = datetime.strptime(birthDate, "%d-%m-%Y")
        
        new_date = datetime.today() - dateOfBirth
        return new_date.days

    def __addressToCoordinates(self, address):
        #try except make sure service timeouts aren't taken into account and simply retries the method until proper callback is made
        try:
            return geolocator.geocode(address, timeout=10000)
        except GeocoderTimedOut:
            print("Error: geocode failed on input %s with message %s"%(address))