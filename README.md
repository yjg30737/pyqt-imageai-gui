![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/36defea9-4f92-4513-be22-1a1c6e96621a)# pyqt-imageai-gui
Using PyQt5 GUI to show imageAI semantic segmentation result

## Requirements
* PyQt5>=5.14
* imageai (for using semantic segmentation)
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
![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/f88fbe78-e7bc-49cb-9bb2-394715c7dc88)

## TODO
1. modify the result widget (currently QSplitter) as below
![image](https://github.com/yjg30737/pyqt-imageai-gui/assets/55078043/16301b2b-9971-43b3-9aba-24bc1a91e9ab)

2. show detections result as text
3. highlight the result
4. blah blah..
