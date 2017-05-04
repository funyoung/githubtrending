# -*- coding: utf-8 -*-

'''
youdao_API
Version 1.0 build 1472571518

use the net dictionary: youdao
this class need the valid youdao API_KEY
'''

import requests
from basicDict import basicDict
import json
import sys


class youdao_API(basicDict):
    """
    **12-11-2016更新！！**
    !!!!
    我发现了一个问题，在
    url_preffix = "http://fanyi.youdao.com/openapi.do?keyfrom=youdaoWord&key="
    这个语句里面，youdaoWord 是我自己申请API时候的应用名称
    别人申请的应该不是这个名称
    自己用的时候一定要换成自己的！！
    ```
    """
    url_preffix = "http://fanyi.youdao.com/openapi.do?keyfrom=githubtrending&key="
    url_suffix = "&type=data&doctype=json&version=1.1&q="
    current_json_text = ''
    current_error_code = 0
    def __init__(self, API_KEY = 'DEFAULT',API_URL= 'DEFAULT',API_PATH = "DEFAULT", name='youdao'):
        super(youdao_API, self).__init__(API_KEY, API_URL,API_PATH,name)
        pass

    def urlencode(self,word,print_RESULT = False):
        if sys.version_info <= (2,8):
            # in python 2
            import urllib
            encoded_word = urllib.quote(word)
            pass
        elif sys.version_info <= (3,8):
            # in python 3
            from urllib.parse import quote
            encoded_word = quote(word)
            pass
        else:
            pass
        if print_RESULT:
            print(encoded_word)
        return encoded_word
        pass

    def get_url(self,word,print_URL = False):
        url = self.url_preffix + self.API_KEY + self.url_suffix + self.urlencode(word)
        if print_URL:
            print(url)
            pass
        return url

    def get_json(self, word, print_JSON = False):
        url = self.get_url(word)
        net_request = requests.get(url)
        json_content = net_request.text
        self.current_json_text = json_content
        if print_JSON:
            print(json_content)
            pass
        self.check_API_KEY(json_content)
        return json_content

    def check_API_KEY(self,json_text, print_CODE = False):
        json_content = json.loads(json_text)
        code = json_content['errorCode']
        if print_CODE:
            print(code)
            pass
        if code == 50:
            msg = 'InValid ' + self.name + ' API_KEY!'
            raise RuntimeError(msg)
        self.current_error_code = code
        pass 

def main():
    e = youdao_API('1749671432')
    print(e.name)
    # print(e.API_KEY)
    e.get_url('数学',print_URL = True)
    json_text = e.get_json('数学')
    print(json_text)
    # e.check_API_KEY('{"query":"book","errorCode":50}')
    pass

if __name__ == "__main__":
    main()
    
