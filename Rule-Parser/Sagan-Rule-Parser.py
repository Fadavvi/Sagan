import re
import os
import sys
import argparse
import pymongo 

######## from modules
from modules import ConfRead
from modules import Mongo

#########################################################################################################
def ParsRules(Line):
    # Final Parser message will be sroted here 
    Rules = []

    Rule_Items = {}

    # Regex for first section of rules
    MainRegex = r"(?P<action>alert|drop) (?P<protocol>any|tcp|udp|icmp) (?P<source_ip>\$EXTERNAL_NET|\$HOME_NET|any|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<source_port>\S+) -> (?P<destination_ip>\$EXTERNAL_NET|\$HOME_NET|any|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<destination_port>\S+) \("
    
    # excract data from lines of rules 
    First_Part = list(re.finditer(MainRegex, Line, re.MULTILINE))
    
    try:
        Rule_Items = First_Part[0].groupdict()
    except EnvironmentError:
        # Rules Than didnt match to Regex (for debug)
        print('Rule did not match to Regex: ' , Line)
        print(EnvironmentError.with_traceback())

    # delete first part of rules
    Rest_of_rule = re.sub(MainRegex, '', Line)
    
    # extract other parts of rule
    Splited_items = Rest_of_rule.split(';')
    
    for items in Splited_items:
        Temp = items.lstrip().split(':', 1)

        if len(Temp) > 1 and (Temp[0] != ')\n' or Temp[0] != ')'):
            # For peer on configs (Conf: value;)
            cleanTemp1 = Temp[1].lstrip().rstrip()

            if Temp[0] in Rule_Items:
                if cleanTemp1.count('"')%2 != 0 :
                    cleanTemp1 += '"'
                if Temp[0] == 'event_id':
                    pass
                else:
                    Data = Rule_Items[Temp[0]]
                    if type(Data) != list:
                        Rule_Items.update({Temp[0] : [Data]})
                    Rule_Items[Temp[0]].append(cleanTemp1)
            else:
                # For closing any open "
                if cleanTemp1.count('"')%2 != 0 :
                    cleanTemp1 += '"'
                if Temp[0] == 'event_id':
                    pass
                else:
                    Rule_Items.update ({Temp[0] : cleanTemp1})
        # for single configs
        elif len(Temp) == 1:
            
            if (Temp[0] != ')\n' or Temp[0] != ')'):
                pass
            else:
                Rule_Items.update ({Temp[0] : 1})
        try:
            #add an additional field "Category" for better searching
            if Temp[0] == 'msg':
                if '[' in Temp[1]:
                    try:
                        category = list(re.finditer(r"\[(?P<category>[A-Z-_0-9]*)\]", Temp[1], re.MULTILINE))[0].groupdict()
                        if len(category) > 0:
                            Rule_Items.update(category)
                    except:
                        try:
                            category = list(re.finditer(r"\[(?P<category>[A-Za-z0-9-_]*)\]", Temp[1], re.MULTILINE))[0].groupdict()
                            if len(category) == 1:
                                Rule_Items.update(category)
                        except:
                            category = list(re.finditer(r"(?P<category>.*)", Temp[1], re.MULTILINE))[0].groupdict()
                            ClearedCategory = category['category'].replace(' ','').replace('/','').replace('-','_').replace('.','')
                            Rule_Items.update ({'category' : ClearedCategory})
                else:
                    category = list(re.finditer(r"(?P<category>.*)", Temp[1], re.MULTILINE))[0].groupdict()
                    ClearedCategory = category['category'].replace(' ','').replace('/','').replace('-','_').replace('.','')
                    Rule_Items.update ({'category' : ClearedCategory})
                
                #Make a name for --autoxbit option
                XbitName = Temp[1].replace('[','').replace(']','').replace(' ','').replace('/','').replace('-','_').replace('.','').replace(':','')
                if len(XbitName) > 30:
                    XbitName = XbitName[:30]

            #use rule id as _id in MongoDB (will be unique)
            if Temp[0] == 'sid':
                Rule_Items.update ({'_id' : int(Temp[1])})

            ## change event_id to old PCRE 
            # if Temp[0] == 'event_id':
            #     if ',' in Temp[1]:
            #         EventIDs = Temp[1].split(',')
            #         Text = '"/ '
            #         Count = len(EventIDs)
            #         X = 1
            #         for IDs in EventIDs:
            #             if Count == X :
            #                 Text = Text + str(IDs) + ': ' 
            #             else:
            #                 Text = Text + str(IDs) + ": | "
            #             X += 1
            #         Text += '/"'
            #     else:
            #         Text = '"/ ' + Temp[1] + ': /"'
                #Rule_Items.update ({'pcre' : [Text]})

            # add a default Xbit to rule    
            if Arguments.autoxbit :
                Rule_Items.update ({'xbits' : 'set, ' + XbitName.replace('"','').replace(',','') +', track ip_src, expire 86400'})

            #additional field for search and other things
            if Arguments.default == "1":
                Rule_Items.update ({'default' : 1}) # System defaults

            if Arguments.default == "2":
                Rule_Items.update ({'default' : 2}) # User defined

            # additional tag for seperate disabled and enabled rules    
            if Arguments.enabled :
                Rule_Items.update ({'enabled' : 1})

            # user defined tag 
            if Arguments.userdef != None:
                Rule_Items.update ({Arguments.userdef[0] : Arguments.userdef[1]})
            Rules.append(Rule_Items)

        except EnvironmentError:
            # for debug in error cases
            print(Temp)
            print(EnvironmentError.with_traceback())
    try:
        # add all parser rules to Mongo DB
        Result = RulesCollection.insert_many(Rules)
        return Result
    except:
        pass
    return 1   
#########################################################################################################
def ReadRuleFile(FilePath):
    #Read all files in given path (and sub pathes)
    Rule_file = open(FilePath,'r')
    Rule_file_content = Rule_file.readlines()
    Rule_file.close()
    for RuleLine in Rule_file_content:
        # Comments and empty lines
        if RuleLine[0:1] == '#' or RuleLine[0:1] == ' ' or RuleLine[0:1] == '\n' :
            pass
        else:
            # Main paerser
            ParsRules(RuleLine)
#########################################################################################################
def WriteRules2File():
    for RuleData in RulesCollection.find():
        print(RuleData)
#########################################################################################################
if __name__ == "__main__":
    ######################[Arguments section - Start]################################
    global Arguments
    parser = argparse.ArgumentParser(description='Sagan Utility: Rule Parser')
    parser.add_argument('--path', help='Path of rules')
    parser.add_argument('--enabled',action='store_true', help='add enabled tag to parsed rules')
    parser.add_argument('--default', help='add default tag to parsed rules')
    parser.add_argument('--autoxbit',action='store_true', help='add auto generated XBIT SET name to parsed rules')
    parser.add_argument('--userdef', nargs=2, help='add user defined (single) tag to parsed rules')
    Arguments = parser.parse_args()
    ########################[Arguments section - End]################################
    global Configs
    # Read MongoDB config from file
    Configs = dict(ConfRead.Read().items('db'))
    # Make a connection to MongoDB
    Connection = Mongo.DBConnection(Host=Configs['mongo_ip'],Port=Configs['mongo_port'],
                              User=Configs['mongo_user'],Password=Configs['mongo_password'],
                              DbName=Configs['mongo_dbname'])
    # Connect [or make] DB and collection in MongoDB
    global RulesCollection
    dbnames = Connection.list_database_names()
    if 'siem' not in dbnames:
        MainDB = Connection.siem
    MainDB = Connection['siem']
    RulesCollection = MainDB['rules']
    # Read & Pars!
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(Arguments.path):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    for Files in listOfFiles:
        ReadRuleFile(Files)
#########################################################################################################
     
