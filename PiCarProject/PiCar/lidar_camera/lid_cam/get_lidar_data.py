import numpy as np

def get_lidar_data(lidar, interval=1):
    """Retrieve lidar data from the specified port."""
    iter_num = 0
    data = []
    for scan in lidar.iter_scans():
        data.extend(scan)
        iter_num += 1
        if (iter_num % interval) == 0:
            yield np.array(data)
            data = []
            iter_num = 0