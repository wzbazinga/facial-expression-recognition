import lmdb,caffe
import numpy as np

def main():
    with open('fer2013.csv','rb') as csvfile:
        buffer=csvfile.read().split('\n')
    buffer=map(lambda x:x.split(',')[:2],buffer)

    a=map(lambda x:int(x),buffer[1][1].split(' '))
    a1=np.array(a,dtype=np.uint8)
    b=np.array([int(buffer[1][0])])
    map_size=a1.nbytes+b.nbytes
    env_train=lmdb.open('fer_train_lmdb',map_size=map_size*28708*10)
    env_validate=lmdb.open('fer_validate_lmdb',map_size=map_size*3597*10)
    env_test=lmdb.open('fer_test_lmdb',map_size=map_size*3597*10)

    '''
    from PIL import Image
    img=Image.new("1",(48,48),(0,))
    for i in range(48*48):
        img.putpixel((i/48,i%48),int(buffer[3][1].split(' ')[i]))
    img.show()
    '''

    with env_train.begin(write=True) as txn:
        for i in xrange(1,28709):
            if i==200:
                break
            datum=caffe.proto.caffe_pb2.Datum()        
            datum.channels=1
            datum.height=48
            datum.width=48
            array=np.array(map(lambda x:int(x),buffer[i][1].split(' ')),dtype=np.uint8)
            datum.data=array.reshape(2304,1).tobytes()
            print (array.dtype),type(datum.data)
            datum.label=int(buffer[i][0])
            str_id="{:08}".format(i)
            txn.put(str_id.encode("ascii"),datum.SerializeToString())

    with env_validate.begin(write=True) as txn:
        for i in xrange(28709,32297):
            if i==29000:
                return
            datum=caffe.proto.caffe_pb2.Datum()        
            datum.channels=1
            datum.height=48
            datum.width=48
            array=np.array(map(lambda x:int(x),buffer[i][1].split(' ')),dtype=np.uint8)
            datum.data=array.reshape(2304,1).tobytes()
            datum.label=int(buffer[i][0])
            str_id="{:08}".format(i)
            txn.put(str_id.encode("ascii"),datum.SerializeToString())

    with env_test.begin(write=True) as txn:
        for i in xrange(32298,35887):
            datum=caffe.proto.caffe_pb2.Datum()        
            datum.channels=1
            datum.height=48
            datum.width=48
            array=np.array(map(lambda x:int(x),buffer[i][1].split(' ')),dtype=np.uint8)
            datum.data=array.reshape(2304,1).tobytes()
            datum.label=int(buffer[i][0])
            str_id="{:08}".format(i)
            txn.put(str_id.encode("ascii"),datum.SerializeToString())
        

if __name__=='__main__':
    main()
