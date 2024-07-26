import urllib.request, json, re, time, os, sys
from packaging.version import Version
from contextlib import closing
import requests

"""
需要修改的：
OBJECT_NAME      项目名称
APP_NAME         软件名称
VERSION_URL      版本检查列表
VERSION          当前版本
UPDATE_FILE_NAME 更新执行文件
UPDATE_FILE_URL  更新执行文件的下载地址
"""



class CheckUpdate():
    def __init__(self, app, 
                 OBJECT_NAME: str, 
                 APP_NAME: str, 
                 VERSION_URL: str, 
                 VERSION:str, 
                 REQUEST_USER_AGENT: str, 
                 UPDATE_FILE_NAME: str, 
                 UPDATE_FILE_URL: str):
        self.app = app

        self.OBJECT_NAME = OBJECT_NAME
        self.APP_NAME = APP_NAME
        self.VERSION_URL = VERSION_URL
        self.VERSION = VERSION
        self.REQUEST_USER_AGENT = REQUEST_USER_AGENT
        self.UPDATE_FILE_NAME = UPDATE_FILE_NAME
        self.UPDATE_FILE_URL = UPDATE_FILE_URL

    def check(self) -> bool:
        file_list= self.open_url(self.VERSION_URL)
        if not file_list: return True
        latestVersion = None
        latestFileName = None
        latestFileURL = None
        latestFileSize = None
        latestDatetime = None
        for file in file_list:
            print(file)
            version = re.findall(f'{self.APP_NAME}(.+?).zip', file[0])
            version = Version(version[0])
            if not latestVersion or version > latestVersion:
                latestVersion = version
                latestFileName = file[0]
                latestFileURL = self.VERSION_URL + latestFileName
                latestFileSize = file[1]
                latestDatetime = time.strftime("%Y-%m-%d", time.localtime(file[2]))
        
        if latestVersion > Version(self.VERSION): # 判断版本是否大于当前版本
            # 执行更新
            try:
                command = f'{self.UPDATE_FILE_NAME} {self.OBJECT_NAME} {latestVersion} {latestFileName} {latestDatetime} {latestFileSize} {latestFileURL} {self.APP_NAME}'
                files_in_directory = os.listdir('./')
                if self.UPDATE_FILE_NAME not in files_in_directory: self.get_update_file()
                print(command)
                os.popen(command)
                self.app.exit()
                sys.exit()
            except Exception as e:
                raise Exception(f'执行更新失败！{e}')
        else:
            # 继续执行
            return True
    
    def get_update_file(self):
        try:
            with closing(requests.get(self.UPDATE_FILE_URL, headers={'User-Agent': self.REQUEST_USER_AGENT}, stream=True)) as response:
                chunk_size = 1024
                with open(self.UPDATE_FILE_NAME, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
        except Exception as e:
            raise Exception(f'下载更新组件失败：{str(e)}')

    
    def open_url(self, url) -> list:
        if url:
            try:
                req = urllib.request.Request(url)
                req.add_header('User-Agent', self.REQUEST_USER_AGENT)
                response = urllib.request.urlopen(req)
                file_list = json.loads(response.readlines()[0])['files']
                return file_list
            except Exception as e:
                raise Exception(f'获取更新列表失败！{e}')
