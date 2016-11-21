# coding=utf-8
import os  
from PIL import Image  
from PIL import ImageTk
import Tkinter  
#import Tkinter.filedialog  
import tkFileDialog
#import Tkinter.messagebox  
import tkMessageBox
from YC_API import *
import cv2
import numpy as np

yc_id  = 'anxingle'
secret =''
class Window():  
    def __init__(self):  
        self.root = root = Tkinter.Tk()  
        self.menu = Tkinter.Menu(root)  
        self.submenu = Tkinter.Menu(self.menu, tearoff=0)  
        self.submenu.add_command(label='作者: 安兴乐')  
        root.config(menu=self.submenu)  
        self.Image = Tkinter.StringVar()  
        self.Image.set('.bmp')  
        
        self.mstatus = Tkinter.IntVar()  
        self.fstatus = Tkinter.IntVar()  
        self.mstatus.set(0)  
        self.fstatus.set(0) 

        self.status = Tkinter.StringVar() 

        self.checkM = Tkinter.Checkbutton(self.root, text='对齐人脸(暂时不行呢)', command=self.OnCheckM, variable=self.mstatus, onvalue=1, offvalue=0)  
        self.checkM.place(x=5, y=30)
        #响应函数BrowserFile
        self.label = Tkinter.Label(root, text='选择人脸图片：')  
        self.label.place(x=5, y=10)  
        self.entryFile = Tkinter.Entry(root)  
        self.entryFile.place(x=85, y=10)  
        self.BrowserFileButton = Tkinter.Button(root, text='选择图片', command=self.BrowserFile)  
        self.BrowserFileButton.place(x=210, y=10) 
        self.ExtractInfoButton = Tkinter.Button(root, text='提取信息', command=self.ExtractInfo) 
        self.ExtractInfoButton.place(x=5,y=70) 
        
        #添加画布 显示图片
        self.canvas = Tkinter.Canvas(root,  
             width = 500,      # 指定Canvas组件的宽度  
             height = 600,      # 指定Canvas组件的高度  
             bg = 'white')      # 指定Canvas组件的背景色
        self.canvas.place(x=5,y=100)
 
    #人脸对齐
    def OnCheckM(self):  
        pass 
  
    #选择图片
    def BrowserFile(self):  
        #file = Tkinter.filedialog.askopenfilename(title='Python player', filetypes=[('JPG', '*.jpg'), ('BMP', '*.bmp'), ('GIF', '*.gif'), ('PNG', '*.png')])  
        file = tkFileDialog.askopenfilename(title='Python player', filetypes=[('JPG', '*.jpg'), ('BMP', '*.bmp'), ('GIF', '*.gif'), ('PNG', '*.png')])  
        if file:  
            self.entryFile.delete(0, Tkinter.END)  
            self.entryFile.insert(Tkinter.END, file)  
    #提取信息
    def ExtractInfo(self):
        print "entryFile is : ",self.entryFile.get()
        file = self.entryFile.get()
        #获得图片基本信息
        error,info,face_num,startX,startY,\
                width,height = face_dect(file,yc_id,secret)
        keyx,keyy = face_keypoints(file,yc_id,secret)
        img = cv2.imread(file)
        print "startX is: ",startX[0]
        print "startY is: ",startY[0]
        """
        img_save = cv2.rectangle(img,pt1=(startY[0],startX[0]),\
        	        pt2=(startY[0]+height[0],startX[0]+width[0]),\
        	        color=(0,0,255),lineType=8)
        """
        img_save = img.copy()
        #最上面的线
        img_save[startY[0]:startY[0]+2,startX[0]:startX[0]+width[0]]  = [0,255,0] #bgr 
        #最下面的线
        img_save[startY[0]+height[0]:startY[0]+height[0]+2,startX[0]:startX[0]+width[0]] = [0,255,0]
        #最左边的线
        img_save[startY[0]:startY[0]+height[0],startX[0]:startX[0]+2] = [0,255,0]
        #最右边的线
        img_save[startY[0]:startY[0]+height[0],startX[0]+width[0]:startX[0]+width[0]+2] =[0,255,0]
        img_save[startY[0]+height[0]:startY[0]+height[0]+4,startX[0]+width[0]:startX[0]+width[0]+4] =[0,255,0]
        #画出关键点
        for i in xrange(67):
        	img_save[int(keyy[0][i]):int(keyy[0][i])+3,int(keyx[0][i]):int(keyx[0][i])+3] =[0,0,255] 
        cv2.imshow("test ",img_save)
        #图片弹出5秒钟
        cv2.waitKey(5000)
        #销毁弹出的图片
        cv2.destroyAllWindows()
        file_pre = file.split('.')[0]
        cv2.imwrite(file_pre+"_.jpg",img_save)
        Image.open(file_pre+"_.jpg").save("temp.gif")
        im = Tkinter.PhotoImage(file="temp.gif") 
        self.canvas.create_image(200,230,image = im)
        self.label = Tkinter.Label(self.root, text='选择人脸图片：')  
        self.label.place(x=5, y=430)  
        #directory = Tkinter.filedialog.askdirectory(title='Python')  
        if self.entryFile:  
            self.entryDir.delete(0, Tkinter.END)  
            self.entryDir.insert(Tkinter.END, entryFile.get())   
    def mainloop(self):  
        self.root.minsize(550, 750)  
        self.root.maxsize(550, 750)  
        self.root.title('人脸信息提取')  
        self.root.mainloop()  
  
  
  
if __name__ == "__main__":  
    window = Window()  
    window.mainloop()  