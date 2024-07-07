import cv2
from ultralytics import YOLO

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

box_coordinates = read_coordinates('Data Files/box-coordinates.txt')

roi_coordinates = read_coordinates('Data Files/roi-coordinates.txt')

if len(box_coordinates) != 4 or len(roi_coordinates) != 4:
    raise ValueError("Both box-coordinates.txt and roi-coordinates.txt must contain exactly 4 points each.")

points = box_coordinates
roi_points = roi_coordinates

tl_x, tl_y = roi_points[0]
br_x, br_y = roi_points[2]

color_tuple = [(0, 255, 0), (0, 0, 255)]

model = YOLO('Trained Models/best.pt')

video_capture = cv2.VideoCapture(0) 

while True:
    ret, image_frame = video_capture.read()
    
    if not ret:
        break 

    condition = 0

    for i in range(len(points)):
        cv2.line(image_frame, points[i], points[(i+1) % len(points)], color_tuple[condition], 3)

    results = model(image_frame, show=False, conf=0.5, save=False, verbose=False)
    for result in results:
        boxes = result.boxes.cpu().numpy()
        xyxy = boxes.xyxy
        classes = boxes.cls

        for index, class_value in enumerate(classes):
            if class_value == 3.0: 
                x1, y1, x2, y2 = xyxy[index]
                if tl_x < x1 < br_x and tl_y < y1 < br_y and tl_x < x2 < br_x and tl_y < y2 < br_y:
                    condition = 1 

    for i in range(len(points)):
        cv2.line(image_frame, points[i], points[(i+1) % len(points)], color_tuple[condition], 3)

    cv2.imshow('Video with Box', image_frame)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

video_capture.release()
cv2.destroyAllWindows()
