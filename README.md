Using PyQt5 GUI to show imageAI object detection result

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

![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/8dec0f2c-026f-448e-a480-ef41a2d19a0a)

## TODO
1. show detections result as text
2. highlight the result
3. allow user to change the box and label color

## Question
I wonder SSD is available in ImageAI as well.
