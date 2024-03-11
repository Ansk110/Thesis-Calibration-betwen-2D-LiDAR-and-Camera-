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


def process_lidar_data(data):
    x = all_data[:, 1]
    y = all_data[:, 1]
    return x, y


def filter_lidar_data(data, max_range=1000, min_angle=156, max_angle=205):
    """Filter lidar data within specified range and distance."""
    filtered_data = [point for point in data if point[2] <= max_range and min_angle < point[1] < max_angle]
    return np.array(filtered_data)


if __name__ == "__main__":
    port = '/dev/ttyUSB0'
    all_data = get_lidar_data(port=port, max_scans=50)

    filtered_data = filter_lidar_data(all_data)
    x, y = process_lidar_data(filtered_data)
    plt.scatter(x, y)
    plt.show()


