import requests
from bs4 import  BeautifulSoup
import sys
from PIL import Image
import random
import multiprocessing 
from functools import partial 
import csv


def get_handwriting(charlist,id):


    for i in charlist:

        url = "http://www.diyiziti.com/Builder/"+str(id)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        data = {"FontInfoId": id,
                "FontSize": 75,
                "FontColor":"#FFFFFF",
                "ImageWidth": 120,
                "ImageHeight": 120,
                "ImageBgColor": "#000000",
                "Content": i,
                "ActionCategory": 1}
        request = requests.post(url, data=data, headers=headers)
        soup = BeautifulSoup(request.text,'lxml')
        img = soup.find('img')
        src = img.get('src')
        photo = requests.session()
        photo = photo.get(src)
        filename = str(id) + i
        with open(sys.path[0]+'/type/'+ filename +'.png','wb') as f :
            # print(2)
            f.write(photo.content)

def getid():
    charlist = []
    csv_file = csv.reader(open(sys.path[0]+'/' + 'words.csv','r'))
    for eachline in csv_file:
        try:
            charlist.append(chr(int(str(eachline[1]))))
        except:
            continue
    return(charlist)

def main():

    idlist = [90, 62, 104, 99, 103, 82, 105, 136, 341, 87, 167,321, 87,167,83,123]

    charlist = getid()

    NUM_WORKERS = 4 
    pool = multiprocessing.Pool(processes=NUM_WORKERS)
    func = partial(get_handwriting, charlist)
    pool.map(func, idlist)
    pool.close()
    pool.join()



if __name__=="__main__": 
    main()



    