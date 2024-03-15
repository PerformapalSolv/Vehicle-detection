# Yolov5-vehicle-detection

[TOC]

### 前言

To deal with 《Computer Vision》 coursework, I  utilize Yolov5 neural network instead of traditional methods based on computer graphics.Besides, I use Pyside6 and Gradio to  achieve graphical interface.  

这个项目是我的《计算机视觉》课程小作业。虽然目前(24/3/15)我还只能看懂并自搭Yolov3网络，但这并不影响我使用好Yolov5。

其中，最开始完成项目(v1.0)的思路都是按别人教程一步步照抄的 [所参考课程](https://www.youtube.com/watch?v=RshY4nejGA0&list=PL2ecZnqc6-L4mp6CktfgLDrw5TCYqL_6B)

> I'm only a user of knowledge, not a creator, right now.This is the biggest gap between experts and apprentices.

[Yolov5](https://github.com/ultralytics/yolov5)     [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/pdf/1506.02640.pdf)   [YOLOv3: An Incremental Improvement](https://arxiv.org/pdf/1804.02767.pdf)  

### 所作工作

- v1.0使用的暂时还是yolov5的预训练模型, 单纯将yolov5用起来了而已。

  **最开始我选择BITVehicle数据集对Yolov5模型进行训练，训练结果Yolov5-vehicle-detection/yolov5/runs/train/exp2**

  **配置文件为：Yolov5-vehicle-detection/yolov5/datadata/myTrain.yaml**
  
- 结果，发现在北理工车辆数据集上训练的模型，只能对北理工车辆数据集起作用(过拟合)———原因：BITVehicle数据集太过高清，一个镜头大多只有一两个车辆，且车辆都是正面的静距离视角。

  如:   在这个图片中，因车辆里摄像头远了些，被标注为Truck

  <img src="https://yitongtuchuang.oss-cn-beijing.aliyuncs.com/image/test.jpg" alt="test" style="zoom: 25%;" />

<font color='dd0000'>**对项目改进方面：**</font>

1. 换用新的、泛化性更强的数据集训练

   最近也找到了合适的数据集：

   > > 链接：https://pan.baidu.com/s/1ZozGHhCKqul6zwnB60_E4w?pwd=pwwk 
   > > 提取码：pwwk 

2. 增加新功能：车辆计数

完成这两点，就从v1升级到v2；之后打算尝试挑战yolov5网络架构，使其更适配车辆识别。

### 简单介绍：如何使用本项目(V1.0)

1.

```git
git clone <本项目>
```

2.

激活相关python环境，进入Yolo文件夹下：

<img src="https://yitongtuchuang.oss-cn-beijing.aliyuncs.com/image/image-20240315214141803.png" alt="image-20240315214141803" style="zoom:50%;" />

**初步UI界面如图：**

<img src="https://yitongtuchuang.oss-cn-beijing.aliyuncs.com/image/image-20240315214207644.png" alt="image-20240315214207644" style="zoom: 50%;" />

**演示效果：**

<img src="https://yitongtuchuang.oss-cn-beijing.aliyuncs.com/image/%E5%8A%A8%E7%94%BB.gif" alt="动画" style="zoom:50%;" />



3. 使用gradio网页端：python gradioDemo.py

<img src="https://yitongtuchuang.oss-cn-beijing.aliyuncs.com/image/image-20240315224810848.png" alt="image-20240315224810848" style="zoom:50%;" />

<img src="https://yitongtuchuang.oss-cn-beijing.aliyuncs.com/image/image-20240315225112886.png" alt="image-20240315225112886" style="zoom: 33%;" />

### 遇到的问题

1.raise NotImplementedError("cannot instantiate %r on your system" NotImplementedError: cannot instantiate 'PosixPath' on your system

我在Ubuntu服务器上训练的模型，在windows下加载时，报这样的错误。最后搜索yolov5 issues解决

[方案](https://github.com/ultralytics/yolov5/issues/10240)
