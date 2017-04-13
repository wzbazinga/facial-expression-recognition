# !/usr/bin/env python
# coding=utf-8
# emotion neutral happy surprise sadness anger disgust fear contempt unknown NF
# fer+     0       1       2        3      4      5     6      7       8     9
# fer      6       3       5        4      0      1     2
# https://github.com/opencv/opencv/blob/master/data/lbpcascades/lbpcascade_profileface.xml
import csv, random
import numpy as np
import cv2
import imutils
import lmdb
import caffe

fermap = {6: 0, 3: 1, 5: 2, 4: 3, 0: 4, 1: 5, 2: 6}
all = 0
all1 = 0
all2 = 0
diff = 0
SIZE = 48
PAD = 15

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# profile_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
lbp_face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface_improved.xml')
# lbp_cascade = cv2.CascadeClassifier('lbpcascade_profileface.xml')

human_judger = False


def writeOne(img, label, degree):
    global face_cascade, profile_cascade
    global all, all1
    all1 += 1

    img = imutils.rotate(img, degree)
    if human_judger:
        x, y, w, h = SIZE, SIZE, SIZE, SIZE
    else:
        faces = face_cascade.detectMultiScale(img[SIZE - PAD:SIZE + PAD, SIZE - PAD:SIZE + PAD], 1.025, 6)
        if len(faces) == 0:
            return False, None

        x, y, w, h = faces[0]
        x = x + SIZE - PAD
        y = y + SIZE - PAD

    roi = img[y:y + w, x:x + h]
    roi = cv2.resize(roi, (SIZE, SIZE))

    name = 'pic/%d.png' % all
    cv2.imwrite(name, roi)
    line = name + ' %d' % label
    all += 1
    if all % 1000 == 0:
        print all, all1, all2

    return True, line


def writeLMDB(name, multilabels):
    n = multilabels.shape[0]
    m = multilabels.shape[1]
    multilabels = multilabels.reshape((n, m, 1, 1))
    map_size = multilabels.nbytes * 10
    env = lmdb.open('%s_labels' % name, map_size=map_size)

    with env.begin(write=True) as txn:
        for i in xrange(n):
            datum = caffe.proto.caffe_pb2.Datum()
            datum.channels = m
            datum.height = 1
            datum.width = 1
            datum.float_data.extend(multilabels[i].flat)
            datum.label = 0
            str_id = '{:08}'.format(i)

            txn.put(str_id, datum.SerializeToString())


def shuffleData(name, labels, multilabels):
    f = open('%s.txt' % name, 'w')
    index = range(len(labels))
    random.shuffle(index)
    labels = np.array(labels)[index]
    multilabels = np.array(multilabels)[index]

    f.write('\n'.join(labels))
    writeLMDB(name, multilabels)

    f.close()


def main():
    fernew = open('fer2013new.csv')
    fer = open('fer2013.csv')
    reader1 = csv.reader(fernew, delimiter=',', quotechar='|')
    reader2 = csv.reader(fer, delimiter=',', quotechar='|')
    global all2
    global diff

    train = []
    validate = []
    test = []
    tv = []
    total = []
    multitrain = []
    multivalidate = []
    multitest = []
    multitv = []
    multitotal = []

    for i, j in zip(reader1, reader2):
        all2 += 1
        print all2
        if i[0] == 'Usage':
            continue
        l = map(lambda x: int(x), i[2:])

        # single label
        l1 = np.argmax(np.array(l))
        l2 = int(j[0])
        if l1 != fermap[l2]:
            diff += 1
        if l1 > 7:
            l1 = fermap[l2]

        # multi label
        # determine face's existence by people judger
        if human_judger and l[-1] >= 5:
            continue
        multilabel = l[:-2]
        multis = sum(multilabel)
        if multis == 0:
            continue
        multilabel = map(lambda x: 1.0 * x / multis, multilabel)

        data = np.array(map(lambda x: int(x), j[1].split(' ')), dtype=np.uint8)
        data.resize(48, 48)
        # 直方图均衡化，效果不明显
        # data = cv2.equalizeHist(data)

        gray_border = np.zeros((144, 144), np.uint8)
        cv2.repeat(data, 3, 3, gray_border)

        if i[0] == 'Training':
            D = range(0, 21, 5)
            D.extend(range(355, 339, -5))
            for d in D:
                ret, line = writeOne(gray_border, l1, d)
                if ret:
                    train.append(line)
                    tv.append(line)
                    total.append(line)
                    multitrain.append(multilabel)
                    multitv.append(multilabel)
                    multitotal.append(multilabel)
        else:
            ret, line = writeOne(gray_border, l1, 0)
            if ret:
                total.append(line)
                multitotal.append(multilabel)
                if i[0] == 'PublicTest':
                    validate.append(line)
                    tv.append(line)
                    multivalidate.append(multilabel)
                    multitv.append(multilabel)
                elif i[0] == 'PrivateTest':
                    test.append(line)
                    multitest.append(multilabel)
    fernew.close()
    fer.close()
    print 'different:', diff
    print 'image data written completed'

    shuffleData('train', train, multitrain)
    shuffleData('validate', validate, multivalidate)
    shuffleData('test', test, multitest)
    shuffleData('total', total, multitotal)
    shuffleData('tv', tv, multitv)


if __name__ == '__main__':
    main()
