import cv2
import numpy as np

# 车辆过滤条件应根据参照物适配，此处仅为演示原理oool
min_w = 100
min_h = 100

# 检测线高度、误差
check_line = 550
dead_line = 400

# 红点范围偏移量、
offset = 50
cv2.namedWindow('video', cv2.WINDOW_AUTOSIZE)
cap = cv2.VideoCapture('./vehicle.mp4')
bs = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
car_count = 0
cars_in_zone = {}  # 用于存储车辆在检测区域内的状态

while 1:
    ok, frame = cap.read()
    if ok:
        # 转换绘图图
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 高斯去噪
        blur = cv2.GaussianBlur(frame, (3, 3), 3)
        # 去除背景
        mask = bs.apply(blur)
        # 腐蚀
        erode = cv2.erode(mask, kernel, iterations=1)
        # 膨胀
        dilate = cv2.dilate(erode, kernel, iterations=1)
        # 闭运算
        close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
        close = cv2.morphologyEx(close, cv2.MORPH_CLOSE, kernel)
        _, close = cv2.threshold(close, 127, 255, cv2.THRESH_BINARY)
        # 查找轮廓
        contours, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 绘制检测线
        cv2.line(frame, (0, check_line), (frame.shape[1], check_line), (255, 0, 0), 3)
        cv2.line(frame, (0, dead_line), (frame.shape[1], dead_line), (0, 0, 0), 3)
        # 根据cars_in_zone中的x_pos绘制框
        for x_pos in cars_in_zone.keys():
            cv2.rectangle(frame, (x_pos - offset, dead_line), (x_pos + offset, check_line), (0, 0, 255), 2)
        for x_pos in list(cars_in_zone.keys()):
            roi = close[dead_line:check_line, x_pos - offset:x_pos + offset]
            shadow_pixels = np.sum(roi <= 127)
            total_pixels = roi.shape[0] * roi.shape[1]
            if shadow_pixels / total_pixels > 0.95:  # 阴影像素占比超过60%
                del cars_in_zone[x_pos]
        # 过滤、绘制轮廓，车辆计数
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # 过滤
            if w < min_w or h < min_h:
                continue
            # 搜集有效车辆
            center_y = y + h // 2
            center_x = x + w // 2
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            # 绘制轮廓
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if dead_line < center_y < check_line:
                found = False
                for x_pos in cars_in_zone.keys():
                    if max(x_pos-offset, center_x-offset) <= min(x_pos+offset, center_x+offset):
                        found = True
                        break
                if not found:
                    cars_in_zone[center_x] = True
                    car_count += 1


        cv2.putText(frame, f'Cars: {car_count}', (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
        cv2.imshow('video', frame)
        key = cv2.waitKey(42)
        if key == 27:
            break
    else:
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
