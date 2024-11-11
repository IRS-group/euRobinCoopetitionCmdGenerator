import cv2
import os
from cv2 import aruco

# Specify the path where you want to save the images
save_path = "./arucoMarkers/"

# Invert colors to make background white and marker black
invertColors = False

# Create the directory if it doesn't exist
os.makedirs(save_path, exist_ok=True)

# Choose dictionary and IDs
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
marker_size = 700  # Pixel size for each marker

# Generate and save 5 markers
for marker_id in range(5):  # IDs 0 to 4
    marker_image = aruco.drawMarker(aruco_dict, marker_id, marker_size)
    if invertColors:
        marker_image = cv2.bitwise_not(marker_image)
    filename = os.path.join(save_path, f"aruco_marker_{marker_id}.png")
    cv2.imwrite(filename, marker_image)
    print(f"Saved: {filename}")
