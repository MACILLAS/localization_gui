import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QLineEdit,
    QSpinBox,
)
from PIL import Image
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
import io
import base64

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.launched = False
        self.windows = []

        lay = QVBoxLayout(self)
        self.setWindowTitle("CViSS Localization Demo - Main")

        host_label = QLabel("Enter Host:")
        self.host_textbox = QLineEdit()
        self.host_textbox.setText("http://127.0.0.1:5000/")

        num_win_label = QLabel("Enter Number of ROI Windows.")
        #self.num_win_textbox = QLineEdit()
        #self.num_win_textbox.setText("5")
        self.num_win_textbox = QSpinBox()
        self.num_win_textbox.setRange(1, 10)
        self.num_win_textbox.setValue(3)


        launch_button = QPushButton("LAUNCH", self)
        launch_button.clicked.connect(self.launch)

        reset_button = QPushButton("RESET", self)
        reset_button.clicked.connect(self.reset)

        lay.addWidget(host_label)
        lay.addWidget(self.host_textbox)
        lay.addWidget(num_win_label)
        lay.addWidget(self.num_win_textbox)
        lay.addWidget(launch_button)
        lay.addWidget(reset_button)

        self.show()

    def launch(self):
        ''' Launch Application '''
        if not self.launched:
            host = self.host_textbox.text()
            test_req = requests.get(host+"status")
            if test_req.status_code != 200:
                print("Host is Invalid.")
                return Exception
            num_win = self.num_win_textbox.value()
            for i in range(int(num_win)):
                window = Window(3, i+1, host)
                window.show()
                self.windows.append(window)
            self.launched = True

    def reset(self):
        if self.launched:
            for window in self.windows:
                window.close()
            self.launched = False

class FooWidget(QWidget):
    def __init__(self):
        super(FooWidget, self).__init__()
        lay = QHBoxLayout(self)
        r_label = QLabel("Previous Inspection")
        q_label = QLabel("Current Inspection")
        r_label.resize(200, 50)
        q_label.resize(200, 50)
        lay.addWidget(r_label)
        lay.addWidget(q_label)

class Window(QWidget):
    def __init__(self, max_labels, roi_idx, host):
        super().__init__()
        # URL paths
        #self.status_url = "http://127.0.0.1:5000/status"
        self.status_url = host+"status"
        #self.latest_url = "http://127.0.0.1:5000/get_latest"
        self.latest_url = host+"get_latest"
        #self.idx_new_url = "http://127.0.0.1:5000/idx_new"
        self.idx_new_url = host+"idx_new"

        # Set Env Variables
        self.max_labels = max_labels # Max images to show per screen
        self.roi_idx = str(roi_idx) # ROI index this window is for

        self.setWindowTitle("Region of Interest: "+self.roi_idx)
        self.empty_string = "Waiting for Image"

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignTop)

        # Add Titles
        lay.addWidget(FooWidget())

        # Store all the label elements
        self.labels = []

        # Add labels and append them to labels
        for _ in range(self.max_labels):
            dummy_label = QLabel()
            dummy_label.setText(self.empty_string)
            dummy_label.resize(400, 200)
            self.labels.append(dummy_label)
            lay.addWidget(dummy_label)

        reset_button = QPushButton("RESET", self)
        reset_button.clicked.connect(self.reset)
        lay.addWidget(reset_button)

        # set window size
        self.setGeometry(0, 0, 400, 650)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.need_refresh)
        self.timer.setInterval(1000)
        self.timer.start()

    def reset(self):
        for label in self.labels:
            label.clear()
            label.setText(self.empty_string)

    def get_num_occ_labels(self):
        """
        Check for default string in self.labels
        This indicates an empty label
        :return: number of empty labels
        """
        counter = self.max_labels
        for label in self.labels:
            if label.text() == self.empty_string:
                counter = counter-1
        return counter
    def pil2pixmap(self, im):
        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        # Bild in RGBA konvertieren, falls nicht bereits passiert
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        return pixmap
    def need_refresh(self):
        # Get the status flag (indicates if flask got new image from localization)
        x = requests.get(self.status_url)
        i = requests.get(self.idx_new_url)

        # If a new image exists then
        if x.text == "1" and i.text == self.roi_idx:
            print("New image index: " + i.text)
            img = requests.get(self.latest_url, params={'img_idx': i.text})
            img = base64.b64decode(img.content)
            img = Image.open(io.BytesIO(img))
            img = img.resize(size=(400, 200))

            # Convert Image to Pixmap
            qim = self.pil2pixmap(img)

            # Check length of self.labels
            num_labels = self.get_num_occ_labels()
            if num_labels < self.max_labels:
                # Set image to free label
                self.labels[num_labels].setPixmap(qim) # cuz index at 0...
                # Resize the label according to image size
                self.labels[num_labels].resize(400, 200)

                # show the widgets
                self.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    #window = Window(3)
    #window.show()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())