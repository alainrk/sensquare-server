from utils import *

# TODO Testing hard on this!
def cleanRules():
    fID, fSENSOR, fMGRS, fGRAN, fEXPCOUNT, fTIMEOUT = 0, 1, 3, 4, 5, 7
    # Remove the oldest by TIMEOUT
    queryObj = Query()
    queryObj.deleteOldRules(italytimestamp())
    queryObj.close()

    # Remove the EXPIRE_COUNT reached
    queryObj = Query()
    rules = list(queryObj.getAllRules())

    for rule in rules:
        sensings = list(getSensingForSensorByTimeAndZone(rule[fSENSOR], rule[fTIMEOUT], rule[fMGRS], rule[fGRAN]))
        if len(sensings) >= rule[fEXPCOUNT]:
            queryObj.deleteRuleById(rule[fID])

    queryObj.close()
