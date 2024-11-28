<!--
 * @Description: 
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-11-27 12:35:08
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-11-28 20:59:25
-->
# Yolov5 for Oriented Object Detection 

[Origin Project：Rotation detection using the improved yolov5](https://github.com/hukaixuan19970627/yolov5_obb)

## Note: After improvement, this project carries out multi-task target detection and keypoint output.

![](docs/yolov5_obb_keypoint.png)

## 1、Project Introduction

In order to improve the accuracy of 2D3D registration, it is necessary to identify the vertebral rotation box and the center point.

## 2、Environment Install

Install according to the original project.

## 3、Dataset Preprocess

On the basis of the original data format, the coordinates of key points are added

~~~
x1    y1    x2     y2    x3    y3    x4    y4    keypoint_x   keypoint_y  classname  diffcult
752.0 186.0 1017.0 261.0 962.0 455.0 697.0 379.0 844.0 313.0 L1 0
672.0 345.0 952.0 445.0 877.0 655.0 597.0 555.0 747.0 486.0 L2 0
581.0 538.0 852.0 623.0 790.0 820.0 519.0 734.0 659.0 668.0 L3 0
506.0 764.0 781.0 800.0 757.0 983.0 482.0 947.0 597.0 864.0 L4 0
470.0 994.0 729.0 952.0 760.0 1146.0 501.0 1188.0 590.0 1075.0 L5 0
833.0 23.0 1084.0 108.0 1023.0 289.0 772.0 204.0 913.0 153.0 T12 0
~~~


## 4、Train

~~~base
python train_keypoints.py --weights "" --data data/buu_rotate.yaml --hyp data/hyps/obb/hyp_buu_keypoints.yaml --epochs 500 --batch-size 8 --img 1024 --device 0
~~~

## 5、Eval

~~~base
python val_keypoints.py --data data/buu_rotate.yaml --weights runs/train/exp/weights/best.pt --batch-size 8 -img 1024 --device 0
~~~

## 6、Detect

~~~base
python detect_keypoints.py --weights runs/train/exp/weights/best.pt --source dataset/BUU/test/images -img 1024 --device 0
~~~