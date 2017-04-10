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
import sys, ast, time


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
    try:
        ret = ast.literal_eval(r2.json())
        return ret
    except:
        return False


def main():
    for i in xrange(3000):
        try:
            r = requests.get('http://54.212.217.139:3000/next')
            res = r.json()
            v = res['err']
            if v == -1:
                continue
            elif v == -2:
                break
            url = res['url']
            id = res['id']
            ret = getEmo(url)
            result = {}
            if ret is False:
                continue
            if len(ret) == 0:
                result['haveface'] = False
            else:
                result['haveface'] = True
                result['json'] = ret
            r=requests.post('http://54.212.217.139:3000/put', json={'id': id, 'result': result})
            print r.content
        except Exception,e:
            print e


if __name__ == '__main__':
    main()
