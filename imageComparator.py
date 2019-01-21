from skimage.measure import compare_ssim
import numpy as np
import cv2
from imageai.Detection import ObjectDetection
import os


data_path="/home/insight/PycharmProjects/cheapserGit/images"
os.chdir(data_path)


class histogram:
    def __init__(self,image1,image2):
        self.image1=image1
        self.image2=image2

    def correlation(self):
        image1, image2= self.image1, self.image2

        filenames = [image1, image2]
        index = {}
        images = {}
        reference = filenames[0]
        for filename in filenames:
            image = cv2.imread(filename)
            images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist)
            index[filename] = hist

        OPENCV_METHODS = [("Correlation", cv2.HISTCMP_CORREL)]

        for e in OPENCV_METHODS:
            methodName, method = e[0], e[1]
            results = {}
            reverse = False
            if methodName in ("Correlation", "Intersection"):
                reverse = True
            for (k, hist) in index.items():
                d = cv2.compareHist(index[reference], hist, method)
                results[k] = d

            results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)
            return results[1][0]

"Structural Similarity Index Measure"
class SSIM:
    def __init__(self,image1,image2):
        self.image1, self.image2 = cv2.imread(image1), cv2.imread(image2)

        self.image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        self.image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

    def mse(self):
        image1, image2= self.image1, self.image2
        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image1.shape[1])
        return err

    def compare_images(self):
        image1, image2= self.image1, self.image2
        m = self.mse()
        s = compare_ssim(image1, image2)
        return (s,m)

class detection:
    def __init__(self, image):
        self.image=image
        self.execution_path = os.getcwd()
        self.path = ""
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(self.execution_path, "resnet50_coco_best_v2.0.1.h5"))
        self.detector.loadModel()

    def getObjects(self):
        print(self.path)
        objects = self.detector.detectObjectsFromImage(input_image=os.path.join(self.execution_path, self.path + self.image),
                                                     output_image_path=os.path.join(self.execution_path,
                                                                                    self.path+"detection_output/" + "new" + self.image[:-4]))
        # for eachObject in objects:
        #     print(eachObject["name"], " : ", eachObject["percentage_probability"])

        return objects

"test"
if  __name__ == "__main__":

    "test SSIM"
    print("\nTest SSIM")
    image1 = "with_logo.jpg"
    image2 = "without_logo.jpg"
    print("(SSIM, MSE) : ", SSIM(image1, image2).compare_images())


    # print(SSIM(image1, image2))
    if SSIM(image1, image2).compare_images()[0] > 0.9:
        print("Exactly the same images, possibly with a logo superposed : ", image1, "and", image2)

    print("")

    "Histogram test"
    print("\nTest Histogramme")
    files = []
    for e in os.listdir():
        if '.jpg' in e: files.append(e)
    near_histo=dict()
    for i in range(len(files)):
        near_histo[files[i]]=set()
        others=[e for e in files if e!=files[i]]
        for x in others:
            if histogram(files[i],x).correlation()>=0.8:
                near_histo[files[i]].add(x)
    print("Images with similar histograms : ",near_histo)

    # print("")
    # image="century.jpg"
    # print(detection(image).getObjects())



