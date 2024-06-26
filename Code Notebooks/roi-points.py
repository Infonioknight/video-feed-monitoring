import cv2

# Function for detecting left mouse click
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pressed:", x, y)

# Event handler
cv2.namedWindow("Frame")  # must match the imshow 1st argument
cv2.setMouseCallback("Frame", click)

# Path to the input video file
video_path = 'videos-predict/maybe_5MN75Ql5.mp4'

point1 = (2285, 1391)
point2 = (1715, 1422)
point3 = (1752, 1760)
point4 = (2418, 1735)

point_roi_1 = (2391, 1092)
point_roi_2 = (1594, 1114)
point_roi_3 = (1667, 2139)
point_roi_4 = (2728, 2113)

points = [point1, point2, point3, point4]
roi_points = [point_roi_1, point_roi_2, point_roi_3, point_roi_4]

# Open the video file
cap = cv2.VideoCapture(0)

# Infinite loop to read frames from the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    for i in range(len(points)):
        cv2.line(frame, points[i], points[(i+1) % len(points)], (255, 0, 0), 6)
    
    for j in range(len(roi_points)):
        cv2.line(frame, roi_points[j], roi_points[(j+1) % len(roi_points)], (255, 0, 0), 6)
    
    # Display the frame
    cv2.imshow("Frame", frame)
    
    # Check for a key event
    key = cv2.waitKey(1)
    # Check if the 'q' key is pressed to exit the loop
    if key & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()