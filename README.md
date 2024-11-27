<!--
 * @Description: 
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-11-27 12:35:08
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-11-27 22:31:09
-->
# Yolov5 for Oriented Object Detection 

[Origin Project：Rotation detection using the improved yolov5](https://github.com/hukaixuan19970627/yolov5_obb)

## Note: After improvement, this project carries out multi-task target detection and keypoint output.

![](docs/yolov5_obb_keypoint.png)

## 1、Project Introduction


## 2、Environment Install


## 3、Train

~~~base
python train_keypoints.py --weights "" --data data/buu_rotate.yaml --hyp data/hyps/obb/hyp_buu_keypoints.yaml --epochs 500 --batch-size 8 --img 1024 --device 0
~~~

## 4、Eval

~~~base
python val_keypoints.py
~~~

## 5、Detect

~~~base
python detect_keypoints.py
~~~