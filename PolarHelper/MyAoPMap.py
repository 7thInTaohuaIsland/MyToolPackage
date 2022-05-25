from CommonHelper.imgIO import read
import numpy as np
import cv2
from CommonHelper.imgOperation import Norm,interpolation
from PolarHelper.PolarBasic import ChannelSeparate
import time
import os
from CommonHelper.fileIO import file_reader

class my_aop_map:
    def __init__(self,AoP:np.ndarray):
        self.AoP = AoP

    @property
    def map_res(self):
        s=self.AoP.shape
        Q = np.zeros([s[0], s[1]])
        U = np.zeros([s[0], s[1]])
        decfuse_represent = np.zeros([s[0], s[1]])
        for i in range(s[0]):
            for j in range(s[1]):
                Q[i, j] = (np.cos(2 * self.AoP[i, j]) + 1) / 2
                U[i, j] = (np.sin(2 * self.AoP[i, j]) + 1) / 2
                decfuse_represent[i, j] = self.__dec_fusion(U[i, j], Q[i, j], 3)
        return decfuse_represent

    def __dec_fusion(self,n,m,precision):
        mod_list=[]
        res=0
        for i in range(1,precision+1):
            mod_list.append(1/(10**i))
        nlist=[]
        mlist=[]
        for i in mod_list:
            nlist.append(np.floor(n/i))
            n=n%i
            mlist.append(np.floor(m/i))
            m=m%i
        exp=2*precision-1
        p=0
        while p<precision:
            res+=nlist[p]*10**exp
            exp-=1
            res+=mlist[p]*10**exp
            exp-=1
            p+=1
        return res

if __name__=="__main__":

    import numpy as np
    import os
    from CommonHelper.fileIO import file_reader
    from CommonHelper.imgIO import read
    import cv2
    from CommonHelper.imgOperation import Norm
    from CommonHelper import imgOperation
    from PolarHelper import PolarBasic


    class pretreat:
        def __init__(self):
            self.BPM = None
            self.img_src = None
            self.BPcom_area = 3
            self.pattern = [90, 45, 135, 0]
            self.PCM_W = None
            self.PCM_d = None

        def __channel_sepa(self, img):
            C = PolarBasic.ChannelSeparate()
            C.pattern = self.pattern
            img_separated = C.Separate(img)
            return img_separated

        def single_polarcal(self):
            eps = 1e-8
            img_separated = self.__channel_sepa(self.img_src)
            I = 0.5 * (img_separated[0] + img_separated[45] + img_separated[90] + img_separated[135])
            Q = img_separated[0] - img_separated[90]
            U = img_separated[45] - img_separated[135]
            Ip = np.sqrt(np.square(Q) + np.square(U))
            dolp = Ip / (I + eps)
            dolp[np.where(dolp > 1)] = 0
            aop = np.arctan2(U, Q)
            return {"I": I,
                    "Q": Q,
                    "U": U,
                    "DOLP": dolp,
                    "AOP": aop}, img_separated


    dirname = r'E:\35\data\SrcData\20210910'
    flist = file_reader().file_iterate_abs(dirname)
    for i in range(len(flist)):
        fname = flist[i]
        img = read().readraw(fname, 960, 540, type=np.uint8).astype(np.float)
        app = pretreat()
        app.img_src = img
        SPC, img_separated = app.single_polarcal()
        aop1=my_aop_map(SPC['AOP']).map_res
        cv2.imshow(fname,Norm(aop1))
    cv2.waitKey(0)
    cv2.destroyAllWindows()