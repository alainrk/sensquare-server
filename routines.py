from utils import *

# TODO Testing hard on this!
def cleanRules():
    fID, fSENSOR, fMGRS, fGRAN, fEXPCOUNT, fTIMESTAMP = 0, 1, 3, 4, 5, 8
    
    # Remove the oldest by TIMEOUT
    queryObj = Query()
    delRules = queryObj.deleteOldRulesAndGetThem(italytimestamp())
    queryObj.close()

    # Remove the EXPIRE_COUNT reached
    queryObj = Query()
    rules = list(queryObj.getAllRules())

    for rule in rules:
        sensings = list(queryObj.getSensingForSensorByTimeAndZone(rule[fSENSOR], rule[fTIMESTAMP], rule[fMGRS], rule[fGRAN]))
        if len(sensings) >= rule[fEXPCOUNT]:
            print("len sensing, rule_expcount: ",len(sensings), rule[fEXPCOUNT])
            print("REMOVING RULE: ",rule[fID])
            delRules += rule
            queryObj.deleteRuleById(rule[fID])

    queryObj.close()
    return delRules
