Using ImageAI in PyQt!

Both image and video is available for object detection.

## Requirements
* PyQt5>=5.14
* imageai (for using object detection)
* requests (for downloading models from remote server)

## How to Install
1. git clone ~
2. pip install -r requirements.txt
3. python main.py

## How to Use
### Select the desired model
![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/e947be1b-56bc-4d11-9092-9225df7d7436)

### Downloading the model
![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/4b9783f1-5fe7-4af7-9f24-498d00867715)

Model file will be downloaded in the root folder of this repo

Note: If there is a model file already, this won't download the model. Remember, you should not change the model's name or parent directory if you don't want to download it again.

### Use the model

#### Object Detection from Image
![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/8dec0f2c-026f-448e-a480-ef41a2d19a0a)

### Object Detection from Video (This is more recent version of GUI)
![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/c1758495-64a5-4f2e-a406-c32ff7e57f6b)

Sample video: https://youtu.be/1QfF8uoGiOY

## TODO
1. show detections result as text
2. highlight the result
3. allow user to change the box and label color

## Question
I wonder SSD is available in ImageAI as well.

## See Also
<a href="https://github.com/yjg30737/pyqt-ultralytics-yolo-gui">pyqt-ultralytics-yolo-gui</a>: Using YOLOv8 of Ultralytics to not only doing object detection but also semantic segmentation

ImageAI is using YOLOv3, but YOLOv8 is much faster and more accurate, which is good choice.
