# -*- coding: utf-8 -*-
'''
用来读写配置文件
支持python3 和 python2
'''
import os 
# 导入configparser时候考虑版本问题
try:
    # python3.x 
    import configparser as configparser
except:
    # python2.7
    import ConfigParser as configparser
    
class configFile(object):
    path = ''
    file_exist = False # 默认文件不存在
    config = None
    def __init__(self,file_path):
        self.path = file_path
        self.read_file()
        return

    def read_file(self):
        if os.path.exists(self.path):
            self.file_exist = True
            try:
                self.config = configparser.ConfigParser()
                self.config.read(self.path)
            except:
                self.file_exist = False
        pass

    def get(self,section, item):
        if self.file_exist == False:
            return False
        try:
            result = self.config.get(section, item)
            return result
        except:
            return False
        pass
    

def main():
    example = configFile('conf.ini')
    key  = example.get('youdao','api_key')
    print(key)
    pass

if __name__ == "__main__":
    main()


    
