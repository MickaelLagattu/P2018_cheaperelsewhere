import os
from imageai.Detection import ObjectDetection

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