import cv2
import os
import sys
import numpy as np
from PyQt5.QtGui import QImage

class read:
    def imread(self,fname,flag=0):
         if os.path.isfile(fname):
             img=cv2.imread(fname,flags=flag)
             return img
         else:
             print("'{0}'   does not exist".format(fname))
             sys.exit(0)

    def readraw(self,fname,x,y,type=np.uint16):
        if 'raw' not in fname:
            raise ValueError('wrong form of images')
        rawData = np.fromfile(fname,dtype=type)
        img=rawData.reshape(y,x)
        return img

class write:
    def imwrite(self,fname,img)->None:
        dir=os.path.dirname(fname)
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("'{0}'   has been made".format(dir))
        cv2.imwrite(fname,img)

def QimgSwitch(img):
    height, width =img.shape
    bytesPerline = 3 * width
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    qImg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
    return qImg