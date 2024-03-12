
def process_lidar_data(all_data):
    scale = 1.4
    offset = -190
    x = ((all_data[:, 1] - 156) * 864) / (205 - 156)
    x = scale * x + offset
    y = [250] * len(x)
    s = all_data[:, 2] / max(all_data[:, 2])    
    return x, y, s