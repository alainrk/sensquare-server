from utils import *

def cleanRules():
    fEXPCOUNT = 5

    queryObj = Query()
    rules = list(queryObj.deleteOldRules(italytimestamp()))
    queryObj.close()


    # TODO Implement remove for EXPIRE_COUNT
    # Use this: select * from all_wifi_data where mgrs regexp '32TPQ867[[:digit:]]{2}312[[:digit:]]{2}'

    # queryObj = Query()
    # rules = list(queryObj.getAllRules())
    # queryObj.close()
    #
    # oldRules = list(filter(lambda x:x[fEXPCOUNT] >= timeNow, rules))
    # if oldRules:
    #     queryObj = Query()
    #     for rule in oldRules:
    #         pass
    #     queryObj.close()
