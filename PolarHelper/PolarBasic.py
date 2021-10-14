import numpy as np
from CommonHelper.imgOperation import interpolation
class ChannelSeparate:
    def __init__(self):
        self.pattern=[90,45,135,0]
    @property
    def pattern(self):
        return self.__pattern
    @pattern.setter
    def pattern(self,value):
        def __value_error():
            raise ValueError(
                "Value 'pattern' must be rearrangement of list [0,45,90,135] "
                "with list-length-4 and interger element.")
        def __whether_rearrange(list):
            for item in [90,45,135,0]:
                if item not in list:
                    __value_error()
                    break
        if len(value)!=4:
            __value_error()
        __whether_rearrange(value)
        self.__pattern=value
    def Separate(self,img)->dict:
        dict = {}
        y, x = img.shape
        (a,b,c,d)=self.__pattern
        dict[a] = img[0:y:2, 0:x:2]
        dict[b] = img[0:y:2, 1:x:2]
        dict[c] = img[1:y:2, 0:x:2]
        dict[d] = img[1:y:2, 1:x:2]
        return dict

class PolarCalculation:
    def __init__(self,img_src:np.ndarray,pattern=(90, 45, 135, 0),inter_flag=True):
        self.img_src = img_src
        self.pattern = pattern
        self.inter_flag=inter_flag

    def __channel_sepa(self, img):
        C = ChannelSeparate()
        C.pattern = self.pattern
        img_separated = C.Separate(img)
        return img_separated

    @property
    def CalRes(self):
        eps = 1e-8
        img_separated = self.__channel_sepa(self.img_src)
        if self.inter_flag:
            for key,value in img_separated.items():
                img_separated[key]=interpolation().inter(value)
        I = 0.5 * (img_separated[0] + img_separated[45] + img_separated[90] + img_separated[135])
        Q = img_separated[0] - img_separated[90]
        U = img_separated[45] - img_separated[135]
        Ip = np.sqrt(np.square(Q) + np.square(U))
        dolp = Ip / (I + eps)
        dolp[np.where(dolp > 1)] = 0
        aop = 0.5*np.arctan2(U, Q)
        return {"I": I,
                "Q": Q,
                "U": U,
                "dolp": dolp,
                "aop": aop}, img_separated