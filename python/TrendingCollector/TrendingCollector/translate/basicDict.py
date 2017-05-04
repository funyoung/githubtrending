# -*- coding: utf-8 -*-

'''
base class of the dict
集成了获取API_KEY的方法
'''
import requests
from configFile import configFile

class basicDict(object):
    '''
    An API_KEY is required.
    '''
    name ='DEFAULT_DICTIONARY_NAME'
    API_KEY = ''
    has_API = False
    default_api_url = "http://127.0.0.1/api-key/youdao.html"
    API_url = ''
    def __init__(self,API_KEY = 'DEFAULT',API_URL= 'DEFAULT',API_PATH = "DEFAULT", name='DEFAULT_DICTIONARY_NAME'):
        # author's default situation
        self.name = name
        self.get_api_key_from_url(url = self.default_api_url)
        if self.has_API == True:
            return
        # directly use the key
        if not API_KEY == 'DEFAULT':
            self.API_KEY = API_KEY
            self.has_API = True
            return
        # use URL
        if not API_URL == 'DEFAULT':
            self.API_URL = API_URL
            self.get_api_key_from_url()
            return 
        # use conf file
        if not API_PATH == 'DEFAULT':
            config_file = configFile(API_PATH)
            key = config_file.get(self.name ,'api_key')
            if not key == False:
                self.API_KEY = key
                self.has_API = True
            else:
                pass
            return
        # no key
        error_message = 'Need ' +self.name + ' API_KEY!'
        raise RuntimeError(error_message)
        pass
    def get_api_key_from_url(self , url = 'DEFAULT'):
        if url == 'DEFAULT':
            url = self.API_URL
            pass
        try:
            q = requests.get(url)
            html_string = q.text
            code = q.status_code
            if code != 200:
                raise RuntimeError('Request Failed!')
                pass
            self.API_KEY = html_string.replace('\n','')
            self.has_API = True
            return True
        except:
            return False
        pass

def main():
    e = basicDict(API_PATH='conf.ini', name = 'youdao')
    print(e.API_KEY)
    print(repr(e.API_KEY))

if __name__ == "__main__":
    main()

    
