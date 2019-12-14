import requests
from requests.adapters import TimeoutSauce
import configparser
import os

class Timeout(TimeoutSauce):
    ## TimeOut class for Request module
    def __init__(self, *args, **kwargs):
        if kwargs['connect'] is None:
            kwargs['connect'] = 500
        if kwargs['read'] is None:
            kwargs['read'] = 500
        super(Timeout, self).__init__(*args, **kwargs)

def ReadConf():
    ## Read configuration from config file
    try:
        configParser = configparser.ConfigParser()
        configFileName = 'config'
        Path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        configParser.read(os.path.join(Path,'', configFileName))
        return configParser
    except:
        print('Error in reading config file')

def SaveFile(Data,Path):
    ## save given data in given path
    try:
        File = open(str(Path),'w+', encoding="utf-8")
        File.write(Data.decode("utf-8"))
        File.close()
        return True
    except:
        print('Error in saving file(s)')


if __name__ == '__main__':
    ## set timeout for request module
    requests.adapters.TimeoutSauce = Timeout
    ## Read config file
    Configurations = dict(ReadConf().items())
    if Configurations['output']['bro_enable'] :
        try:
            ## Downloadable Bro Int file URL
            BroUrl = str(Configurations['main']['misp_proto']) + '://' + str(Configurations['main']['misp_host']) + '/attributes/bro/download/' + str(Configurations['output']['bro_out_type'])
            response = requests.get(BroUrl, headers={'Authorization': str(Configurations['main']['misp_auth_key'])})
            ## Save Bro Int file to given path
            SaveFile(response.content,str(Configurations['output']['bro_output_path']))
        except:
            print('Error: Bro file download failed')    
        if Configurations['sagan']['auto_restart']:
            ## Restart Sagan / Reload data
            os.popen('pkill -9 SaganMain && sagan -u root')
    if Configurations['output']['snort_enable'] :
        try:
            ## Downloadable Snort rule file URL
            SnortUrl = str(Configurations['main']['misp_proto']) + '://' + str(Configurations['main']['misp_host']) + '/events/nids/snort/download'
            response = requests.get(SnortUrl, headers={'Authorization': str(Configurations['main']['misp_auth_key'])})
            ## Save Snort rules file to given path
            SaveFile(response.content,str(Configurations['output']['snort_output_path']))
        except:
            print('Error: Snort file download failed')
        if Configurations['sagan']['auto_restart']:
            ## Restart Sagan / Reload data
            os.popen('pkill -9 SaganMain && sagan -u root')
       

