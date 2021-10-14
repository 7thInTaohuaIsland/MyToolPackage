import cv2

def frameCapture(path,time_zone,save_path,time_interval=-1):
    '''
    :param path:
    :param time_zone: [[0,30],[50.60],[77,89]],单位s
    :param time_interval: 保存帧之间的时间间隔，ms
    :return:
    '''
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
    for i in range(zone_num):
        temp=time_zone[i]
        fstart=int(temp[0]*fps)
        fend=int(temp[1]*fps)
        frame_zone.append([fstart,fend])

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
            cv2.imwrite(save_path+"/frame_{0}.jpg".format(current_frame_num),frame)
        success, frame = videoCapture.read()  # 获取下一帧
        current_frame_num+=1
    videoCapture.release()

if __name__=="__main__":
    path=r"E:\35\实验\无人机\0929_0930\DJI_0017.MP4"
    time_zone=[[30,50],[90,100]]
    frameCapture(path,time_zone,r'E:\pycode\video_capture\res\test',time_interval=500)