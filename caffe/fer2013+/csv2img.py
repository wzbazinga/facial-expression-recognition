# !/usr/bin/env python
# coding=utf-8
# emotion neutral happy surprise sadness anger disgust fear contempt unknown NF
# fer+     0       1       2        3      4      5     6      7       8     9
# fer      6       3       5        4      0      1     2

import csv
import numpy as np
import cv2
import imutils

fermap = {6: 0, 3: 1, 5: 2, 4: 3, 0: 4, 1: 5, 2: 6}
all = 0

ftrain = open('train.txt', 'w')
fvalidate = open('validate.txt', 'w')
ftest = open('test.txt', 'w')


def outputOne(img, label, type):
    global all
    name = 'pic/%d.png' % all
    cv2.imwrite(name, img)
    if type == 'Training':
        ftrain.write(name + ' %d\n' % label)
    elif type == 'PublicTest':
        fvalidate.write(name + ' %d\n' % label)
    elif type == 'PrivateTest':
        ftest.write(name + ' %d\n' % label)
    all += 1
    if all % 1000 == 0:
        print all


def main():
    fernew = open('fer2013new.csv')
    fer = open('fer2013.csv')

    reader1 = csv.reader(fernew, delimiter=',', quotechar='|')
    reader2 = csv.reader(fer, delimiter=',', quotechar='|')

    diff = 0
    for i, j in zip(reader1, reader2):
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

    print 'different:', diff

    fernew.close()
    fer.close()
    ftrain.close()
    fvalidate.close()
    ftest.close()


if __name__ == '__main__':
    main()
