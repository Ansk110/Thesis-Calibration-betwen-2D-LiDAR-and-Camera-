import cv2


def calculate_image_size(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    height, width, _ = image.shape
    return width, height


image_path = "/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_20.jpg"
image_width, image_height = calculate_image_size(image_path)
print(f"Image size: {image_width} x {image_height}")
