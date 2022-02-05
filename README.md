# u2net_gimp_plugin
A plugin for GIMP that use u2net for segmentation

|input|result|
|---|---|
|![](imgs/Parrot.jpg)|![](imgs/ParrotSeg.png)|

## Installation
1. Clone repo into your GIMP plugin folder (We need GIMP 2.99.* or greater)

    ```bash
    # cd into GIMP folder
    git clone https://github.com/nicolalandro/u2net_gimp_plugin.git
    cd u2net_gimp_plugin
    ```
2. Install dependent packages

    ```bash
    cd u2net_gimp_plugin
    flatpak run --command=bash org.gimp.GIMP//beta
    python -m ensurepip
    python -m pip install --upgrade pip

    python -m pip install -r requirements.txt
    ```
3. Download pretrained models

    ```bash
    cd u2net_gimp_plugin
    wget https://github.com/nicolalandro/u2net_gimp_plugin/releases/download/0.1/u2net.onnx
    ```
## Usage
* open GIMP
...

## Dev
Test script:
```
pip install -r requirements
python3.8 inference.py
```