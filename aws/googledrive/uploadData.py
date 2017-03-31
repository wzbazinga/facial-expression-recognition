# Created by wz on 17-3-29.
# encoding=utf-8
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive=GoogleDrive(gauth)

file=drive.CreateFile({'title':'data.tar.gz'})
file.SetContentFile('../data.tar.gz')
file.Upload()
