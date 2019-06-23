import selectivesearch.selectivesearch as ss
import cv2
from PIL import Image
import numpy as np
from keras.models import load_model
from keras.applications import VGG16
import multiprocessing
from functools import partial 
import time

def read_im(name):
    im = Image.open("D:/Statistical Learning/project/image/ours/"+name)
    a,b = im.size
    if(a > 600):
        out = im.resize((800,int((800*b)/a)),Image.ANTIALIAS)
        
        out.save("D:/Statistical Learning/project/image/ours/"+name)
        im = out

    im = im.convert('RGB')
    img = cv2.imread("D:/Statistical Learning/project/image/ours/"+name)
    start_time = time.time()
    img_lbl, regions = ss.selective_search(img, scale=100, sigma=0.8, min_size=20)
    end_time = time.time()
    print('Time for SS: %ssecs'%(end_time - start_time))
    return([im,regions])

def model_predict(im_part, conv_base, dense):
    input_frame = np.array(im_part)/255.0
    input_frame = input_frame.reshape((1,50,50,3))

    con = conv_base.predict(input_frame)
    dense_input = con[0,0, :, :]
    pre_y = dense.predict(dense_input)

    if(pre_y < 0.5):
        return(1)
    else:
        return(0)


    


def im_filter(regions, im, conv_base, dense):
    li = []
    print(len(regions))
    start_time = time.time()
    for r in regions:

        rect = r['rect']
        x,y,h,w = rect
        if(h/(w+0.001) < 0.4 or w/(h+0.001) < 0.4):
            continue
        im_part = im.crop((x,y,x+h,y+w))
        im_part = im_part.resize((50,50))
        a = model_predict(im_part, conv_base, dense)
        if(a == 1):
            li.append(rect)
        else:
            continue
    print(len(li))
    end_time = time.time()
    # print('Time for step1: %ssecs'%(end_time - start_time))
    # start_time = time.time()

    # li = list(set(li))

    # true_li = li
    # final_li = []
    # for i in true_li:
    #     x,y,w,h = i
    #     tmp2 = 1
    #     for j in true_li:
    #         xj,yj,wj,hj = j   #四个角都要判断！
    #         if((x >= xj and x <= xj + wj and y >= yj and y <= yj + hj) or (x + w >= xj and x + w <= xj + wj and y >= yj and y <= yj + hj)):
    #             if(w*h < wj*hj):
    #                 tmp2 = 0
    #                 break
    #             else:
    #                 pass
    #         else:
    #             pass
    #     if(tmp2):
    #         final_li.append(i)

    # end_time = time.time()
    # print('Time for step2: %ssecs'%(end_time - start_time))

    return(li)

def ss_draw(name, regions):
    img = cv2.imread("D:/Statistical Learning/project/image/ours/"+name)
    for r in regions:
        x,y,h,w = r['rect']
        cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0), 2)

    cv2.imwrite('D:/Statistical Learning/project/output/ss/'+name, img)

def filter_draw(name, li):
    img = cv2.imread("D:/Statistical Learning/project/image/ours/"+name)
    for r in li:
        x,y,h,w = r
        cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0), 2)

    cv2.imwrite('D:/Statistical Learning/project/output/filter/'+name, img)



if __name__ == "__main__":

    VGG_conv_base = VGG16(weights='imagenet',
                        include_top=False,
                        input_shape=(50, 50, 3))
    VGG_dense = load_model("D:/Statistical Learning/project/CNN/VGG16.h5")

    name = 'board_243.jpg'  #243 272 278 160 202 170 283  scale = 300
    im,regions = read_im(name)
    li = im_filter(regions, im, VGG_conv_base, VGG_dense)
    ss_draw(name, regions)
    filter_draw(name, li)