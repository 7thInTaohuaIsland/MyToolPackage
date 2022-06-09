import cv2
from CommonHelper.fileIO import file_reader
from CommonHelper.imgOperation import interpolation
from CommonHelper.fileIO import mkdir

def frameCapture(path,time_zone,save_path,time_interval=-1):
    '''
    :param path:
    :param time_zone: [[0,30],[50.60],[77,89]],单位s
    :param time_interval: 保存帧之间的时间间隔，ms
    :return:
    '''
    mkdir(save_path, rmtree=True)
    videoCapture = cv2.VideoCapture(path)
    # 获得码率及尺寸
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    # 读帧
    success, frame = videoCapture.read()
    current_frame_num=0
    #截取帧序号
    zone_num=len(time_zone)
    frame_zone=[]
    if zone_num!=0:
        for i in range(zone_num):
            temp=time_zone[i]
            fstart=int(temp[0]*fps)
            fend=int(temp[1]*fps)
            frame_zone.append([fstart,fend])
    else:
        frame_zone=[[0,fNUMS-1]]

    #计算帧间隔
    if time_interval*fps/1000<=1:
        frame_interval=1
    else:
        frame_interval=int(time_interval*fps/1000)

    while success:
        #不符合帧序号要求的continue
        if current_frame_num%frame_interval!=0:
            success, frame = videoCapture.read()  # 获取下一帧
            current_frame_num += 1
            continue
        #超过最大帧序数的break
        if current_frame_num>=frame_zone[zone_num-1][1]:
            break
        #判断是否保存
        save_flag = False
        for zone in frame_zone:
            if current_frame_num>=zone[0] and current_frame_num<zone[1]:
                save_flag=True
                break
        if save_flag:
            cv2.imwrite(save_path+"/{:0>5}.jpg".format(current_frame_num),frame)
        success, frame = videoCapture.read()  # 获取下一帧
        current_frame_num+=1
    videoCapture.release()

# def video_writer(src_path,dst_path=None,fps=20,size=(360,480),encode="mp4v"):
#     flist=file_reader().file_iterate_abs(src_path)
#     videowrite = cv2.VideoWriter(dst_path, cv2.VideoWriter_fourcc(*encode), fps, size)
#     """
#     参数1 即将保存的文件路径
#     参数2 VideoWriter_fourcc为视频编解码器
#         fourcc意为四字符代码（Four-Character Codes），顾名思义，该编码由四个字符组成,下面是VideoWriter_fourcc对象一些常用的参数,注意：字符顺序不能弄混
#         cv2.VideoWriter_fourcc('I', '4', '2', '0'),该参数是YUV编码类型，文件名后缀为.avi
#         cv2.VideoWriter_fourcc('P', 'I', 'M', 'I'),该参数是MPEG-1编码类型，文件名后缀为.avi
#         cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),该参数是MPEG-4编码类型，文件名后缀为.avi
#         cv2.VideoWriter_fourcc('T', 'H', 'E', 'O'),该参数是Ogg Vorbis,文件名后缀为.ogv
#         cv2.VideoWriter_fourcc('F', 'L', 'V', '1'),该参数是Flash视频，文件名后缀为.flv
#         cv2.VideoWriter_fourcc('m', 'p', '4', 'v')    文件名后缀为.mp4
#     参数3 为帧播放速率
#     参数4 (width,height)为视频帧大小
#     """
#     cv2.namedWindow("1")
#     for img_name in flist:
#         image = cv2.imread(img_name,0)
#         img=interpolation().inter(image,dsize=size)
#         cv2.imshow("1",img)
#         videowrite.write(img)
#         cv2.waitKey(1)
#     videowrite.release()
#     cv2.destroyAllWindows()

if __name__=="__main__":
#     path=r"E:\35\实验\无人机\0929_0930\DJI_0017.MP4"
#     time_zone=[[30,50],[90,100]]
#     frameCapture(path,time_zone,r'E:\pycode\video_capture\res\test',time_interval=500)

    # img_path=r"E:\35\dataset\20210929\video_6\IR"
    # save_path=r"E:\pycode\pysot-master\demo\video_3.mp4"
    img_path=r"E:/test/seq"
    save_path=r"E:/test/seq.mp4"
    # video_writer(img_path, save_path,fps=10)