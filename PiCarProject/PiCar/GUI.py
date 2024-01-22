import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt 
from adafruit_rplidar import RPLidar
from math import cos, sin, pi, floor
from lidar import LidarScanner

class LidarGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.lidar_scanner = LidarScanner()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Lidar Measurements')
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel('Lidar Measurements', self)
        self.label.setAlignment(Qt.AlignCenter)  # Update this line to use Qt directly
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_measurements)
        self.timer.start(1000) 

    def update_measurements(self):
        self.lidar_scanner.run_lidar()  # Call run_lidar on the LidarScanner instance
        front_distance = self.lidar_scanner.front_distance
        back_distance = self.lidar_scanner.back_distance
        left_distance = self.lidar_scanner.left_distance
        right_distance = self.lidar_scanner.right_distance

        # Update label text with Lidar measurements
        text = f"Front: {front_distance} mm\nBack: {back_distance} mm\nLeft: {left_distance} mm\nRight: {right_distance} mm"
        self.label.setText(text)

        # Check for exit condition (you can integrate your exit logic here)
        if exit_program:
            self.close()
            # Add code to stop Lidar and disconnect here (if needed)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lidar_gui = LidarGUI()
    lidar_gui.show()
    sys.exit(app.exec_())
