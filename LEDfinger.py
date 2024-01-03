import cv2
import mediapipe as mp
import time
import pyfirmata

time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils #use function drawing_utils to draw straight connect landmark point
mp_hand=mp.solutions.hands #use function hands to find hand on camera
def resizeImg(image, square = 10):
    width = int(image.shape[1] * square/8)
    height = int(image.shape[0] * square/10)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation =cv2.INTER_AREA)

tipIds=[4,8,12,16,20] # media-pipe position  of fingertips

def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        # print("Input is an integer number. Number = ", val)
        bv = True
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            # print("Input is a float  number. Number = ", val)
            bv = True
        except ValueError:
            # print("No.. input is not a number. It's a string")
            bv = False
    return bv

cport = input('Enter the camera port: ')
while not (check_user_input(cport)):
    print('Please enter a number not string')
    cport = input('Enter the camera port: ')

comport = input('Enter the arduino board COM port: ')
while not (check_user_input(comport)):
    print('Please enter a number not string')
    comport = input('Enter the arduino board COM port: ')

board=pyfirmata.Arduino('COM'+comport)
led_1=board.get_pin('d:13:o') #Set pin to output
led_2=board.get_pin('d:12:o')
led_3=board.get_pin('d:11:o')
led_4=board.get_pin('d:10:o')
led_5=board.get_pin('d:9:o')


video=cv2.VideoCapture(int(cport)) #OpenCamera at index position 0

with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:#(min_detection_confidence, min_tracking_confidence) are Value to considered for detect and tracking image
    while True:
        ret,image=video.read() #Read frame in camera video
        image = resizeImg(image, square = 15)
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  #convert color BGR to RGB
        image.flags.writeable=False  #to improve nothing drawed in image
        results=hands.process(image) #process image
        image.flags.writeable=True #can drawing  image
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  #convert color RGB to BGR
        TotalFinger = 0
        fingers=[]
        FingerType= []
        
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)               
                    
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
                   FingerType.append("Index Finger")
                   fingers.append("1")
                   led_1.write(1)
                else:
                   led_1.write(0)

                if cy12 < cy10:
                   FingerType.append("Middle Finger")
                   fingers.append("1")
                   led_2.write(1) 
                else:
                   led_2.write(0)  

                if cy16 < cy14:
                   FingerType.append("Ring Finger")
                   fingers.append("1")  
                   led_3.write(1)
                else:
                   led_3.write(0)
                
                if cy20 < cy18:
                   FingerType.append("Pinky Finger")
                   fingers.append("1")    
                   led_4.write(1)
                else:
                   led_4.write(0)   

                if cx4 > cx2:
                   FingerType.append("Thumb") 
                   fingers.append("1")
                   led_5.write(1)
                else:
                   led_5.write(0)
            
                TotalFinger = len(fingers)
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)  #drawing hand skeleton from hand_landmark point

            #led(total,led_1,led_2,led_3,led_4,led_5) #import function in module to control arduino output
            """
            creat condition to put text in frame

            """
            if ((results.multi_hand_landmarks))!="None":
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, str(int(TotalFinger)), (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, str(FingerType), (100, 575), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)


        cv2.imshow("Frame",image)  #show edited image
        k=cv2.waitKey(1)
        if k==ord('q'):  #press "q" to exit programe
            break
video.release()
cv2.destroyAllWindows()