import cv2
from ultralytics import YOLO

# Function to read coordinates from a file
def read_coordinates(filename):
    points = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                x, y = map(int, line.strip().split(','))
                points.append((x, y))
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return points

# Read the box coordinates from box-coordinates.txt
box_coordinates = read_coordinates('box-coordinates.txt')
# Read the ROI coordinates from roi-coordinates.txt
roi_coordinates = read_coordinates('roi-coordinates.txt')

# Check if we have valid points
if len(box_coordinates) != 4 or len(roi_coordinates) != 4:
    raise ValueError("Both box-coordinates.txt and roi-coordinates.txt must contain exactly 4 points each.")

# Define points for the box and ROI
points = box_coordinates
roi_points = roi_coordinates

# ROI coordinates (top-left and bottom-right)
tl_x, tl_y = roi_points[0]
br_x, br_y = roi_points[2]

# Define colors (Green, Red)
color_tuple = [(0, 255, 0), (0, 0, 255)]

# Load the YOLO model
model = YOLO('Trained Models/best.pt')

# Select video source (webcam or video file)
video_capture = cv2.VideoCapture(0)  # Use webcam
# video_capture = cv2.VideoCapture('videos-predict/maybe_5MN75Ql5.mp4')  # Use video file

while True:
    ret, image_frame = video_capture.read()
    
    if not ret:
        break 

    # Reset the condition to 0 (green) at the start of each frame
    condition = 0

    # Draw the box from box coordinates
    for i in range(len(points)):
        cv2.line(image_frame, points[i], points[(i+1) % len(points)], color_tuple[condition], 6)

    # Perform object detection
    results = model(image_frame, show=False, conf=0.5, save=False, verbose=False)
    for result in results:
        boxes = result.boxes.cpu().numpy()
        xyxy = boxes.xyxy
        classes = boxes.cls

        # Check if any detection is a person and within the ROI
        for index, class_value in enumerate(classes):
            if class_value == 3.0:  # Assuming class 3.0 is 'person'
                x1, y1, x2, y2 = xyxy[index]
                # Check if the detected person is within the defined ROI
                if tl_x < x1 < br_x and tl_y < y1 < br_y and tl_x < x2 < br_x and tl_y < y2 < br_y:
                    condition = 1  # Change color to red

    # Draw the updated box with the new condition (possibly red)
    for i in range(len(points)):
        cv2.line(image_frame, points[i], points[(i+1) % len(points)], color_tuple[condition], 6)

    # Display the frame
    cv2.imshow('Video with Box', image_frame)

    # Exit on 'ESC' key
    if cv2.waitKey(1) & 0xFF == 27:  # ASCII for ESC is 27
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
