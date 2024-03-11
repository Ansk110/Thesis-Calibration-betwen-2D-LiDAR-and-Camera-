import numpy as np
import cv2
from adafruit_rplidar import RPLidar
import time

# Camera setup
camera = cv2.VideoCapture(0)  # Open the default camera (usually camera 0)
if not camera.isOpened():
    print("Error: Unable to open camera.")
    exit()

# LiDAR setup
PORT_NAME = '/dev/ttyUSB0'  # Change this to match your LiDAR port
lidar = RPLidar(None, PORT_NAME)

# Output file paths
image_filename = "camera_image.jpg"
lidar_filename = "lidar_data.npy"

# Function to capture synchronized data
def capture_data():
    # Capture image from camera
    ret, frame = camera.read()
    if not ret:
        print("Error: Unable to capture frame from camera.")
        return None, None
    
    # Collect LiDAR data
    lidar_data = []
    for scan in lidar.iter_scans():
        lidar_data.extend(scan)
        break  # Break after one scan
        
    return frame, lidar_data

try:
    while True:
        start_time = time.time()
        
        # Capture synchronized data
        frame, lidar_data = capture_data()
        if frame is None or lidar_data is None:
            break
        
        # Save captured data
        cv2.imwrite(image_filename, frame)
        np.save(lidar_filename, lidar_data)
        
        # Process the captured data (replace this with your processing logic)
        # For example, you can display the image and print the LiDAR data
        cv2.imshow("Camera Image", frame)
        print("LiDAR Data:", lidar_data)

        # Calculate time elapsed
        elapsed_time = time.time() - start_time
        print("Time Elapsed:", elapsed_time, "seconds")
        
        # Check for key press to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

finally:
    # Release resources
    camera.release()
    cv2.destroyAllWindows()
    lidar.stop()
    lidar.disconnect()
    print("Camera and LiDAR Disconnected.")

