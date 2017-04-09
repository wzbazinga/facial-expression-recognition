# Created by wz on 17-4-7.
# encoding=utf-8
# smile people
# sad people
# surprise people
# angry people
# scared people
# contempt people
# disgusted people
# people face

import requests, re
import sys, ast,time
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.database import Database


def getMongoCol():
    uri = "mongodb://%s" % ('localhost:27017')
    client = MongoClient(uri)
    db = Database(client, 'test')
    col = db.get_collection('img')
    return col


def getEmo(img):
    url = 'https://www.microsoft.com/cognitive-services/en-us/emotion-api'
    upurl = 'https://www.microsoft.com/cognitive-services/Demo/EmotionDemo/RecognizeEmotion'
    session = requests.Session()
    r1 = session.get(url)
    time.sleep(1)
    html = r1.content
    remod = re.compile("antiForgeryToken = '(.*?)'")
    result = remod.findall(html)
    r2 = session.post(upurl,
                      data={'imageData': img, 'dataType': 'imageUrl',
                            '__RequestVerificationToken': result[0]},
                      headers={'referer': 'https://www.microsoft.com/cognitive-services/en-us/emotion-api',
                               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                               'origin': 'https: // www.microsoft.com'})
    time.sleep(1)
    return ast.literal_eval(r2.json())


def saveImg(session, url, o, query, all):
    print url
    remod = re.compile('id=(.*?)&')
    r = session.get(url)
    img = r.content
    name = '%s%d.jpg' % (query, all)
    with open('pic/' + name, 'wb') as f:
        f.write(img)
    col = getMongoCol()
    col.insert_one({'name': name, 'emo': o})

def main(query):
    url = 'https://cn.bing.com/images/search?view=detailv2&form=OIIRPO&q=angry+people'
    session = requests.session()
    r1 = session.get(url)
    html = r1.content
    remod = re.compile('IG:"(.*?)"')
    result = remod.findall(html)
    start = 1
    l = 35
    remod = re.compile('src="(.*?)"')
    all = 0
    for i in xrange(2000):
        try:
            url = 'https://cn.bing.com/images/async?view=detailv2&SFX=1&first=%d&count=%d&q=%s&IG=%s&IID=images.3_1.3_2.3' % (
                start, l, query.replace(' ', '+'), result[0])
            start += l
            r2 = session.get(url)
            html = r2.content
            result = remod.findall(html)
            for j in result:
                j = j.replace('&amp;w=78&amp;h=78&amp;c=7', '')
                res = getEmo(j)
                if len(res) > 0:
                    all += 1
                    saveImg(session, j, res, query, all)
                    print i, all
        except Exception,e:
            print e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'query string needed'
    else:
        query = sys.argv[1]
        main(query)
