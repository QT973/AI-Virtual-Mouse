import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
pTime = 0
cTime = 0
height = 0
height = 0
while True:
    Success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    # vì hands là dùng RGB mà trong opencv dùng màu BGR
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)  # xuất ra tọa độ của bàn tay
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Nối các lanmarks lại với nhau
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id,":",cx,cy)
                if id == 3:
                    cv2.circle(frame, (cx, cy), 5, (1, 1, 1), cv2.FILLED)
                    width = (screen_w/w)*cx
                    height = (screen_h/h)*cy
                    pyautogui.moveTo(width, height)
                if id == 8:
                    cv2.circle(frame, (cx, cy), 5, (1, 1, 1), cv2.FILLED)
                    width_ver1 = (screen_w/w)*cx
                    heigh_ver1 = (screen_h/h)*cy
                    print("outside", abs(height - heigh_ver1),
                          "and", abs(width-width_ver1))
                    if abs(height - heigh_ver1) < 20 and abs(width-width_ver1) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS:{int(fps)}", (20, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)
    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) == ord("b"):
        break
