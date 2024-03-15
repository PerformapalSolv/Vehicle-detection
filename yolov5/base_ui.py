import cv2
import sys
import torch

from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage
from qt_material import apply_stylesheet
from TheGUI import Ui_MainWindow


def convert2QImage(img):
    height, width, channel = img.shape
    return QImage(img, width, height, width*channel, QImage.Format_RGB888)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.model = torch.hub.load('./', "custom", path='yolov5s.pt', source='local')
        self.model.cuda()
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.video = None
        self.setupUi(self)
        self.bind_slots()

    def image_pred(self, file_path):
        results = self.model(file_path)
        img = results.render()[0]
        return convert2QImage(img)

    def video_pred(self):
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.input.setPixmap(QPixmap.fromImage(convert2QImage(frame)))
            results = self.model(frame)
            image = results.render()[0]
            self.output.setPixmap(QPixmap.fromImage(convert2QImage(image)))

    def open_image(self):
        file_path = QFileDialog.getOpenFileName(self, dir='../TheGUI/', filter='*.jpg;*.png;*.jpeg')
        if file_path[0]:
            file_path = file_path[0]
            self.timer.stop()
            qimage = self.image_pred(file_path)
            self.input.setPixmap(QPixmap(file_path))
            self.output.setPixmap(QPixmap.fromImage(qimage))

    def open_video(self):
        file_path = QFileDialog.getOpenFileName(self, dir='../TheGUI/', filter='*.mp4;')
        if file_path[0]:
            file_path = file_path[0]
            self.video = cv2.VideoCapture(file_path)
            self.timer.start()

    def bind_slots(self):
        self.det_image.clicked.connect(self.open_image)
        self.det_video.clicked.connect(self.open_video)
        self.timer.timeout.connect(self.video_pred)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Yolov5Detaction_v1.0")
    apply_stylesheet(app, theme='dark_red.xml')
    window.show()
    app.exec()
