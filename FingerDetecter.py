#This code demonstrate how to show location of hand landmark
import cv2
import mediapipe as mp

Nfing = 0
cap = cv2.VideoCapture(0)

#Call hand pipe line module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
def resizeImg(img, square = 10):
    width = int(img.shape[1] * square/8)
    height = int(img.shape[0] * square/10)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation =cv2.INTER_AREA)



while True:
    success, img = cap.read()
    rect, img = cap.read()
    img = resizeImg(img, square = 15)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    FingerCount = []
    FingerType= []
    TotalFinger = 0
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                if id == 20:
                    id20 = int(id)
                    cy20 = cy

                if id == 18:
                    id18 = int(id)
                    cy18 = cy
                
                if id == 16:
                    id16 = int(id)
                    cy16 = cy    
                if id == 14:
                    id14 = int(id)
                    cy14 = cy
                
                if id == 12:
                    id12 = int(id)
                    cy12 = cy
                if id == 10:
                    id10 = int(id)
                    cy10 = cy
                
                if id == 8:
                    id8 = int(id)
                    cy8 = cy
                if id == 6:
                    id6 = int(id)
                    cy6 = cy
                
                if id == 4:
                    id4 = int(id)
                    cx4 = cx
                if id == 2:
                    id2 = int(id)
                    cx2 = cx
                
                if id == 0:
                    id0 = int(id)
                    cy0 = cy    
            

            if cy8 < cy6:
                FingerCount.append('1')
                FingerType.append("Index Finger")

            if cy12 < cy10:
                FingerCount.append('2')
                FingerType.append("Middle Finger")
      
            if cy16 < cy14:
                FingerCount.append('3')
                FingerType.append("Ring Finger")
    
            if cy20 < cy18:
                FingerCount.append('4')
                FingerType.append("Pinky Finger")
          
            if cx4 > cx2:
                FingerCount.append('5')
                FingerType.append("Thumb")
           
            TotalFinger = len(FingerCount)
            if TotalFinger > 5:
                TotalFinger = 5
            
            

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.putText(img, str(int(TotalFinger)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cv2.putText(img, str(list(FingerType)), (10, 600), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 3)
    cv2.putText(img, ("Chaiyapruk Parinyanuntakan"), (700, 650), cv2.FONT_HERSHEY_PLAIN, 2,  
                (255, 0, 0), 3) 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
#Closeing all open windows
#cv2.destroyAllWindows()