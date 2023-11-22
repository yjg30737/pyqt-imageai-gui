import sys
import os.path

from imageai.Detection import ObjectDetection, VideoObjectDetection
import requests


def open_directory(path):
    if sys.platform.startswith('darwin'):  # macOS
        os.system('open "{}"'.format(path))
    elif sys.platform.startswith('win'):  # Windows
        os.system('start "" "{}"'.format(path))
    elif sys.platform.startswith('linux'):  # Linux
        os.system('xdg-open "{}"'.format(path))
    else:
        print("Unsupported operating system.")


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

def get_result_video_by_doing_object_detection(model_name, model_path, src_filename, dst_filename):
    detector = VideoObjectDetection()
    if model_name == 'RetinaNet':
        detector.setModelTypeAsRetinaNet()
    elif model_name == 'YOLOv3':
        detector.setModelTypeAsYOLOv3()
    elif model_name == 'TinyYOLOv3':
        detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    detections = detector.detectObjectsFromVideo(input_file_path=src_filename,
                                                 output_file_path=dst_filename)

    # for eachObject in detections:
    #     print(eachObject)
    #     print(eachObject["name"] , " : " , eachObject["percentage_probability"])

    return dst_filename

#
#
# def train_custom_dataset(model_name, model_path, object_names_array, data_directory):
#     from imageai.Detection.Custom import DetectionModelTrainer
#
#     trainer = DetectionModelTrainer()
#     trainer.setModelTypeAsYOLOv3()
#     trainer.setDataDirectory(data_directory=data_directory)
#     trainer.setTrainConfig(object_names_array=object_names_array, batch_size=4, num_experiments=100,
#                            train_from_pretrained_model="yolov3.pt")
#     # In the above,when training for detecting multiple objects,
#     # set object_names_array=["object1", "object2", "object3",..."objectz"]
#     trainer.trainModel()
#
# # model_name = "retinanet_resnet50_fpn_coco-eeacb38b.pth"
# # model_path = os.path.join(os.getcwd(), model_name)
# # src_filename = os.path.join(os.getcwd(), 'image.jpg')
# # dst_filename = os.path.join(os.getcwd(), 'imagenew.jpg')
# #
#
# import os
# from PIL import Image
#
# import os
# from PIL import Image
#
#
# # def convert_png_to_jpg(source_folder, dest_folder=None):
# #     # If destination folder is not specified, use the source folder
# #     if dest_folder is None:
# #         dest_folder = source_folder
# #
# #     # Ensure destination folder exists
# #     os.makedirs(dest_folder, exist_ok=True)
# #
# #     # Iterate over all files in the source folder
# #     for filename in os.listdir(source_folder):
# #         if filename.endswith(".png"):
# #             # Construct the full file path
# #             file_path = os.path.join(source_folder, filename)
# #
# #             # Open the image
# #             with Image.open(file_path) as img:
# #                 # Convert the image to RGB mode in case it's in RGBA
# #                 rgb_img = img.convert('RGB')
# #
# #                 # Construct the destination file path
# #                 dest_file_path = os.path.join(dest_folder, filename[:-4] + '.jpg')
# #
# #                 # Save the image in JPG format
# #                 rgb_img.save(dest_file_path, "JPEG")
# #                 os.remove(file_path)
# #
# #     print("Conversion completed.")
# #
# #
# # # Example usage
# # source_folder = 'dataset/train/images'
# # dest_folder = 'dataset/train/images'  # Optional: specify a different folder for the converted images
# # convert_png_to_jpg(source_folder, dest_folder)
#
# # train_custom_dataset('YOLOv3', 'yolov3.pt', ['hololens'], 'hololens-yolo')