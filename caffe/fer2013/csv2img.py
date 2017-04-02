#!/usr/bin/env python
# coding=utf-8
import csv
from PIL import Image

def main():
    with open('fer2013.csv','r') as csvfile:
        reader=csv.reader(csvfile,delimiter=',',quotechar='|')
        
        ftrain=open('train.txt','w')
        fvalidate=open('validate_mini.txt','w')
        ftest=open('test_mini.txt','w')
        trains,validates,tests=0,0,0
        for i in reader:
            if i[2]=='Usage':
                continue
            #img=Image.new('L',(48,48),(0,))
            #ps=map(lambda x:int(x),i[1].split(' '))
            #for j in range(48*48):
            #    img.putpixel((j%48,j/48),(ps[j],))
                
            if i[2]=='Training':
                #img.save('images_train/%d.png'%(trains),'png')
                ftrain.write('images_train/%d.png %s\n'%(trains,i[0]))
                trains+=1
                
            if i[2]=='PublicTest':
                #img.save('images_validate/%d.png'%(validates),'png')
                fvalidate.write('images_validate/%d.png %s\n'%(validates,i[0]))
                validates+=1
                #if validates==100:
                #    break
                
            if i[2]=='PrivateTest':
                #img.save('images_test/%d.png'%(tests),'png')
                ftest.write('images_test/%d.png %s\n'%(tests,i[0]))
                tests+=1
                if tests ==100:
                    break
        ftrain.close()
        fvalidate.close()
        ftest.close()

if __name__=='__main__':
    main()
