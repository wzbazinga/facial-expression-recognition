# Created by wz on 17-3-29.
# encoding=utf-8
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive=GoogleDrive(gauth)

fileList=drive.ListFile({}).GetList()
for f in fileList:
    if f['title']=='data.tar.gz':
        file1=drive.CreateFile({'id':f['id']})
        file1.GetContentFile('data.tar.gz')

