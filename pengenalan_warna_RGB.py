import cv2 
from numpy import pi

kamera = cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True :
    _, frame = kamera.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int (width/2)
    cy = int (height/2)

    cv2.circle(frame, (cx,cy), 5, (25,25,25),0 )

    # mengambil nilai dari pixel warna
    pixel_center = hsv_frame[cy, cx]
    hue = pixel_center[0]
    saturation = pixel_center[1]
    value = pixel_center[2]

    color = "Tidak Terdeteksi"
    if hue == 0 | saturation == 0:
        color = "PUTIH"
    elif value < 50 :
        color = "HITAM"
    elif hue < 5 :
        color = "MERAH"
    elif hue < 15 :
        color = "ORANGE"
    elif hue < 25 :
        color = "PUTIH"
    elif hue < 35 :
        color = "KUNING"
    elif hue < 75 :
        color = "HIJAU"
    elif hue < 120 :
        color = "BIRU"
    elif hue < 165 :
        color = "UNGU"
    elif hue < 170 :
        color = "PINK"
    else :
        color = "MERAH"

    pixel_center_bgr = frame[cy, cx]

    b = int(pixel_center_bgr[0])
    g = int(pixel_center_bgr[1])
    r = int(pixel_center_bgr[2])

    print(pixel_center)
    cv2.putText(frame, color, (cx - 100, cy - 150), 0, 1.5, (b,g,r), 8)

    cv2.imshow("program pengenalan warna", frame)
    key = cv2.waitKey(1)
    if key == 27:  
        break

kamera.release()
cv2.destroyAllWindows()

