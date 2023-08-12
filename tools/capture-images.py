import cv2

cap = cv2.VideoCapture(0)

for i in range(20):
    while(True):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imshow('image', frame)
        if cv2.waitKey(1) == 97:
            cv2.imwrite(f"images/{i}.jpg",frame)
            break

cv2.destroyAllWindows()
cap.release()
