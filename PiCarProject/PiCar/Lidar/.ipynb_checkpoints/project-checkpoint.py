import cv2
from cv2 import aruco as Aruco  # Ensure `aruco` is installed
import numpy as np

# Placeholder camera intrinsic parameters (replace with yours)
cam_matrix = np.array([[500, 0, 256],
                      [0, 500, 192],
                      [0, 0, 1]])
dist_coeffs = np.array([0.2, -0.1, 0.05, 0, 0.1])

# Placeholder LiDAR data (replace with yours)
# Generate 10 random points within 5m radius
distances = np.random.rand(10) * 5
angles = np.random.rand(10) * 2 * np.pi

# Replace with your image path
image_path = "/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg"

# Load the image
frame = cv2.imread(image_path)

# Check if image loaded successfully
if frame is None:
    print("Error: Image not found or could not be loaded.")
    exit()

# Simulate Aruco marker detection (replace with yours)
# Assuming a single marker with ID 0
corners = np.array([[[150, 100], [350, 100], [350, 250], [150, 250]]])
ids = [0]

# Simulate marker pose (replace with yours)
# Random rotation and translation within specific ranges
rvec = np.random.rand(3, 1) * 0.5  # Rotation vector
tvec = np.random.rand(3, 1) * 0.2  # Translation vector

# Process LiDAR data
points = []
for i in range(len(distances)):
    x = distances[i] * np.cos(angles[i])
    y = distances[i] * np.sin(angles[i])
    points.append([x, y, 0])  # Assuming 2D lidar, set z to 0

# Transform LiDAR points based on marker pose (replace with your logic)
# Assuming no transformation needed in this demo
transformed_points = points

# Project transformed points to image plane
projected_points = []
for point in transformed_points:
    projected_point = np.dot(cam_matrix, point)
    projected_points.append(projected_point)

# Draw projected points on the image
for point in projected_points:
    if point[2] != 0:  # Check for zero division
        point = point[:2] / point[2]  # Normalize by z-coordinate
    else:
        continue  # Skip drawing if z-coordinate is zero

    if np.isfinite(point).all():  # Check for infinite values
        # Adjust circle parameters for better visualization
        circle_color = (0, 255, 0)  # Green color
        circle_radius = int(max(0, min(50, (5 - distances[i]) * 10)))  # Larger for closer points
        frame = cv2.circle(frame, (int(point[0]), int(point[1])), circle_radius, circle_color, 2)
    else:
        continue  # Skip drawing if point has infinite values



# Display the image with overlaid LiDAR data
cv2.imshow('Image with LiDAR Projection', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
