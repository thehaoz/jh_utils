import numpy as np
import cv2 as cv
import torch
drawing = False # true if mouse is pressed
src_x, src_y = -1,-1
dst_x, dst_y = -1,-1

src_list = []
dst_list = []

# mouse callback function
def select_points_src(event,x,y,flags,param):
    global src_x, src_y, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        src_x, src_y = x,y
        cv.circle(src_copy,(x,y),5,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False

# mouse callback function
def select_points_dst(event,x,y,flags,param):
    global dst_x, dst_y, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        dst_x, dst_y = x,y
        cv.circle(dst_copy,(x,y),5,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False

def get_plan_view(src, dst):
    src_pts = np.array(src_list).reshape(-1,1,2)
    dst_pts = np.array(dst_list).reshape(-1,1,2)
    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
    print("H:")
    print(H)
    plan_view = cv.warpPerspective(src, H, (dst.shape[1], dst.shape[0]))
    return plan_view, H

def merge_views(src, dst):
    plan_view, _ = get_plan_view(src, dst)
    for i in range(0,dst.shape[0]):
        for j in range(0, dst.shape[1]):
            if(plan_view.item(i,j,0) == 0 and \
               plan_view.item(i,j,1) == 0 and \
               plan_view.item(i,j,2) == 0):
                plan_view.itemset((i,j,0),dst.item(i,j,0))
                plan_view.itemset((i,j,1),dst.item(i,j,1))
                plan_view.itemset((i,j,2),dst.item(i,j,2))
    return plan_view

src = cv.imread('C:\\Users\\User\\Desktop\\invigilo\\project\\CR117-penta\\data\\test_ppe\\0f257827-f5d0-45b2-9d91-24a3dc15bc32.jpg', -1)
src = cv.resize(src, (1080,720))
src_copy = src.copy()
cv.namedWindow('src')
cv.moveWindow("src", 80,80)
cv.setMouseCallback('src', select_points_src)

model = torch.hub.load('ultralytics/yolov5',
                       'custom',
                       "C:\\Users\\User\\Desktop\\invigilo\\experiments\\invigilo-megadata\\megadata_v5_1280l.pt",
                       device=0)
src_infer = cv.cvtColor(src, cv.COLOR_BGR2RGB)
out = model(src_infer)
data = out.pandas().xyxy[0]
people_list = []
for i in range(len(data)):
    xmin = int(data['xmin'][i])
    ymin = int(data['ymin'][i])
    xmax = int(data['xmax'][i])
    ymax = int(data['ymax'][i])
    cls = int(data['class'][i])
    if cls == 0:
        print(xmin,ymin,xmax,ymax)
        people_list.append([xmin,ymin,xmax,ymax])


dst = cv.imread('C:\\Users\\User\\Desktop\\invigilo\\project\\CR117-penta\\data\\site_map_cropped.png', -1)
dst_copy = dst.copy()
cv.namedWindow('dst')
cv.moveWindow("dst", 780,80)
cv.setMouseCallback('dst', select_points_dst)

while(1):
    cv.imshow('src',src_copy)
    cv.imshow('dst',dst_copy)
    k = cv.waitKey(1) & 0xFF
    if k == ord('s'):
        print('save points')
        cv.circle(src_copy,(src_x,src_y),5,(0,255,0),-1)
        cv.circle(dst_copy,(dst_x,dst_y),5,(0,255,0),-1)
        src_list.append([src_x,src_y])
        dst_list.append([dst_x,dst_y])
        print("src points:")
        print(src_list)
        print("dst points:")
        print(dst_list)
    elif k == ord('h'):
        print('create plan view')
        plan_view, H = get_plan_view(src, dst)
        people_list_prime = []
        for p in people_list:
            xmin,ymin,xmax,ymax = p
            p_coords = np.array([[(xmin+xmax)//2,(ymin+ymax)//2]], dtype=np.float32)
            pointsOut = cv.perspectiveTransform(np.array([p_coords]), H)
            print(pointsOut)

            # print(p_coords_prime)
            dst = cv.circle(dst,(int(pointsOut[0][0][0]),int(pointsOut[0][0][1])),5,(0,255,0),-1)
        
        cv.imshow("plan view", plan_view) 
        cv.imshow("map view", dst) 
    elif k == ord('m'):
        print('merge views')
        merge = merge_views(src,dst)      
        cv.imshow("merge", merge)        
    elif k == 27:
        break
cv.destroyAllWindows()

