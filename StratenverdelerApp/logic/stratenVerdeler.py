from geopy import distance

from logic.memberCSV import MemberCSV
from logic.member import Member
from logic.street import Street

class StratenVerdeler():
    
    allStreetsOfGennep = ["1e Dwarsweg","2e Dwarsweg","Achter de Hoven","Anjerstraat","Arendstraat","Asterstraat","Augustinus","Bergstraat","Bierbrouwersgroes","Bleekstraat","Boomheide","Brabantweg","Brugstraat","Burg.Gilissenweg","Burg.van Banningstraat","Burg.Woltersstraat","Condorstraat","Davidlaan","De Gaest","De Genneper molen","De Poel","De Vang","Dieseltram","Doelen","Dopheide","Dr.Ariënsstraat","Dr.Nolensstraat","Dr.Poelsstraat","Dr.Schaepmanstraat","Duivenakkerstraat","Eksterstraat","Ellen Hoffmannplein","Emmastraat","Europaplein","Fazantstraat","Genneperhuisweg","Groene kruisstraat","Haspel","Havikstraat","Heidehof","Heijenseweg","Heinsbergstraat","Hezeland","Hoekweg","Hoenderweg","Horse Dwarsweg","Horsestraat","Houthakkersgroes","Houtstraat","Israëlstraat","Jasmijnstraat","Julianalaan","Kalander","Kalboerstraat","Kampweg","Kellerberg","Ketelhuis","Kleermakersgroes","Kleineweg","Kloosterstraat","Kollermolen","Korenbloemstraat","Korhoenstraat","Kraaienhof","Kraaiheide","Kromme Elleboog","Kromsteeg","Kruisstraat","Kuipersgroes","Langeweg","Lavendelstraat","Leerlooiersgroes","Leeuwerikstraat","Lijsterstraat","Logterberge","Logterbos","Logterheuvel","Loodsstraat","Maaskempweg","Maasstraat","Maasweg","Maria-oord","Markt","Martinushof","Melkstraatje","Merelstraat","Middelweg","Molenstraat","Moutstraat","Nachtegaalstraat","Niersdijk","Niersstraat","Niersweg","Nieuwstraat","Nijmeegseweg","Noordwal","Norbertplein","Oliestraat","Ottersumseweg","Paesplasweg","Panoven","Papierschepper","Pater Celiestraat","Patrijsstraat","Perron","Picardie","Pr.Beatrixstraat","Pr.Bernhardlaan","Pr.Hendrikstraat","Pr.Irenestraat","Pr.Margrietstraat","Pr.Marijkestraat","Puttershof","Randweg","Rijssenbeeklaan","Roggestraat","Rozenstraat","Seringenstraat","Sneeuwheide","Spechtstraat","Sperwerstraat","Spoorstraat","Spoorwegje","Stamelbergerdijk","Stationsweg","Steendalerstraat","Stiemensweg","St.Martinusstraat","St.Norbertusstraat","Struikheide","Torenstraat","Touwslagersgroes","'t Straatje","Van Brederodestraat","Van Gelrestraat","Van Loonstraat","Veerstraat","Voorhoevepark","Wagenstraat","Watertoren","Weverstraat","Wikkel","Wilhelminaplein","Willem Boyeweg","Winterheide","Zandpoort","Zandstraat","Zuidoosterlaan","Zuid-Oostwal","Zuidwal","Zwaluwstraat"]
    allStreetsOfOttersum = []
    allStreetsOfHeijen = []

    def __init__(self, csvFilePath, firstNameClm, middleNameClm, lastNameClm, birthDateClm, groupClm,streetClm, streetNumbrClm, postalCodeClm, townClm):
    
        self.firstNameClm = firstNameClm
        self.middleNameClm = middleNameClm
        self.lastNameClm = lastNameClm
        self.birthDateClm = birthDateClm
        self.groupClm = groupClm
        self.streetClm = streetClm
        self.streetNumbrClm = streetNumbrClm
        self.postalCodeClm = postalCodeClm
        self.townClm = townClm
        self.csvFilePath = csvFilePath


    def setupMembers(self):
        memberCSV = MemberCSV(self.csvFilePath, self.firstNameClm, self.middleNameClm, self.lastNameClm, self.birthDateClm, self.groupClm, self.streetClm, self.streetNumbrClm, self.postalCodeClm, self.townClm)
        members = memberCSV.getMembers()
        
        print("Kids list made")
        return members

    def setupStreets(self, town, streetList):
        streetObjectsList = []

        print("Setting up Street list with provided town name, this can take some time because of api calls...")
        for street in streetList:

            streetObject = Street(street, town)
            print([streetObject.name, streetObject.latitude, streetObject.longitude])

            if streetObject.longitude is not None and streetObject.latitude is not None:
                streetObjectsList.append(streetObject)
            else:
                print("street " + street + " has no valid address")
        
        print("Street list made")

        return streetObjectsList

    def verdeelStratenOverKinderen(self, town):
        memberData = self.setupMembers() # sets up the kids objects with coordinates generated from the csv
        memberDataWithoutLeiding = [ x for x in memberData if "Leiding" not in x.group] # remove leiding from object list
        memberDataWithoutLeidingOnlyInCertainTown = [ x for x in memberDataWithoutLeiding if town in x.address ] # only select objects with specified town
        processedMemberData = sorted(memberDataWithoutLeidingOnlyInCertainTown, key=lambda x: x.ageInDays)   # sort by age
        
        # processedMemberData = [Member("Guus", "Heijenseweg 72 Gennep 6591HD", 100, "Roze Cavia's", 51.690872, 5.973307)] # test purposes, reduce the list

        streetData = self.setupStreets(town, self.allStreetsOfGennep)

        for kid in processedMemberData:
            coordinatesKid = (kid.latitude, kid.longitude)
            
            streetDistances = []

            for i, street in enumerate(streetData):
                coordinatesStreet = (street.latitude, street.longitude)

                streetDistances.append([street.name, i, distance.distance(coordinatesKid, coordinatesStreet).kilometers])
                
            nearestStreet = min(streetDistances, key=lambda x: x[2])
            print(nearestStreet[0])
            kid.assignedStreet = nearestStreet[0]
            del streetData[nearestStreet[1]]

        # print(streetData)
        print("Deze straten zijn over:")
        for street in streetData:
            print(street.name)

        return processedMemberData