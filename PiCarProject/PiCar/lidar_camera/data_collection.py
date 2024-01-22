import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from adafruit_rplidar import RPLidar
from math import floor

# Function to initialize the LiDAR sensor
def initialize_lidar(port='/dev/ttyUSB0'):
    lidar = RPLidar(None, port)
    return lidar

# Function to capture LiDAR scan
def capture_lidar_scan(lidar):
    scan_data = [0] * 360  # Placeholder for LiDAR scan data
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        return scan_data

# Function to initialize the camera
def initialize_camera():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 16
    return camera

# Function to capture camera image
def capture_camera_image(camera):
    raw_capture = PiRGBArray(camera, size=(640, 480))
    camera.capture(raw_capture, format="bgr")
    image = raw_capture.array
    return image

# Function to collect data samples
def collect_data(lidar, camera, num_samples=10):
    lidar_data = []
    camera_data = []

    for _ in range(num_samples):
        timestamp = time.time()

        lidar_timestamp = timestamp
        lidar_scan = capture_lidar_scan(lidar)
        lidar_data.append((lidar_scan, lidar_timestamp))

        camera_timestamp = timestamp
        image = capture_camera_image(camera)
        camera_data.append((image, camera_timestamp))

        # Synchronization and further processing can be added here

    return lidar_data, camera_data

# Function to close LiDAR and camera connections
def close_connections(lidar, camera):
    lidar.stop()
    lidar.disconnect()
    camera.close()

if __name__ == "__main__":
    lidar = initialize_lidar()
    camera = initialize_camera()

    lidar_data, camera_data = collect_data(lidar, camera)

    close_connections(lidar, camera)
