import cv2
import numpy as np

# buka kamera
kamera = cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# atur brightness & contrast (opsional, tergantung kamera)
kamera.set(cv2.CAP_PROP_BRIGHTNESS, 0.6)
kamera.set(cv2.CAP_PROP_CONTRAST, 0.7)

while True:
    ret, frame = kamera.read()
    if not ret:
        break

    # flip agar tidak mirror
    frame = cv2.flip(frame, 1)

    # gunakan filter untuk mengurangi noise
    frame = cv2.bilateralFilter(frame, 9, 75, 75)

    # konversi ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # definisi range warna (lebih luas)
    warna_ranges = {
        "MERAH": [(np.array([0, 100, 100]), np.array([15, 255, 255])),
                  (np.array([160, 100, 100]), np.array([179, 255, 255]))],
        "ORANGE": [(np.array([16, 100, 100]), np.array([25, 255, 255]))],
        "KUNING": [(np.array([26, 100, 100]), np.array([35, 255, 255]))],
        "HIJAU": [(np.array([36, 100, 100]), np.array([75, 255, 255]))],
        "BIRU": [(np.array([76, 100, 100]), np.array([120, 255, 255]))],
        "UNGU": [(np.array([121, 100, 100]), np.array([165, 255, 255]))],
        "PINK": [(np.array([166, 100, 100]), np.array([179, 255, 255]))],
        "PUTIH": [(np.array([0, 0, 180]), np.array([180, 40, 255]))],
        "HITAM": [(np.array([0, 0, 0]), np.array([180, 255, 50]))]
    }

    # ambil area kecil di tengah (ROI)
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    roi = hsv[cy-5:cy+5, cx-5:cx+5]  # area 10x10 pixel
    avg_hsv = np.mean(roi.reshape(-1, 3), axis=0).astype(int)
    pixel_hsv = avg_hsv

    # gambar lingkaran di tengah
    cv2.circle(frame, (cx, cy), 5, (0, 0, 0), -1)

    # cek warna berdasarkan range
    detected_color = "Tidak Terdeteksi"
    for warna, ranges in warna_ranges.items():
        for lower, upper in ranges:
            if np.all(pixel_hsv >= lower) and np.all(pixel_hsv <= upper):
                detected_color = warna
                break
        if detected_color != "Tidak Terdeteksi":
            break

    # tampilkan teks
    cv2.putText(frame, detected_color, (cx - 100, cy - 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    cv2.imshow("Deteksi Warna HSV (Versi Jernih & Luas)", frame)

    # keluar dengan ESC
    if cv2.waitKey(1) == 27:
        break

kamera.release()
cv2.destroyAllWindows()
