import cv2

click_coordinates = []

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        with open('box-coordinates.txt', 'a') as file:
            file.write(f"{x}, {y}\n")
        print("Pressed:", x, y)
        click_coordinates.append((x, y))
        if len(click_coordinates) == 4:
            cap.release()
            cv2.destroyAllWindows()

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click)
cv2.waitKey(100) 

open('box-coordinates.txt', 'w').close()

cap = cv2.VideoCapture(0)

for _ in range(10):
    ret, frame = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(10) 
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
