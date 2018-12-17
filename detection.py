from imageai.Detection import ObjectDetection
import os
import time
import threading
import _thread
os.chdir("/home/insight/PycharmProjects/P2018_cheaperelsewhere/imagesComparison")
t1=time.time()
execution_path = os.getcwd()
path=""

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
def detect(image):
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path ,path+image), output_image_path=os.path.join(execution_path , path+"new"+image))

    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
t_start=time.time()

for image in ["C12G1713.jpg"]:
    detect(image)
t2=time.time()
print("")
print("Time spent : ",t2-t1)
print("t_start : ", t_start)

