import cv2

roi_click_coordinates = []

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        with open('Data Files/roi-coordinates.txt', 'a') as file:
            file.write(f"{x}, {y}\n")
        print("Pressed:", x, y)
        roi_click_coordinates.append((x, y))
        if len(roi_click_coordinates) == 4:
            cap.release()
            cv2.destroyAllWindows()

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

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click)
cv2.waitKey(100) 

open('Data Files/roi-coordinates.txt', 'w').close()

box_coordinates = read_box_coordinates('Data Files/box-coordinates.txt')

cap = cv2.VideoCapture(0)

for _ in range(10):
    ret, frame = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
 
    if len(box_coordinates) == 4:
        for i in range(len(box_coordinates)):
            cv2.line(frame, box_coordinates[i], box_coordinates[(i+1) % len(box_coordinates)], (0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(10) 
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
