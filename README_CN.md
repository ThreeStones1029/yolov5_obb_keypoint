<!--
 * @Description: 
 * @version: 
 * @Author: ThreeStones1029 2320218115@qq.com
 * @Date: 2024-11-27 12:35:08
 * @LastEditors: ShuaiLei
 * @LastEditTime: 2024-11-27 22:32:01
-->
# 原项目：yolov5用于旋转目标检测

[Origin Project：Rotation detection using the improved yolov5](https://github.com/hukaixuan19970627/yolov5_obb)

## 说明：改进后，本项目进行多任务的目标检测和关键点输出

![](docs/yolov5_obb_keypoint.png)

## 一：项目介绍


## 二、环境安装


## 三、训练

~~~base
python train_keypoints.py --weights "" --data data/buu_rotate.yaml --hyp data/hyps/obb/hyp_buu_keypoints.yaml --epochs 500 --batch-size 8 --img 1024 --device 0
~~~

## 四、评估

~~~base
python val_keypoints.py
~~~


## 五、预测

~~~base
python detect_keypoints.py
~~~