import cv2

def visual(frame,frame_num,bbox:list,winname='BBox-visualization'):
    '''
    :param frame:
    :param bbox:[x(左上),y(左上),x(右下),y(右下)]
    :param winname:
    :return:
    '''
    xlt=bbox[0]
    ylt=bbox[1]
    xrb=bbox[2]
    yrb=bbox[3]
    im_show = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.rectangle(im_show, (int(xlt), int(ylt)), (int(xrb), int(yrb)),
                  (0, 255, 0), 3)
    cv2.putText(im_show, str(frame_num), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow(winname, im_show)
    cv2.waitKey(1)