import pymongo

def DBConnection(Host='127.0.0.1',Port='27017',User='root',Password='',DbName='rules'):
    # make a connection to Mongo DB based on given informations
    DBConnection = pymongo.MongoClient(Host,username=User,password=Password)
    return DBConnection

def ReadFromMongo(DBObj,Limit=0,Skip=0,Query=None,Addetional=None):
    # Get all rules info from MongoDB
    if Query != None:
        if Addetional == None :
            RuleData = list(DBObj.find(Query).skip(Skip).limit(Limit).sort("_id",-1))
            return RuleData
        else:
            RuleData = list(DBObj.find(Query,Addetional).skip(Skip).limit(Limit).sort("_id",-1))
            return RuleData
    if Limit == 0 :
        RuleData = list(DBObj.find().sort("_id",-1))
        return RuleData
    elif Skip == 0:
        RuleData = list(DBObj.find().limit(Limit).sort("_id",-1))
        return RuleData
    elif Limit != 0 and Skip != 0:
        RuleData = list(DBObj.find().skip(Skip).limit(Limit).sort("_id",-1))
        return RuleData
