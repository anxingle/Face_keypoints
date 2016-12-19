# coding=utf-8
import  caffe
import  cv2
import  numpy as np
import  sys
import  os
import struct
import sklearn.metrics.pairwise as pw

# 初始化函数的相关操作
def initilize():
    # 运行模型的prototxt
    deployPrototxt =  'D:/study/DeepCare/YunCong/caffe_vgg/VGG_FACE_deploy.prototxt'
    # 相应载入的modelfile
    modelFile = 'D:/study/DeepCare/YunCong/caffe_vgg/VGG_Face_finetune_iter_5000.caffemodel'
    print 'initilize ... '
    caffe.set_mode_cpu()
    #caffe.set_device(gpuID)
    net = caffe.Net(deployPrototxt, modelFile,caffe.TEST)
    return net  
# 提取特征并保存为相应地文件
def extractFeature(imagefile, net):
	# meanfile 也可以用自己生成的
    meanFile = 'D:/study/DeepCare/YunCong/caffe_vgg/face_mean.npy'
    # 对输入数据做相应地调整如通道、尺寸等等
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(meanFile).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  
    transformer.set_channel_swap('data', (2,1,0))  
    # set net to batch size of 1 如果图片较多就设置合适的batchsize 
    net.blobs['data'].reshape(1,3,224,224)      #这里根据需要设定，如果网络中不一致，需要调整
    num=0
    feature = np.zeros((1,4096))
    loop = 0
    #for imagefile in imageList:
    imagefile_abs = os.path.join("./", imagefile)
    #print imagefile_abs
    net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(imagefile_abs))
    out = net.forward()
    #fea_file = imagefile_abs.replace('.jpg',postfix)
    #print 'Num ',num,' extract feature ',fea_file
    feature1 = net.blobs['fc7'].data
    feature1 = np.reshape(feature1,(1,4096))
    return feature1
    #correct = pw.cosine_similarity(feature[0], feature[1])
    #return correct
def save_feature(imagefile,dict):
    net = initilize()
    feature = extractFeature(imagefile,net)
    f    = open(dict,"w")
    for i in xrange(1,4097):
        f.writelines("%.10f\n"%(feature[0][i-1]))
    f.close()
def get_bin(face_num):
    # 1.bin 习近平 2.bin 李克强 3.bin 李克强他老婆
    feature = np.zeros((face_num,1,4096),dtype=np.float32)
    for i in xrange(face_num):
        f = open("%d.bin"%(i+1),"r")
        readlines = f.readlines()
        count = 0
        for line in readlines:
            feature[i][0][count] = line
            count += 1
    return feature
if __name__ == '__main__':
    save_feature("./cheng.jpg","cheng.bin")