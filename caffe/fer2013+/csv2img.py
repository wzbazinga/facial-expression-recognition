# !/usr/bin/env python
# coding=utf-8
# emotion neutral happy surprise sadness anger disgust fear contempt unknown NF
# fer+     0       1       2        3      4      5     6      7       8     9
# fer      6       3       5        4      0      1     2
#https://github.com/opencv/opencv/blob/master/data/lbpcascades/lbpcascade_profileface.xml
import csv
import numpy as np
import cv2
import imutils

fermap = {6: 0, 3: 1, 5: 2, 4: 3, 0: 4, 1: 5, 2: 6}
all = 0
all1 = 0
all2 = 0
diff = 0

SIZE = 48
A = ((144 / 2) - (SIZE / 2))
B = ((144 / 2) + (SIZE / 2))

ftrain = open('train.txt', 'w')
fvalidate = open('validate.txt', 'w')
ftest = open('test.txt', 'w')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
lbp_cascade=cv2.CascadeClassifier('lbpcascade_profileface.xml')

t=0
def outputOne(img, label, type, degree):
    global face_cascade
    global profile_cascade
    global all
    global all1
    global t
    all1 += 1

    img = imutils.rotate(img, degree)

    faces = face_cascade.detectMultiScale(img[A:B, A:B], 1.025, 6)
    if len(faces) == 0:
        #cv2.imshow('noface', img)
        #cv2.waitKey(100)
        return
        #faces=lbp_cascade.detectMultiScale(img[A - PAD:B + PAD, A - PAD:B + PAD], 1.025, 6)
        #if len(faces)==0:
            #cv2.imshow('noface',img)
            #cv2.waitKey(50)
            #t+=1
    #return
    #faces = profile_cascade.detectMultiScale(img[A - PAD:B + PAD, A - PAD:B + PAD], 1.025, 6)
    #if len(faces) != 0:
    #    cv2.imshow('profile',img)
    #    cv2.waitKey(100)
    #return

    x, y, w, h = faces[0]
    x = x + SIZE
    y = y + SIZE
    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #cv2.imshow('profile', img)
    #cv2.waitKey(50)
    #return
    roi = img[y:y + w, x:x + h]
    roi = cv2.resize(roi, (SIZE, SIZE))
    # print x, y, w, h
    #cv2.imshow('face', roi)
    #cv2.waitKey(100)
    #return

    name = 'pic/%d.png' % all
    cv2.imwrite(name, roi)
    if type == 'Training':
        ftrain.write(name + ' %d\n' % label)
    elif type == 'PublicTest':
        fvalidate.write(name + ' %d\n' % label)
    elif type == 'PrivateTest':
        ftest.write(name + ' %d\n' % label)
    all += 1
    if all % 1000 == 0:
        print all, all1, all2


def main():
    fernew = open('fer2013new.csv')
    fer = open('fer2013.csv')

    reader1 = csv.reader(fernew, delimiter=',', quotechar='|')
    reader2 = csv.reader(fer, delimiter=',', quotechar='|')

    global all2
    global diff
    for i, j in zip(reader1, reader2):
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
        # continue

        gray_border = np.zeros((144, 144), np.uint8)
        gray_border[:, :] = 170
        cv2.repeat(data, 3, 3, gray_border)

        if i[0] != 'Training':
            outputOne(gray_border, l1, i[0], 0)
            continue

        D = range(0, 21, 5)
        D.extend(range(345, 361, 5))
        for d in D:
            outputOne(gray_border, l1, i[0], d)
    print 't',t
    print 'different:', diff

    fernew.close()
    fer.close()
    ftrain.close()
    fvalidate.close()
    ftest.close()


if __name__ == '__main__':
    main()
