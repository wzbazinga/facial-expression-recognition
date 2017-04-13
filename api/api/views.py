# Created by wz on 17-4-10.
# encoding=utf-8

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.database import Database

baseurl = 'http://120.25.193.46/'


def getMongoCol():
    uri = "mongodb://%s" % ('localhost:27017')
    client = MongoClient(uri)
    db = Database(client, 'test')
    col = db.get_collection('UserImages')
    return col


@csrf_exempt
def example(req):
    ret = {'type': 'url',
           'image': baseurl + 'static/MonaLisa',
           'faces': [
               {
                   "faceRectangle": {
                       "left": 75,
                       "top": 65,
                       "width": 55,
                       "height": 55
                   },
                   "scores": {
                       "anger": 0.0000592936267,
                       "contempt": 0.009701225,
                       "disgust": 0.0000174590314,
                       "fear": 7.714585e-7,
                       "happiness": 0.174377829,
                       "neutral": 0.8152689,
                       "sadness": 0.0005051276,
                       "surprise": 0.00006942739
                   }
               }
           ]}
    return JsonResponse(ret)


@csrf_exempt
def upload(req):
    image = None
    id = None
    result = None
    ret = {
        'type': 'data',
        'image': image,
        'id': id,
        'faces': result
    }
    return JsonResponse(ret)


@csrf_exempt
def remark(req):
    id = None
    return JsonResponse({'err': 0})
