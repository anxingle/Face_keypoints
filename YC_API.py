# -*- coding: utf-8 -*-
"""
         @function  ：云丛科技人脸识别python-API 
         @author    : 安兴乐
         @time      : 2016-11-21 02:34
         @XXX       : 您可以随便使用，但请著明代码来源
"""
import requests
import base64
import cv2
import numpy as np
"""
function: 
          face_dect
args    : 
          file_name: yuncong id,yuncong passwd
return  : 
          result: number which 0 is success 
          info: just tell you success or fail
          face_num: the number of faces have been dected
          x,y: the coordinate(type is list)
          width,height: you know (type is list)
"""
def face_dect(file_name,id,secret): 
    img         = cv2.imread(file_name)
    ret,imgEn   = cv2.imencode('.png',img)
    imgBase64   = base64.b64encode(imgEn)
    param = {
        'app_id': id,
        'app_secret': secret,
        'img': imgBase64,
         'mode':False
        }
    result      = requests.post('http://120.25.161.56:7000/face/tool/detect',\
    	                        param)
    faces       = result.json()['faces']
    error_num   = result.json()['result']
    info        = result.json()['info']
    file_name   = file_name.split('.')[0]
    #frame_file  = open('frame1_'+file_name,'w')
    #keypt_file  = open('keypt1_'+file_name,'w')
    #print "face number is : ",len(faces)
    face_num    = len(faces)
    x           = []
    y           = []
    width       = []
    height      = []
    for loop in xrange(face_num):
    	x.append(faces[loop]['x'])
    	y.append(faces[loop]['y'])
    	width.append(faces[loop]['width'])
    	height.append(faces[loop]['height'])
    return error_num,info,face_num,x,y,width,height
"""
function: 
        face_attribute
args    : 
        file_name: yuncong id,yuncong passwd
return  : 
        face_num: the number of faces have been dected
        age     : age of the person (type is list)
        gender  : man or femel(type is list) 
"""
def  face_attribute(file_name,id,secret):
    img         = cv2.imread(file_name)
    ret,imgEn   = cv2.imencode('.png',img)
    imgBase64   = base64.b64encode(imgEn)
    param = {
        'app_id': id,
        'app_secret': secret,
        'img': imgBase64,
         'mode':False
        }
    result      = requests.post('http://120.25.161.56:7000/face/tool/attribute',\
                                param)
    faces       = result.json()['faces']
    face_num    = len(faces)
    age         = []
    gender      = []
    for loop in xrange(face_num):
        age.append(faces[loop]['age'])
        gender.append(faces[loop]['gender'])
    return face_num,age,gender
"""
function: 
        face_keypoints
args    : 
        file_name: yuncong id,yuncong passwd
return  : 
        x,y :  key points 
          type is  list and every element length is 68 
"""
def face_keypoints(file_name,id,secret):
    img         = cv2.imread(file_name)
    ret,imgEn   = cv2.imencode('.png',img)
    imgBase64   = base64.b64encode(imgEn)
    param = {
        'app_id': id,
        'app_secret': secret,
        'img': imgBase64,
         'mode':False
        }
    result      = requests.post('http://120.25.161.56:7000/face/tool/keypt',\
                                param)
    faces       = result.json()['faces']
    face_num    = len(faces)
    x           = np.zeros([face_num,68])
    y           = np.zeros([face_num,68])
    for loop in xrange(face_num):
        for i in xrange(68):
            x[loop][i] = int(faces[loop]['keypt'][i]['x'])
            y[loop][i] = int(faces[loop]['keypt'][i]['y'])
    return x,y