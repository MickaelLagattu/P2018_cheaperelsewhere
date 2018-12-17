from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import cv2
import os


index = {}
images = {}

path="/home/insight/PycharmProjects/cheaper_elsewhere/images/test"
os.chdir(path)

def correlation(image1,image2):
    filenames=[image1,image2]
    reference = filenames[0]
    for filename in filenames:
        image = cv2.imread(filename)
        images[filename] = cv2.cvtColor(image, cvhttps://github.com2.COLOR_BGR2RGB)
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],[0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist)
        index[filename] = hist

    OPENCV_METHODS =[("Correlation", cv2.HISTCMP_CORREL)]

    for e in OPENCV_METHODS:
        methodName, method=e[0],e[1]
        results = {}
        reverse = False
        if methodName in ("Correlation", "Intersection"):
            reverse = True
        for (k, hist) in index.items():
            d = cv2.compareHist(index[reference], hist, method)
            results[k] = d

        results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)
        return results[1][0]

files=[]
for e in os.listdir():
    if '.jpg' in e: files.append(e)
for i in range(len(files)):
    others=[e for e in files if e!=files[i]]
    for x in others:
        if correlation(files[i],x)>=0.8: print("Match ! :",files[i],"et",x)

