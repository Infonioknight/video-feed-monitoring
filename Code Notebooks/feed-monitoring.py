import cv2
from ultralytics import YOLO

model = YOLO('Trained Models/best.pt')

# Select video source (webcam or video file)
video_capture = cv2.VideoCapture(0)  # Use webcam
# video_capture = cv2.VideoCapture('videos-predict/maybe_5MN75Ql5.mp4')  # Use video file

# Define points for the box and ROI
points = [(100, 30), (1100, 30), (1100, 700), (100, 700)]
roi_points = [(100, 30), (1100, 30), (1100, 700), (100, 700)]

# ROI coordinates (top-left and bottom-right)
tl_x, tl_y = roi_points[0]
br_x, br_y = roi_points[2]

# Define colors (Green, Red)
color_tuple = [(0, 255, 0), (0, 0, 255)]

while True:
    ret, image_frame = video_capture.read()
    
    if not ret:
        break 

    # Reset the condition to 0 (green) at the start of each frame
    condition = 0

    # Draw the box
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
                if tl_x < x1 < br_x and tl_y < y1 < br_y and tl_x < x2 < br_x and tl_y < y2 < br_y:
                    condition = 1  # Change color to red

    # Draw the updated box with the new condition
    for i in range(len(points)):
        cv2.line(image_frame, points[i], points[(i+1) % len(points)], color_tuple[condition], 6) 

    # Display the frame
    cv2.imshow('Video with Box', image_frame)

    # Exit on 'ESC' key
    if cv2.waitKey(1) & 0xFF == 27: 
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()