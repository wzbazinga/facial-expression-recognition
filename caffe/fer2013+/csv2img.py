# !/usr/bin/env python
# coding=utf-8
# emotion neutral happy surprise sadness anger disgust fear contempt unknown NF
# fer+     0       1       2        3      4      5     6      7       8     9
# fer      6       3       5        4      0      1     2

import csv
import numpy as np
import cv2
import imutils
from multiprocessing import Process, Lock, Value

fermap = {6: 0, 3: 1, 5: 2, 4: 3, 0: 4, 1: 5, 2: 6}
all = 0
all1 = 0
all2 = 0
SIZE = 48
diff = 0

v = Value('i', 0)
v1 = Value('i', 0)

ftrain = open('train.txt', 'w')
fvalidate = open('validate.txt', 'w')
ftest = open('test.txt', 'w')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

lock = Lock()
lock1=Lock()


def outputOne(img, label, type):
    global face_cascade
    gray_border = np.zeros((150, 150), np.uint8)
    gray_border[:, :] = 170
    gray_border[((150 / 2) - (SIZE / 2)):((150 / 2) + (SIZE / 2)),
    ((150 / 2) - (SIZE / 2)):((150 / 2) + (SIZE / 2))] = img

    global face_cascade
    lock1.acquire()
    faces = face_cascade.detectMultiScale(gray_border, 1.025, 6)
    lock1.release()
    if len(faces) != 1:
        return

    # return
    # else:
    #    cv2.imshow('noface',img)
    #    cv2.waitKey()
    x, y, w, h = faces[0]
    # cv2.rectangle(gray_border, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi = gray_border[y:y + w, x:x + h]
    roi = cv2.resize(roi, (SIZE, SIZE))
    # print x, y, w, h
    # cv2.imshow('face', gray_border)
    # cv2.waitKey()

    global all
    global all1
    global lock
    lock.acquire()
    tall1 = v1.value
    v1.value += 1
    tall = v.value
    v.value += 1
    lock.release()
    name = 'pic/%d.png' % tall
    cv2.imwrite(name, roi)
    if type == 'Training':
        ftrain.write(name + ' %d\n' % label)
    elif type == 'PublicTest':
        fvalidate.write(name + ' %d\n' % label)
    elif type == 'PrivateTest':
        ftest.write(name + ' %d\n' % label)
    if tall % 1000 == 0:
        print tall, tall1, all2


def labor(pair):
    global all2
    global diff
    for i, j in pair:
        all2 += 1
        if i[0] == 'Usage':
            # print i, j
            continue

        l1 = np.argmax(np.array(map(lambda x: int(x), i[2:])))
        l2 = int(j[0])
        if l1 != fermap[l2]:
            diff += 1
        if l1 > 6:
            l1 = fermap[l2]

        data = np.array(map(lambda x: int(x), j[1].split(' ')), dtype=np.uint8)
        data.resize(48, 48)

        # 直方图均衡化，效果不明显
        # data = cv2.equalizeHist(data)
        outputOne(data, l1, i[0])

        # continue
        if i[0] != 'Training':
            continue
        data1 = imutils.rotate(data, 5)
        outputOne(data1, l1, i[0])
        data1 = imutils.rotate(data, 10)
        outputOne(data1, l1, i[0])
        data1 = imutils.rotate(data, 15)
        outputOne(data1, l1, i[0])
        data1 = imutils.rotate(data, 20)
        outputOne(data1, l1, i[0])

        data1 = imutils.rotate(data, 365 - 5)
        outputOne(data1, l1, i[0])
        data1 = imutils.rotate(data, 365 - 10)
        outputOne(data1, l1, i[0])
        data1 = imutils.rotate(data, 365 - 15)
        outputOne(data1, l1, i[0])
        data1 = imutils.rotate(data, 365 - 20)
        outputOne(data1, l1, i[0])


def main():
    fernew = open('fer2013new.csv')
    fer = open('fer2013.csv')

    reader1 = csv.reader(fernew, delimiter=',', quotechar='|')
    reader2 = csv.reader(fer, delimiter=',', quotechar='|')

    pair = [(a, b) for a, b in zip(reader1, reader2)]
    l = len(pair)
    step = 9000
    pool = []
    for i in range(0, l, step):
        pool.append(Process(target=labor, args=[pair[i:i + step]]))
    for i in pool:
        i.start()
    for i in pool:
        i.join()

    print 'different:', diff

    fernew.close()
    fer.close()
    ftrain.close()
    fvalidate.close()
    ftest.close()


if __name__ == '__main__':
    main()
