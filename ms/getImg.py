import requests, re
from multiprocessing import Process, Lock, Value

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
from pymongo.mongo_client import MongoClient
from pymongo.database import Database

all = Value('i', 0)
lock = Lock()


def getMongoCol():
    uri = "mongodb://%s" % ('localhost:27017')
    client = MongoClient(uri)
    db = Database(client, 'test')
    col = db.get_collection('images')
    return col


def labor(query):
    url = 'https://cn.bing.com/images/search?view=detailv2&form=OIIRPO&q=%s' % query.replace(' ', '+')
    session = requests.session()
    r1 = session.get(url)
    html = r1.content
    remod = re.compile('IG:"(.*?)"')
    result = remod.findall(html)
    start = 1
    l = 35
    remod = re.compile('src="(.*?)"')
    for i in xrange(4000):
        col = getMongoCol()
        try:
            url = 'https://cn.bing.com/images/async?view=detailv2&SFX=1&first=%d&count=%d&q=%s&IG=%s&IID=images.3_1.3_2.3' % (
                start, l, query.replace(' ', '+'), result[0])
            start += l
            r2 = session.get(url)
            html = r2.content
            result = remod.findall(html)
            for j in result:
                j = j.replace('&amp;w=78&amp;h=78&amp;c=7', '')
                lock.acquire()
                v = all.value
                all.value += 1
                lock.release()
                r = requests.get(j)
                name = '%s%d' % (query, v)
                with open('pic/%s.jpg' % name, 'wb') as f:
                    f.write(r.content)
                col.insert_one({'id': v, 'name': name, 'url': j, 'state': 0})
        except Exception, e:
            print e


def main():
    pool = []
    pool.append(Process(target=labor, args=("smile people",)))
    pool.append(Process(target=labor, args=("sad people",)))
    pool.append(Process(target=labor, args=("surprise people",)))
    pool.append(Process(target=labor, args=("angry people",)))
    pool.append(Process(target=labor, args=("scared people",)))
    pool.append(Process(target=labor, args=("contempt people",)))
    pool.append(Process(target=labor, args=("disgusted people",)))
    pool.append(Process(target=labor, args=("people face",)))
    for i in pool:
        i.start()
    for i in pool:
        i.join()


if __name__ == '__main__':
    main()
