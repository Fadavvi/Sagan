import configparser
import os

def Read():
    ## Read configuration from cfg file
    configParser = configparser.ConfigParser()
    configFileName = 'cfg'
    Path = os.path.abspath(os.path.join( os.path.dirname(__file__),os.pardir))
    configParser.read(os.path.join(Path,'', configFileName))
    return configParser
    
  