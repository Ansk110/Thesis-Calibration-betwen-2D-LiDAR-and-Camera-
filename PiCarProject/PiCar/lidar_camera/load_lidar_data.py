import os
import numpy as np

def load_lidar_data(file_path):
    return np.load(file_path)

def main():
    lidar_data_dir = "/home/pi/Desktop/Thesis/PiCarProject/PiCar/lidar_camera/Lidar_data"
    for file_name in os.listdir(lidar_data_dir):
        if file_name.endswith(".npy"):
            file_path = os.path.join(lidar_data_dir, file_name)
            lidar_data = load_lidar_data(file_path)
            print(f"Loaded Lidar data from {file_path}:")
            print(lidar_data)

if __name__ == "__main__":
    main()
