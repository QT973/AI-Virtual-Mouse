import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
screen_w,screen_h = pyautogui.size()
pTime = 0
cTime = 0
while True:
    Success, frame = cap.read()
    frame = cv2.flip(frame,1)  
    # vì hands là dùng RGB mà trong opencv dùng màu BGR
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    h,w,c = frame.shape
    # print(results.multi_hand_landmarks)  # xuất ra tọa độ của bàn tay
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS) #Nối các lanmarks lại với nhau 
            for id , lm in enumerate(handLms.landmark):
                # print(id,lm)
               
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(id,":",cx,cy)
                if id==8:
                    cv2.circle(frame, (cx, cy), 5, (1,1,1), cv2.FILLED)
                    width = (screen_h/w)*cx
                    height = (screen_h/h)*cy
                    pyautogui.moveTo(width,height)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS:{int(fps)}", (20, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)
    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) == ord("b"):
        break
