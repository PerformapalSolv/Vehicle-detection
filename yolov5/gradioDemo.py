import torch
import gradio as gr

model = torch.hub.load('./', "custom", path='yolov5s.pt', source='local')

title = 'Yolov5计算机视觉演示项目(基于Gradio框架搭建)'
desc = '上传一张图片，由Yolov5网络对其进行目标检测'
base_conf, base_iou = 0.25, 0.45

def det_image(img, conf, iou):
    model.conf = conf
    model.iou = iou
    return model(img).render()[0], type(img)


gr.Interface(inputs=["image", gr.Slider(minimum=0, maximum=1, value=base_conf), gr.Slider(minimum=0, maximum=1, value=base_iou)],
             outputs=["image", "text"],
             fn=det_image,
             title=title,
             description=desc,
             examples=[['../ForVal/example01.jpg', base_conf, base_iou], ['../ForVal/example02.jpg', 0.4, 0.5], ['../ForVal/example03.jpg', 0.8, 0.6]]).launch()
