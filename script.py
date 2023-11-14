import os.path

from imageai.Detection import ObjectDetection
import requests


MODEL_DICT = {
    'RetinaNet': {'filename': 'retinanet_resnet50_fpn_coco-eeacb38b.pth',
    'url': 'https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/retinanet_resnet50_fpn_coco-eeacb38b.pth/'},
    'YOLOv3': {'filename': 'yolov3.pt',
    'url': 'https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt'},
    'TinyYOLOv3': {'filename': 'tiny-yolov3.pt',
                   'url': 'https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/tiny-yolov3.pt'}
}


def is_exists(model):
    return os.path.exists(MODEL_DICT[model]['filename'])

def download_model(model):
    url = MODEL_DICT[model]['url']
    response = requests.get(url)
    filename = MODEL_DICT[model]['filename']
    with open(filename, 'wb') as file:
        file.write(response.content)

def get_model_path(model):
    return MODEL_DICT[model]['filename']

def get_result_image_by_doing_object_detection(model_name, model_path, src_filename, dst_filename):
    detector = ObjectDetection()
    if model_name == 'RetinaNet':
        detector.setModelTypeAsRetinaNet()
    elif model_name == 'YOLOv3':
        detector.setModelTypeAsYOLOv3()
    elif model_name == 'TinyYOLOv3':
        detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    detections = detector.detectObjectsFromImage(input_image=src_filename,
                                                 output_image_path=dst_filename)

    # for eachObject in detections:
    #     print(eachObject)
    #     print(eachObject["name"] , " : " , eachObject["percentage_probability"])

    return dst_filename


def train_custom_dataset(model_path, object_names_array, data_directory):
    from imageai.Detection.Custom import DetectionModelTrainer

    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory="hololens-yolo")
    trainer.setTrainConfig(object_names_array=["hololens"], batch_size=4, num_experiments=200,
                           train_from_pretrained_model="yolov3.pt")
    # In the above,when training for detecting multiple objects,
    # set object_names_array=["object1", "object2", "object3",..."objectz"]
    trainer.trainModel()

# model_name = "retinanet_resnet50_fpn_coco-eeacb38b.pth"
# model_path = os.path.join(os.getcwd(), model_name)
# src_filename = os.path.join(os.getcwd(), 'image.jpg')
# dst_filename = os.path.join(os.getcwd(), 'imagenew.jpg')
#
# get_result_image_by_doing_object_detection(model_path, src_filename, dst_filename)