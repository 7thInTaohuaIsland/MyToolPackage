import numpy as np
import cv2
from CommonHelper.imgOperation import Norm
class mean_value_cal:
    def __init__(self,img:np.ndarray,winname="image",LU=(0,0),RB=(0,0),verbose=False):
        '''
        :param img:  type can be both uint8 and float
        :param winname: default name "image"
        :param LU: Left-Up-Coordinate (y,x)
        :param RB: Right-Bottom-Coordinate (y,x)
        :param verbose:
        '''
        self.img=img
        self.h,self.w=img.shape
        self.point1 = LU
        self.point2 = RB
        self.mean_value=-100
        self.winname=winname
        self.verbose=verbose
        self.fix_poin_flag = True

    @property
    def mean_package(self):
        '''
        :return: 【均值，画框的图像（Normed),左上角坐标，右下角坐标】
        '''
        if self.point2==(0,0) and self.point1==(0,0):
            self.fix_poin_flag=False
            cv2.namedWindow(self.winname)
            cv2.setMouseCallback(self.winname, self.__on_mouse)
            cv2.imshow(self.winname, Norm(self.img))
            cv2.waitKey(0)
        else:
            min_x = min(self.point1[1], self.point2[1])
            min_y = min(self.point1[0], self.point2[0])
            width = abs(self.point1[1] - self.point2[1])
            height = abs(self.point1[0] - self.point2[0])
            if min_x<0 or min_y<0 or min_y + height>=self.h or min_x + width>=self.w:
                print("out of boundry")
            cut_img=self.img[self.point1[0]:self.point2[0],self.point1[1]:self.point2[1]]
            self.mean_value=np.mean(cut_img)
            self.img2s=Norm(self.img)
            cv2.rectangle(self.img2s, (self.point1[1],self.point1[0]),(self.point2[1],self.point2[0]), (255, 0, 0), 2)
        if not self.fix_poin_flag:
            rpoint1=(self.point1[1],self.point1[0])
            rpoint2=(self.point2[1],self.point2[0])
        else:
            rpoint1=(self.point1[0],self.point1[1])
            rpoint2=(self.point2[0],self.point2[1])
        return self.mean_value, self.img2s, rpoint1, rpoint2

    def __on_mouse(self,event, x, y, flags, param):
        img2 = self.img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            self.point1 = (x, y)
            img2s=Norm(img2)
            cv2.circle(img2s, self.point1, 10, (0, 255, 0), 2)
            cv2.imshow(self.winname, img2s)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
            img2s = Norm(img2)
            cv2.rectangle(img2s, self.point1, (x, y), (255, 0, 0), 2)
            cv2.imshow(self.winname, img2s)
        elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
            self.point2 = (x, y)
            img2s = Norm(img2)
            cv2.rectangle(img2s, self.point1, self.point2, (255, 0, 0), 2)
            cv2.imshow(self.winname, img2s)
            min_x = min(self.point1[0], self.point2[0])
            min_y = min(self.point1[1], self.point2[1])
            width = abs(self.point1[0] - self.point2[0])
            height = abs(self.point1[1] - self.point2[1])
            if min_x<0 or min_y<0 or min_y + height>=self.h or min_x + width>=self.w:
                print("out of boundry")
            else:
                cut_img = self.img[min_y:min_y + height, min_x:min_x + width]
                self.mean_value=np.mean(cut_img)
                if self.verbose:
                    print("mean value: ",self.mean_value,end="  ")
                    rpoint1 = (self.point1[1], self.point1[0])
                    rpoint2 = (self.point2[1], self.point2[0])
                    print("LU: ",rpoint1,"  RB: ",rpoint2)
            self.img2s=img2s


if __name__=="__main__":
    img=cv2.imread("E:/test/trees/trees_002.jpg",0)
    val,img2,point1,point2=mean_value_cal(img,verbose=True).mean_package
    # val,img2,point1,point2=mean_value_cal(img,LU=(6,48),RB=(638,111),verbose=True).mean_package
    print(val,point1,point2)
    cv2.imshow("!",Norm(img2))
    cv2.waitKey(0)
    cv2.destroyAllWindows()