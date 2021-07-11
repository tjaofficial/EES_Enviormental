
# takes in the database array and returns wether it is empty True/False
def DBEmpty(DBArray):
    emptyDB = False
    if len(DBArray) is 0:
        emptyDB = True
    return emptyDB
