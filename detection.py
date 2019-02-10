import os
from imageai.Detection import ObjectDetection

class detection:
    def __init__(self, image):
        full_path = os.path.realpath(__file__)
        # print("full_path",full_path)
        full_path = str.replace(full_path, '\\', '/')
        # print("full_path", full_path)
        path, filename = os.path.split(full_path)
        self.image=image
        self.execution_path = path + "/" + "flaskr/static/images/"
        # print(self.execution_path)
        self.path = ""
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(self.execution_path + "resnet50_coco_best_v2.0.1.h5")
        with open(self.execution_path + "resnet50_coco_best_v2.0.1.h5") as f:
            pass
        self.detector.loadModel()

    def getObjects(self):
        # print(self.path)
        image_name = os.path.basename(self.image)
        objects = self.detector.detectObjectsFromImage(input_image=os.path.join(self.image),
                                                        output_image_path=os.path.join(self.execution_path,
                                                                                    self.path+"detection_output/" + "new" + image_name[:-4]))
        # for eachObject in objects:
        #     print(eachObject["name"], " : ", eachObject["percentage_probability"])

        return objects