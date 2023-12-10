import cv2
import cv2.aruco as aruco

# Initialize camera
camera = cv2.VideoCapture(0)  # Adjust the camera index if needed

# Load the predefined dictionary for ArUco markers
dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Create a detector parameters object
parameters = aruco.DetectorParameters_create()

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()

    # Process the frame
    if ret:
        # Convert the frame to grayscale (optional)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect markers
        corners, ids, _ = aruco.detectMarkers(gray, dictionary, parameters=parameters)

        # If markers are detected
        if ids is not None:
            for i in range(len(ids)):
                # Perform actions based on detected marker IDs
                marker_id = ids[i][0]

                # Example action mapping
                if marker_id == 0:
                    print("Stop sign detected")
                    # Perform actions corresponding to stop sign

                elif marker_id == 1:
                    print("Left turn sign detected")
                    # Perform actions corresponding to left turn sign

                # Add more elif conditions for other marker IDs and actions

            # Draw detected markers on the frame
            aruco.drawDetectedMarkers(frame, corners)

        # Display the processed frame
        cv2.imshow('ArUco Marker Detection', frame)

    # Exit on ESC key press
    if cv2.waitKey(1) == 27:
        break

# Release the camera and close windows
camera.release()
cv2.destroyAllWindows()
