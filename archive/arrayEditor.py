class ArrayEditor:

    @staticmethod
    def removeRowsFromArrayIfColumnContainsStringPart(array, string, column):
        newArray = [ x for x in array if string not in x[column]]
    
        return newArray

    @staticmethod
    def removeRowsFromArrayIfColumnDoesNotContainStringPart(array, string, column):
        newArray = [ x for x in array if string in x[column] ]
        
        return newArray