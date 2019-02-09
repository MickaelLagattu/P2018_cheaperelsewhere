from detection import detection
import os
import time
import urllib.request
from PIL import Image

data_path="flaskr/static/images/"


def parse(file):
    if file[-4:]=='.jpg': return file[:-4]
    else: return file
files = []
for file in os.listdir(data_path):
    if '.jpg' in file: files.append(file)

def save_image(link, output=None):
    if output==None:
        urllib.request.urlretrieve(link, link)
    else:
        urllib.request.urlretrieve(link, output)


def local_detection():
    for image in files:
        if image not in os.listdir(data_path + "detection_output/raw/"):
            t1 = time.time()
            objects=detection(image).getObjects()
            print(objects)
            f=open(data_path + "detection_output/raw/"+parse(image),"w")
            f.write(str(objects))
            f.close()
            t2=time.time()
            print("Time spent: ", t2-t1,"\n")


def get_objects(image, path=data_path + "detection_output/raw/"):
    if parse(image) in os.listdir(data_path + "detection_output/raw/"):
        f=open(path+parse(image), "r")
        line=f.readline()
        f.close()
        return set([dico['name'] for dico in eval(line)])
    else:
        t1 = time.time()
        objects = detection(image).getObjects()
        print(objects)
        f = open(data_path + "detection_output/raw/" + parse(image), "w")
        f.write(str(objects))
        f.close()
        t2 = time.time()
        print("Time spent: ", t2 - t1, "\n")


def array(x):
    return 0


def jaccard(image1, image2):
    intersection=get_objects(image1) & get_objects(image2)
    union = get_objects(image1) | get_objects(image2)
    return len(intersection)/len(union)


def getSize(image):
    with Image.open(image) as img:
        width, height = img.size
    return (width, height)













