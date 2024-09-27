import cv2
import mediapipe as mp
import serial
import time
import serial.tools.list_ports
import sys


ports = serial.tools.list_ports.comports()
print("Available serial ports:")
for port in ports:
    print(port.device)


port_name = 'COM3' 

try:
    arduino = serial.Serial(port_name, 9600, timeout=1)
    time.sleep(2)  
    print(f"Connected to {port_name}")
except serial.SerialException as e:
    print(f"Error: {e}")
    sys.exit()

cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

def send_command_to_arduino(command):
    try:
        arduino.write(command.encode())
    except serial.SerialException as e:
        print(f"Failed to send command: {e}")

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame.")
            break


        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)

        num_fingers = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark
                if landmarks:
         
                    num_fingers = sum(
                        1 for i in [4, 8, 12, 16, 20]
                        if landmarks[i].y < landmarks[i - 2].y
                    )

        if num_fingers == 1:
            send_command_to_arduino('ON\n') 
        elif num_fingers == 2:
            send_command_to_arduino('OFF\n')  

        cv2.imshow("Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:

    cap.release()
    if 'arduino' in locals():
        arduino.close()
    cv2.destroyAllWindows()


  
