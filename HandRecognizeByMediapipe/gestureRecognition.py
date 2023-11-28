import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)

while True:
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    yPos = int(lm.y * imgHeight)
                    xPos = int(lm.x * imgWidth)
                    cv2.putText(img, str(i), (xPos-20, yPos-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,255),1)
                    print(i, xPos, yPos)
        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break
