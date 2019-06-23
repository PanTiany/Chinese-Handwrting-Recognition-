from PIL import Image
import sys
import os
import multiprocessing
from functools import partial 

def tail_photo(Start_path, pic):
    path=Start_path+'/'+pic
    im=Image.open(path)
    im.sq = im.crop((25,35,115,115))
    out = im.sq.resize((50,50),Image.ANTIALIAS)
    new_path='D:/Statistical Learning/大作业/' + pic
    out.save(new_path)

def main():
    # Start_path = sys.path[0]
    Start_path = 'D:/Statistical Learning/大作业/Handwriting'
    photolist=os.listdir(Start_path)

    NUM_WORKERS = 4 
    pool = multiprocessing.Pool(processes=NUM_WORKERS)

    func = partial(tail_photo, Start_path)
    pool.map(func, photolist)
    pool.close()
    pool.join()


if __name__=="__main__": 
    main()

