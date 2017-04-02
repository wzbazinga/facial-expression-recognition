# Created by wz on 17-4-2.
# encoding=utf-8
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive=GoogleDrive(gauth)

file=drive.CreateFile({'title':'fer2013+.tar.gz'})
file.SetContentFile('../fer2013+.tar.gz')
file.Upload()