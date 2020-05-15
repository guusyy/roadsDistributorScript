import csv
import numpy as np
import pandas as pd

class MyCSV:
    __data = []

    def __init__(self, csvFilePath):
        self.csvFilePath = csvFilePath

    @classmethod
    def readFromFile(self, filePath):
        csv = MyCSV(filePath)
        csv.read()

        return csv

    @classmethod
    def writeToFile(self, filePath, array):
        a = np.asarray(array)
        pd.DataFrame(a).to_csv(filePath, ";", header=None, index=None)

        return MyCSV(filePath)

    def getData(self):

        return self.__data

    def read(self):
        self.__data.clear()

        print(self.csvFilePath)
        with open(self.csvFilePath) as csvfile:
            reader = csv.reader(csvfile, delimiter=';',  quoting=csv.QUOTE_MINIMAL) 
            for row in reader: # each row is a list
                self.__data.append(row)

        #remove the headerlabels of CSV from the list
        self.__data.pop(0)

        print("CSV data read and put into the memory")

        return self.__data