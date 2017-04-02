# Created by wz on 17-3-29.
# encoding=utf-8
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive=GoogleDrive(gauth)

file=drive.CreateFile({'title':'fer.caffemodel'})
file.SetContentFile('../snapshot/fer_iter_20000.caffemodel')
file.Upload()

file=drive.CreateFile({'title':'fer.solverstate'})
file.SetContentFile('../snapshot/fer_iter_20000.solverstate')
file.Upload()
