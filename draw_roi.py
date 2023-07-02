"""
ROI drawing tool for OpenCV image.

DESCRIPTION
    This script is used to draw a ROI on an image. The ROI output will be printed out in the terminal for 
    further reference.

USAGE
    1. Change the img_file variable to the path of the image.
    2. Run the script.
    3. Click on the image to draw the ROI.
    4. Press 'd' to draw the ROI when you are done.
    5. Press 'q' to quit the program.
    6. Press 'x' to reset the ROI

NOTES
    - The ROI will be printed out in the terminal in the following format:
        [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    - To draw ROI for resized image, change the width and height variable to the desired size and
        uncomment the line that resizes the image.

"""



import cv2
import numpy as np
import yaml
import os
img_file = "<im path here>"

width, height = 640, 480
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        points.append([int(x), int(y)])
        cv2.circle(img,(x,y),5,(0,0,255),-1)
    
if __name__ == "__main__":

    drawing = False # true if mouse is pressed
    ix,iy = -1,-1
    original_mask = -1
    filled_mask = -1
    done = False
    points = []

    img = cv2.imread(img_file)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)


    # img = cv2.resize(img, (width, height))
    mask_display = np.zeros_like(img, dtype=np.uint8)
    mask_ = np.zeros(shape=img.shape[:2], dtype=np.uint8)
    temp_img = img.copy()
    img_t = img.copy()
    while(1):
        cv2.imshow('image',img)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('d'):
            poly_pts = np.array(points, np.int32)
            poly_pts_draw = poly_pts.reshape((-1,1,2))
            print(poly_pts.reshape((-1,2)).tolist())
            
            cv2.polylines(img_t,[poly_pts_draw],True,(0,255,255))
            cv2.fillPoly(mask_display, pts = [poly_pts_draw], color =(0,255,0))
            cv2.fillPoly(mask_, pts = [poly_pts_draw], color =1)

            img_t = cv2.addWeighted(img_t, 0.7, mask_display, 0.3, 0.0)
            cv2.imshow('image3',img_t)
            
        elif k == ord('x'): #resets the image (removes circles and rectangles)
            img = np.copy(temp_img)
            img_t = np.copy(temp_img)
            mask_display = np.zeros(shape=img.shape, dtype=np.uint8)
            mask_ = np.zeros(shape=img.shape[:2], dtype=np.uint8)
            points = []
            ix,iy = -1,-1
        elif k == 27:
            break
    cv2.destroyAllWindows()