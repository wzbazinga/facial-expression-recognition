# Created by wz on 17-3-29.
# encoding=utf-8
# emo neutral happy surprise sadness anger disgust fear contempt unknown NF
# fer+   0     1      2        3      4      5      6       7      8     9
# fer    6     3      5        4      0      1      2
fermap = {0: 4, 1: 5, 2: 6, 3: 1, 4: 3, 5: 2, 6: 0}
import csv
import numpy as np
from PIL import Image

f = open('fer2013new.csv')
fer = open('../fer2013/fer2013.csv')
reader1 = csv.reader(f, delimiter=',', quotechar='|')
reader2 = csv.reader(fer, delimiter=',', quotechar='|')
ftrain = open('train.txt', 'w+')
fvalidate = open('validate.txt', 'w+')
ftest = open('test.txt', 'w+')
all = 0
diff = 0
for i, j in zip(reader1, reader2):
    if i[0] == 'Usage':
        # print i, j
        continue
    label1 = np.array(map(lambda x: int(x), i[2:]))
    label2 = int(j[0])
    img = np.array(map(lambda x: int(x), j[1].split(' ')), dtype=np.uint8)
    img.resize(48, 48)
    img = Image.fromarray(img, mode='L')
    name = 'pic/%d.png' % all
    img.save(name)
    label1 = np.argmax(label1)
    if label1 > 6:
        label1 = fermap[label2]
    if i[0] == 'Training':
        ftrain.write('%s %s\n' % (name, label1))
    elif i[0] == 'PublicTest':
        fvalidate.write('%s %s\n' % (name, label1))
    elif i[0] == 'PrivateTest':
        ftest.write('%s %s\n' % (name, label1))
    all += 1
    if all % 1000 == 0:
        print all

f.close()
fer.close()
ftrain.close()
fvalidate.close()
ftest.close()
