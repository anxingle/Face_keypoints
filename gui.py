# coding=utf-8
import os
#引入我的提取特征函数
import extract_feature as ex
#定时器
import time
import caffe
import sys
import struct
import sklearn.metrics.pairwise as pw
import numpy as np
import cv2
from PIL import Image  
import Tkinter  
#import Tkinter.filedialog  
import tkFileDialog
#import Tkinter.messagebox  
import tkMessageBox

  
class Window():  
    def __init__(self):  
        self.root = root = Tkinter.Tk()  
        self.menu = Tkinter.Menu(root)  
        self.submenu = Tkinter.Menu(self.menu, tearoff=0)  
        self.submenu.add_command(label='作者: 安兴乐')  
        root.config(menu=self.submenu)  
        self.Image = Tkinter.StringVar()  
        self.Image.set('.bmp')  
        self.feature = ex.get_bin(3)
        self.mstatus = Tkinter.IntVar()  
        self.fstatus = Tkinter.IntVar()  
        self.mstatus.set(0)  
        self.fstatus.set(0) 

        self.status = Tkinter.StringVar() 

        self.checkM = Tkinter.Checkbutton(self.root, text='风格转换(暂时不行呢)', command=self.OnCheckM, variable=self.mstatus, onvalue=1, offvalue=0)  
        self.checkM.place(x=5, y=55)
        #响应函数BrowserFile  
        self.label = Tkinter.Label(root, text='开启监控：')  
        self.label.place(x=5, y=10)  
        self.entryFile = Tkinter.Entry(root)  
        self.entryFile.place(x=85, y=10)  
        self.BrowserFileButton = Tkinter.Button(root, text='选择视频', command=self.BrowserFile)  
        self.BrowserFileButton.place(x=210, y=10) 
        self.BrowserDirButton = Tkinter.Button(root, text='显示视频(q键退出)', command=self.BrowserDir) 
        self.BrowserDirButton.place(x=5,y=85)
        #录入人脸
        self.label = Tkinter.Label(root, text='录入人脸(开发中)：')  
        self.label.place(x=5, y=35)
        self.entryFile = Tkinter.Entry(root)  
        self.entryFile.place(x=105, y=35)    
        self.BrowserFile = Tkinter.Button(root, text='录入人脸（需GPU设备）', command=self.BrowserFile)  
        self.BrowserFile.place(x=200, y=35) 
        #添加画布 显示图片
        self.canvas = Tkinter.Canvas(root,  
             width = 500,      # 指定Canvas组件的宽度  
             height = 300,      # 指定Canvas组件的高度  
             bg = 'white')      # 指定Canvas组件的背景色
        self.canvas.place(x=5,y=120)
  
    #风格转换
    def OnCheckM(self):  
        if not self.mstatus.get():  
            self.entryDir.config(state=Tkinter.DISABLED)  
            self.entryFile.config(state=Tkinter.NORMAL)  
            self.BrowserFileButton.config(state=Tkinter.NORMAL)  
            self.BrowserDirButton.config(state=Tkinter.DISABLED)  
        else:  
            self.entryDir.config(state=Tkinter.NORMAL)  
            self.entryFile.config(state=Tkinter.DISABLED)  
            self.BrowserFileButton.config(state=Tkinter.DISABLED)  
            self.BrowserDirButton.config(state=Tkinter.NORMAL)  
    #选择图片
    def BrowserFile(self):  
        file = tkFileDialog.askopenfilename(title='Python player', filetypes=[('MP4', '*.mp4'), ('BMP', '*.bmp'), ('GIF', '*.gif'), ('PNG', '*.png')])  
        if file:  
            self.entryFile.delete(0, Tkinter.END)  
            self.entryFile.insert(Tkinter.END, file)  
    #显示视频
    def BrowserDir(self):
        start_time = time.time()
        net = ex.initilize()
        print "entryFile is : ",self.entryFile.get()
        cap = cv2.VideoCapture(self.entryFile.get())
        #cap = cv2.VideoCapture(0)
        while(cap.isOpened()):  
            ret, frame = cap.read()  
            cv2.imshow('image', frame)
            cost = time.time()-start_time
            if cost%12 > 2  and cost%12 < 4:
                cv2.imwrite("./save.jpg",frame)
                feature_now = ex.extractFeature("./save.jpg",net)
                string = ["习近平","李克强","李克强的老婆"]
                for i in xrange(3):
                    correct = pw.cosine_similarity(feature_now,self.feature[i])
                    if correct > 0.85:
                        tkMessageBox.showinfo(title='aaa', message ="他是 "+string[i])  
            k = cv2.waitKey(20)  
            #q键退出
            if (k & 0xff == ord('q')):  
                break
        cap.release()  
        cv2.destroyAllWindows()
  
    def make(self, file, format=None):  
        im = Image.open(file)  
        mode = im.mode  
        if mode not in('L', 'RGB'):  
            im = im.convert('RGB')  
        width, height = im.size  
        s = self.entryNew.get()  
        if s == '':  
            Tkinter.messagebox.showerror('出错啦', '请输入百分比')  
            return  
        else:  
            n = int(s)  
        nwidth = int(width*n/100)  
        nheight = int(height*n/100)  
        thumb = im.resize((nwidth, nheight), Image.ANTIALIAS)  
        if format:  
            thumb.save(file[:(len(file)-4)] + '_thumb' + format)  
        else:  
            thumb.save(file[:(len(file)-4)] + '_thumb' + file[-4:])  
 
  
    def mainloop(self):  
        self.root.minsize(550, 550)  
        self.root.maxsize(550, 550)  
        self.root.title('视频人脸检索')  
        self.root.mainloop()  
  
  
  
if __name__ == "__main__":  
    window = Window()  
    window.mainloop()  