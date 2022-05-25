import cv2
import numpy as np

def Norm(img:np.ndarray):
    res=cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return res

class interpolation:
    def __init__(self):
        self.inter_method=cv2.INTER_CUBIC

    def inter(self,src,dsize=(0,0),fx=2,fy=2):
        if dsize!=(0,0):
            dsize=(dsize[1],dsize[0])
        img_dst=cv2.resize(src, dsize=dsize, fx=fx, fy=fy, interpolation=self.inter_method)
        return img_dst

class MyImshow:
    def __init__(self,g_image_original:np.ndarray,g_window_name="window",initial_ratio=1,text_color=None,g_image_pixel_source=np.zeros([1,1])):
        self.g_image_original=g_image_original
        self.k=len(g_image_original.shape)
        self.g_window_wh=[initial_ratio*g_image_original.shape[1],
                          initial_ratio*g_image_original.shape[0]]
        self.initial_ratio=initial_ratio
        self.g_window_name=g_window_name
        self.g_zoom, self.g_step = 1, 0.1  # 图片缩放比例和缩放系数
        self.g_location_win = [0, 0]  # 相对于大图，窗口在图片中的位置
        self.location_win = [0, 0]  # 鼠标左键点击时，暂存g_location_win
        self.g_location_click, self.g_location_release = [0, 0], [0, 0]  # 相对于窗口，鼠标左键点击和释放的位置
        self.g_image_zoom = g_image_original.copy()  # 缩放后的图片
        self.g_image_show = g_image_original[self.g_location_win[1]:self.g_location_win[1] + self.g_window_wh[1],
                       self.g_location_win[0]:self.g_location_win[0] + self.g_window_wh[0]]  # 实际显示的图片
        self.g_image_show_in_window = self.g_image_show.copy()
        self.text_color=text_color
        self.g_image_pixel_source=g_image_pixel_source

    def show(self):
        cv2.namedWindow(self.g_window_name, cv2.WINDOW_NORMAL)
        # 设置窗口大小，只有当图片大于窗口时才能移动图片
        cv2.resizeWindow(self.g_window_name, self.g_window_wh[0], self.g_window_wh[1])
        cv2.moveWindow(self.g_window_name, 700, 100)  # 设置窗口在电脑屏幕中的位置
        # 鼠标事件的回调函数
        cv2.setMouseCallback(self.g_window_name, self.mouse)
        while True:
            if cv2.getWindowProperty(self.g_window_name, 0) == -1:  # 当窗口关闭时为-1，显示时为0
                break
            cv2.waitKey(1)
        cv2.destroyAllWindows()

    def count_zoom(self,flag, step, zoom):
        if flag > 0:  # 滚轮上移
            zoom += step
            if zoom > 1 + step * 40:  # 最多只能放大到5倍
                zoom = 1 + step * 40
        else:  # 滚轮下移
            zoom -= step
            if zoom < 5*step:  # 最多只能缩小到0.5倍
                zoom = 5*step
        zoom = round(zoom, 2)  # 取2位有效数字
        return zoom

    # 矫正窗口在图片中的位置
    # img_wh:图片的宽高, win_wh:窗口的宽高, win_xy:窗口在图片的位置
    def check_location(self,img_wh, win_wh, win_xy):
        for i in range(2):
            if win_xy[i] < 0:
                win_xy[i] = 0
            elif win_xy[i] + win_wh[i] > img_wh[i] and img_wh[i] > win_wh[i]:
                win_xy[i] = img_wh[i] - win_wh[i]
            elif win_xy[i] + win_wh[i] > img_wh[i] and img_wh[i] < win_wh[i]:
                win_xy[i] = 0

    def mouse(self,event, x, y, flags, param=0):

        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            self.g_location_click = [x, y]  # 左键点击时，鼠标相对于窗口的坐标
            self.location_win = [self.g_location_win[0], self.g_location_win[1]]  # 窗口相对于图片的坐标
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
            self.g_location_release = [x, y]  # 左键拖曳时，鼠标相对于窗口的坐标
            h1, w1 = self.g_image_zoom.shape[0:2]  # 缩放图片的宽高
            w2, h2 = self.g_window_wh  # 窗口的宽高
            if w1 < w2 and h1 < h2:  # 图片的宽高小于窗口宽高，无法移动
                show_wh = [w1, h1]
                self.g_location_win = [0, 0]
            elif w1 >= w2 and h1 < h2:  # 图片的宽度大于窗口的宽度，可左右移动
                show_wh = [w2, h1]
                self.g_location_win[0] = self.location_win[0] + self.g_location_click[0] - self.g_location_release[0]
            elif w1 < w2 and h1 >= h2:  # 图片的高度大于窗口的高度，可上下移动
                show_wh = [w1, h2]
                self. g_location_win[1] = self.location_win[1] + self.g_location_click[1] - self.g_location_release[1]
            else:  # 图片的宽高大于窗口宽高，可左右上下移动
                show_wh = [w2, h2]
                self.g_location_win[0] = self.location_win[0] + self.g_location_click[0] - self.g_location_release[0]
                self.g_location_win[1] = self.location_win[1] + self.g_location_click[1] - self.g_location_release[1]
            self.check_location([w1, h1], [w2, h2], self.g_location_win)  # 矫正窗口在图片中的位置
            self.g_image_show = self.g_image_zoom[self.g_location_win[1]:self.g_location_win[1] + show_wh[1],
                           self.g_location_win[0]:self.g_location_win[0] + show_wh[0]]  # 实际显示的图片
            self.g_image_show_in_window=self.g_image_show.copy()
        elif event == cv2.EVENT_MOUSEWHEEL:  # 滚轮
            z = self.g_zoom  # 缩放前的缩放倍数，用于计算缩放后窗口在图片中的位置
            self.g_zoom = self.count_zoom(flags, self.g_step, self.g_zoom)  # 计算缩放倍数
            w1, h1 = [int(self.g_image_original.shape[1] * self.g_zoom*self.initial_ratio),
                      int(self.g_image_original.shape[0] * self.g_zoom*self.initial_ratio)]  # 缩放图片的宽高
            w2, h2 = self.g_window_wh  # 窗口的宽高
            self.g_image_zoom = cv2.resize(self.g_image_original, (w1, h1), interpolation=cv2.INTER_CUBIC)  # 图片缩放
            if w1 < w2 and h1 < h2:  # 缩放后，图片宽高小于窗口宽高
                show_wh = [w1, h1]
                cv2.resizeWindow(self.g_window_name, w1, h1)
            elif w1 >= w2 and h1 < h2:  # 缩放后，图片高度小于窗口高度
                show_wh = [w2, h1]
                cv2.resizeWindow(self.g_window_name, w2, h1)
            elif w1 < w2 and h1 >= h2:  # 缩放后，图片宽度小于窗口宽度
                show_wh = [w1, h2]
                cv2.resizeWindow(self.g_window_name, w1, h2)
            else:  # 缩放后，图片宽高大于窗口宽高
                show_wh = [w2, h2]
                cv2.resizeWindow(self.g_window_name, w2, h2)
            self.g_location_win = [int((self.g_location_win[0] + x) * self.g_zoom / z - x),
                              int((self.g_location_win[1] + y) * self.g_zoom / z - y)]  # 缩放后，窗口在图片的位置
            self.check_location([w1, h1], [w2, h2], self.g_location_win)  # 矫正窗口在图片中的位置
            # print(g_location_win, show_wh)
            self.g_image_show = self.g_image_zoom[self.g_location_win[1]:self.g_location_win[1] + show_wh[1],
                           self.g_location_win[0]:self.g_location_win[0] + show_wh[0]]  # 实际的显示图片
            self.g_image_show_in_window = self.g_image_show.copy()
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.k==2:
                if self.g_image_pixel_source.shape[0]==1:
                    sum=0
                    count=0
                    for i in range(-2,2):
                        for j in range(-2,2):
                            sum+=self.g_image_pixel_source[y+i, x+i]
                            count+=1
                    mean=sum/count
                    # pixel = '{:.1f}'.format(self.g_image_show[y,x])
                    pixel = '{:.1f}'.format(mean)
                else:
                    pixel = '{:.1f}'.format(self.g_image_pixel_source[y, x])
                cv2.circle(self.g_image_show_in_window, (x, y), 1, (255, 255, 255), thickness=-1)
                cv2.putText(self.g_image_show_in_window, pixel, (x, y), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (255, 255, 255), thickness=1)
            elif self.k==3:
                pixel = "(B:{0},G:{1},R:{2})" .format(self.g_image_show[y,x,0],
                                                      self.g_image_show[y,x,1],
                                                      self.g_image_show[y,x,2])
                pixel_B=self.g_image_show[y,x,0]
                pixel_G=self.g_image_show[y,x,1]
                pixel_R=self.g_image_show[y,x,2]
                if pixel_B<=pixel_G and pixel_B<=pixel_R:
                    text_color0=(255,0,0)
                elif pixel_G<=pixel_B and pixel_G<=pixel_R:
                    text_color0=(0,255,0)
                elif pixel_R<=pixel_G and pixel_R<=pixel_B:
                    text_color0=(0,0,255)
                if self.text_color==None:
                    text_color=text_color0
                else:
                    text_color=self.text_color
                cv2.circle(self.g_image_show_in_window, (x, y), 1, text_color, thickness=-1)
                cv2.putText(self.g_image_show_in_window, pixel, (x, y), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (text_color), thickness=1)
        self.g_image_show_in_window = Norm(self.g_image_show_in_window)
        cv2.imshow(self.g_window_name, self.g_image_show_in_window)

if __name__=="__main__":
    img=cv2.imread("E:/test/trees/trees_002.jpg")
    MyImshow(img,initial_ratio=1).show()