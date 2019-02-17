from skimage.measure import compare_ssim
import numpy as np
import cv2
from imageai.Detection import ObjectDetection
import os
import functions



full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
data_path = os.path.join(path, "flaskr/static/images/")



class histogram:
    """this class implements the mesure of correlation between two images histograms"""
    def __init__(self,image1,image2):
        self.image1=data_path + image1
        self.image2=data_path + image2

    def correlation(self):
        """ return a float between 0 and 1"""
        image1, image2= self.image1, self.image2

        filenames = [image1, image2]
        index = {}
        images = {}
        reference = filenames[0]
        for filename in filenames:
            # print("Filename", filename)
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
    """this class implements the mesure of the structural similarity index between two images"""
    def __init__(self,image1,image2):
        print('SSIM')
        print("image1 : ", image1)
        print("image2 : ", image2)
        self.image1, self.image2 = cv2.imread(data_path + image1), cv2.imread(data_path + image2)

        self.image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        self.image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

    def mse(self):
        """this method returns the mean square error"""
        image1, image2= self.image1, self.image2
        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image1.shape[1])
        return err

    def compare_images(self):
        """this method return a the couple (SSSIM, MSE)"""
        image1, image2= self.image1, self.image2
        m = self.mse()
        s = compare_ssim(image1, image2)
        return (s,m)





def global_score(image1, image2):
    # image1 = "static/images/"+image1
    # image2 = "static/images/"+image2
    """this function uses the methods above to calculate a global_score for a couple images.
    It returns 1 when we are sure that the two arguments refer to the same image.
    Otherwise, it returns an average score."""
    try:
        if functions.getSize(data_path+image1)==functions.getSize(data_path+image2):
            if SSIM(image1, image2).compare_images()[0]>0.8:
                return 1
        elif image1!=image2:
            if histogram(image1, image2).correlation()>0.95:
                return 1
            else:
                h=histogram(image1, image2).correlation()
                j=functions.jaccard(image1, image2)
                return (h + j) / 2
    except Exception as e:
        print(444)
        print(e)
        h = histogram(image1, image2).correlation()
        j = functions.jaccard(image1, image2)
        return (h + j) / 2

    return 0



"test"
# if  __name__ == "__main__":
#
#     "test SSIM"
#     print("\nTest SSIM")
#     image1 = "with_logo.jpg"
#     image2 = "without_logo.jpg"
#     print("(SSIM, MSE) : ", SSIM(image1, image2).compare_images())
#
#
#     # print(SSIM(image1, image2))
#     if SSIM(image1, image2).compare_images()[0] > 0.9:
#         print("Exactly the same images, possibly with a logo superposed : ", image1, "and", image2)
#
#     print("")
#
#     "Histogram test"
#     print("\nTest Histogramme")
#     files = []
#     for e in os.listdir(data_path):
#         if '.jpg' in e: files.append(e)
#     near_histo=dict()
#     for i in range(len(files)):
#         near_histo[files[i]]=set()
#         others=[e for e in files if e!=files[i]]
#         for x in others:
#             if histogram(files[i],x).correlation()>=0.8:
#                 near_histo[files[i]].add(x)
#     print("Images with similar histograms : ",near_histo)
#
#     # print("")
#     # image="century.jpg"
#     # print(detection(image).getObjects())
