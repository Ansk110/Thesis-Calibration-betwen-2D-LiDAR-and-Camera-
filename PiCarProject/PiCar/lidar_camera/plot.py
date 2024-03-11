import numpy as np
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar
from tqdm.auto import tqdm

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
    scale = 1.1
    offset = -1
    x = ((all_data[:, 1] - 156) * 864) / (205 - 156)
    x = scale * x + offset
    y = [300] * len(x)
    s = all_data[:, 2] / max(all_data[:, 2])    
    return x, y, s

def filter_lidar_data(data, max_range=100000, min_angle=156, max_angle=205):
    filtered_data = [point for point in data if point[2] <= max_range and min_angle < point[1] < max_angle]
    return np.array(filtered_data)

def plot_obstacle_region(x, y, s):
    plt.scatter(x, y, c=s, s=5, cmap="rainbow")
    
if __name__ == "__main__":
    port = '/dev/ttyUSB0'
    all_data = get_lidar_data(port=port, max_scans=50)
    filtered_data = filter_lidar_data(all_data)
    x, y, s = process_lidar_data(filtered_data)
    image_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/lidar_camera/Images/img_1.jpg'
    im = plt.imread(image_path)
    implot = plt.imshow(im)
    plot_obstacle_region(x, y, s)
    plt.show()
