## 本文当主要用于介绍简单的html网页如何通过公共校园网访问

## 1、代码生成需要展示图片的网页
运行命令生成网页文件
~~~base
python Label_Studio_COCO_YOLO_BUU/generate_html.py
~~~

## 2、python运行网页部署到服务器指定端口

~~~base
python3 -m http.server 8080
~~~

## 3、一些命令

### 3.1.查询8080端口服务
~~~base
sudo netstat -tuln | grep 8082
~~~

### 3.2.打开8080端口

~~~base
sudo ufw status # 查看状态
sudo ufw allow 8080 # 打开8080端口
sudo ufw reload # 让新的规则生效
~~~