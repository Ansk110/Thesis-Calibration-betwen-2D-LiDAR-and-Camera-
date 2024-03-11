import numpy as np
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar
from tqdm.auto import tqdm
import cv2

def get_lidar_data(port='/dev/ttyUSB0', max_scans=50):
    """Retrieve lidar data from the specified port."""
    lidar = RPLidar(None, port)
    all_data = []
    for i, scan in tqdm(enumerate(lidar.iter_scans()), desc="Scanning", total=max_scans):
        if i >= max_scans:
            break
        all_data.extend(scan)
    lidar.stop()
    return np.array(all_data)

def process_lidar_data(all_data):
    scale = 1.00
    offset = 0
    x = ((all_data[:, 1] - 156)*864)/(205-156)
    x = scale * x + offset
    y = [300]*len(x)
    s = all_data[:, 2] / 200
    return x, y, s

def filter_lidar_data(data, max_range=100000, min_angle=156, max_angle=205):
    filtered_data = [point for point in data if point[2] <= max_range and min_angle < point[1] < max_angle]
    return np.array(filtered_data)

def detect_aruco_markers(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the dictionary of ArUco markers
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

    # Initialize the ArUco detector parameters
    parameters = cv2.aruco.DetectorParameters_create()

    # Detect the markers in the image
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Draw the detected markers on the image
    image_with_markers = cv2.aruco.drawDetectedMarkers(image.copy(), corners, ids)

    # Return the image with detected markers
    return image_with_markers

if __name__ == "__main__":
    port = '/dev/ttyUSB0'
    all_data = get_lidar_data(port=port, max_scans=50)
    filtered_data = filter_lidar_data(all_data)
    x, y, s = process_lidar_data(filtered_data)
    image_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/lidar_camera/Images/img_1.jpg'
    
    # Detect ArUco markers and overlay on the image
    image_with_markers = detect_aruco_markers(image_path)

    # Display the image with detected markers
    im = plt.imread(image_path)
    implot = plt.imshow(im)

    # Plot points with s values below a certain threshold in red, and above the threshold in blue
    threshold = 3  # Adjust the threshold as needed
    plt.scatter(x[s < threshold], y[s < threshold], color='red')
    plt.scatter(x[s >= threshold], y[s >= threshold], color='blue')
    
    plt.show()
