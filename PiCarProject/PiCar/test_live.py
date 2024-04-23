import cv2
import numpy as np
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar
from picamera import PiCamera
from picamera.array import PiRGBArray

from src.camera import undistort_image
from src.lidar import filter_lidar_data, process_lidar_data


IMG_W, IMG_H = (864, 544)
PARAMS = {
    "lidar_extrinsic": "data/parameters/lidar_extrinsic_params.npz",
    # "camera_extrinsic": "data/parameters/camera_extrinsic_params.npz",
    "camera_intrinsic": "data/parameters/camera_intrinsic_params.npz",
}


def load_parameters():
    return {
        name: np.load(path2param)
        for name, path2param in PARAMS.items()
    }


def plot_obstacle_region(x, y, s):
    plt.scatter(x, y, c=s, s=5, cmap="rainbow")
    

def init_camera():
    camera = PiCamera()
    camera.resolution = (IMG_W, IMG_H)
    camera.framerate = 32
    return camera


def get_continuous_images(camera):
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):    
        image = frame.array
        yield image
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

        rawCapture.truncate(0)


def get_lidar_data(lidar):
    for scan in lidar.iter_scans():
        yield np.array(scan)


def main(
    lidar_port='/dev/ttyUSB0',
    lidar_max_range=10000,
    lidar_min_angle=158,
    lidar_max_angle=205,
):
    camera = init_camera()
    lidar = RPLidar(None, lidar_port)
    
    try:
        # Load and read parameters
        params = load_parameters()
        cam_matrix = params["camera_intrinsic"]["camera_matrix"]
        cam_dist_coeffs = params["camera_intrinsic"]["dist_coeffs"]
        lidar_ext_matrix = params["lidar_extrinsic"]["extrinsic_matrix"]
        lidar_scale_matrix = params["lidar_extrinsic"]["scale_matrix"]
        lidar_trans_vector = params["lidar_extrinsic"]["translation_vector"]

        cv2.namedWindow("Frame")
        lidar_gen = get_lidar_data(lidar)
        image_gen = get_continuous_images(camera)
        for image, lidar_data in zip(image_gen, lidar_gen):
            # Undistort image
            undistorted_img = undistort_image(image, cam_matrix, cam_dist_coeffs)

            # Filter and process lidar data
            filtered_lidar_data = filter_lidar_data(lidar_data, lidar_max_range, lidar_min_angle, lidar_max_angle)
            if len(filtered_lidar_data) == 0:
                continue
            
            lidar_pixels = process_lidar_data(filtered_lidar_data, lidar_ext_matrix, cam_matrix, cam_dist_coeffs, lidar_scale_matrix, lidar_trans_vector)
            norm_distances = filtered_lidar_data[:, 2]/1000

            # Add lidar points to the image
            for point, dist in zip(lidar_pixels, norm_distances):
                # Set color based on distance normalized to [0-1] range
                color = (0, int((1 - dist) * 255), int(dist * 255))
                undistorted_img = cv2.circle(undistorted_img, point, radius=5, color=color, thickness=-1)

            cv2.imshow("Frame", undistorted_img)
    
    finally:
        lidar.stop()
        camera.close()
        cv2.destroyAllWindows()

    
if __name__ == "__main__":
    main()

