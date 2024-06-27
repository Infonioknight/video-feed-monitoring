import cv2

# Initialize the list to store coordinates for the region of interest (ROI)
roi_click_coordinates = []

# Function for detecting left mouse click and recording coordinates for ROI
def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Write the coordinates to the roi-coordinates.txt file
        with open('roi-coordinates.txt', 'a') as file:
            file.write(f"{x}, {y}\n")
        print("Pressed:", x, y)
        # Add the point to the list
        roi_click_coordinates.append((x, y))
        # Check if we have 4 points
        if len(roi_click_coordinates) == 4:
            # Release the video capture object and close all windows
            cap.release()
            cv2.destroyAllWindows()

# Read points from box-coordinates.txt
def read_box_coordinates(filename):
    points = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                x, y = map(int, line.strip().split(','))
                points.append((x, y))
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return points

# Event handler setup
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click)
cv2.waitKey(100)  # Ensure the window has time to initialize

# Clear the contents of roi-coordinates.txt when the program starts
open('roi-coordinates.txt', 'w').close()

# Read box coordinates from box-coordinates.txt
box_coordinates = read_box_coordinates('box-coordinates.txt')

# Open the video file or camera
cap = cv2.VideoCapture(0)

# Ensure the camera is initialized
for _ in range(10):
    ret, frame = cap.read()

# Infinite loop to read frames from the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Draw the box using points from box-coordinates.txt if 4 points are available
    if len(box_coordinates) == 4:
        for i in range(len(box_coordinates)):
            cv2.line(frame, box_coordinates[i], box_coordinates[(i+1) % len(box_coordinates)], (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow("Frame", frame)
    
    # Check for a key event
    key = cv2.waitKey(10) 
    # Check if the 'q' key is pressed to exit the loop
    if key & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
