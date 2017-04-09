# Created by wz on 17-4-4.
# encoding=utf-8
import cv2
import caffe
import numpy as np

SIZE = 48
deploy = 'deploy.prototxt'
model = 'snapshot/fer_iter_20000.caffemodel'
mean_file = 'fer2013+/train.npy'


class Classfier:
    def __init__(self):
        self.emomap = {0: 'neutral', 1: 'happy', 2: 'surprise', 3: 'sadness', 4: 'anger', 5: 'disgust', 6: 'fear'}
        self.face_cascade = cv2.CascadeClassifier('fer2013+/haarcascade_frontalface_default.xml')
        self.mu = np.load(mean_file)
        self.mu.resize((SIZE, SIZE))
        self.net = caffe.Net(deploy, model, caffe.TEST)
        self.video_capture = cv2.VideoCapture(0)
        cv2.namedWindow('emotion detector')

    def classify(self, img):
        img = (img - self.mu) / 255
        self.net.blobs['data'].data[...] = img
        out = self.net.forward()['prob']
        return out

    def detect(self, img):
        if len(img.shape) > 2:
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            grayimg = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
        faces = self.face_cascade.detectMultiScale(grayimg, 1.2, 6)
        labels = []
        for face in faces:
            x, y, w, h = face
            print 'face ', x, y, w, h,
            faceimg = grayimg[y:y + w, x:x + h]
            try:
                fimg = cv2.resize(faceimg, (SIZE, SIZE))
            except Exception, e:
                print e
                return [], []
            label = self.classify(fimg)
            print self.emomap[np.argmax(label)]
            labels.append(np.copy(label))

        return faces, labels

    def drawEmotions(self, frame, faces, labels):
        if len(faces) != 0:
            for face, label in zip(faces, labels):
                x, y, w, h = face
                e = self.emomap[np.argmax(label)]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, e, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
        cv2.imshow('emotion detector', frame)

    def loop(self):
        while True:
            ret, frame = self.video_capture.read()
            faces, labels = self.detect(frame)
            self.drawEmotions(frame, faces, labels)
            cv2.waitKey(10)

    def detectOne(self, imgname='e.jpg'):
        im = cv2.imread(imgname)
        faces, labels = self.detect(im)
        self.drawEmotions(im, faces, labels)
        cv2.waitKey()


def saveface(imgname='e.jpg'):
    img = cv2.imread(imgname)
    if len(img.shape) > 2:
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        grayimg = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    face_cascade = cv2.CascadeClassifier('fer2013+/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(grayimg, 1.1, 6)
    for i, face in enumerate(faces):
        x, y, w, h = face
        faceimg = np.copy(grayimg[y:y + w, x:x + h])
        cv2.imwrite('face%d.png' % i, faceimg)


def main():
    classfier = Classfier()
    classfier.loop()
    # classfier.detectOne('e.jpg')
    # saveface()


if __name__ == '__main__':
    main()
