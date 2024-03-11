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
    x = (all_data[:, 1] * 864) / (205 - 156)
    y = [100]*len(x)
    s = all_data[:, 2]/1000
    return x, y, s


if __name__ == "__main__":
    port = '/dev/ttyUSB0'
    all_data = get_lidar_data(port=port, max_scans=50)
    x, y, s = process_lidar_data(all_data)
    plt.scatter(x, y, s)
    plt.show()



