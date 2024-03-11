import numpy as np
from adafruit_rplidar import RPLidar

# Define the region of interest where the ArUco marker lies (in degrees)
ARUCO_REGION_START = 158
ARUCO_REGION_END = 201

def collect_lidar_data():
    lidar_data = []
    # Establish connection to the RPLIDAR
    lidar = RPLidar(None, '/dev/ttyUSB0')  # Update the port based on your device configuration
    
    # Start scanning
    lidar.start_motor()
    lidar.connect()
    
    # Iterate through each scan
    for scan in lidar.iter_scans():
        # Filter out points outside the region of interest
        scan_data = [(np.radians(measurement[1]), measurement[2]) for measurement in scan 
                     if ARUCO_REGION_START <= measurement[1] <= ARUCO_REGION_END]
        lidar_data.extend(scan_data)
        
        # Break if enough data is collected
        if len(lidar_data) >= 1000:
            break
    
    # Stop scanning and close connection
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    
    return np.array(lidar_data)

# Example usage
if __name__ == "__main__":
    lidar_data = collect_lidar_data()
    print("Collected Lidar Data:")
    print(lidar_data)
