import cv2
import numpy as np
import json
import math

# Statik araç JSON dosyasını yükleme
with open(r"C:\Users\90545\Desktop\goruntu_isleme_proje\output\static_cars.json", "r") as f:
    static_cars = json.load(f).get("static_cars", [])

# Yaya yollarını içeren JSON dosyasını yükleme
with open(r"C:\Users\90545\Desktop\goruntu_isleme_proje\output\regions.json", "r") as f:
    regions = json.load(f)

# Yaya yollarını alın
pedestrian_paths = regions.get("pedestrians", [])

cap = cv2.VideoCapture(r"C:\Users\90545\Desktop\goruntu_isleme_proje\videos\Test.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)  # Video FPS değeri
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (5, 5), 0)

paused = False

# Hareketli nesneler için merkez noktalarını takip etmek
object_centers = {}  # Nesne ID'sine göre {ID: [(x, y), ...]} şeklinde saklanır
next_object_id = 0

# Piksel-metre oranı (örnek: 1 piksel = 0.05 metre)
pixel_to_meter_ratio = 0.05

# Toplam yaya ve araç sayacı
total_pedestrians = 0
total_cars = 0

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        frame_diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(frame_diff, 10, 250, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=5)
        thresh = cv2.erode(thresh, None, iterations=1)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w > 30 and h > 30:
                cx = x + w // 2
                cy = y + h // 2

                # Mevcut nesneleri güncelle
                matched = False
                for object_id, center_history in object_centers.items():
                    prev_cx, prev_cy = center_history[-1]
                    distance = math.sqrt((cx - prev_cx) ** 2 + (cy - prev_cy) ** 2)

                    if distance < 50:  # Nesne eşleşme toleransı
                        object_centers[object_id].append((cx, cy))
                        matched = True
                        break

                if not matched:
                    object_centers[next_object_id] = [(cx, cy)]
                    object_id = next_object_id  # Yeni oluşturulan ID'yi kaydet
                    next_object_id += 1
                else:
                    # Eşleşme durumunda mevcut ID'yi kullan
                    object_id = object_id  

                # Hız hesaplama
                if len(object_centers[object_id]) > 1:
                    prev_cx, prev_cy = object_centers[object_id][-2]
                    pixel_distance = math.sqrt((cx - prev_cx) ** 2 + (cy - prev_cy) ** 2)
                    real_distance = pixel_distance * pixel_to_meter_ratio  # Pikselden metreye çevir
                    speed_m_per_s = real_distance * fps  # Hız (m/s)
                    speed_km_per_h = speed_m_per_s * 3.6  # Hız (km/s)

                    cv2.putText(frame, f"Hiz: {speed_km_per_h:.2f} km/s", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # Araç veya yaya kontrolü
                if w > 120 and h > 110:  # Araç
                    in_pedestrian_path = any(
                        cv2.pointPolygonTest(np.array(path, dtype=np.int32), (cx, cy), False) >= 0
                        for path in pedestrian_paths
                    )
                    if in_pedestrian_path:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(frame, "Arac Yol Ihlali", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.putText(frame, "Arac", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    total_cars += 1

                elif w > 10 and h > 20:  # Yaya
                    in_pedestrian_path = any(
                        cv2.pointPolygonTest(np.array(path, dtype=np.int32), (cx, cy), False) >= 0
                        for path in pedestrian_paths
                    )
                    if not in_pedestrian_path:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(frame, "Yaya Yol Ihlali", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, "Yaya", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    total_pedestrians += 1

     # JSON'dan alınan statik araçları kontrol edin ve çizin
        for ((x1, y1), (x2, y2)) in static_cars:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Statik aracın merkez noktası
            in_pedestrian_path = any(
                cv2.pointPolygonTest(np.array(path, dtype=np.int32), (cx, cy), False) >= 0
                for path in pedestrian_paths
            )
            if in_pedestrian_path:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Statik Arac Yol Ihlali", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(frame, "Statik Arac", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Frame", frame)
        prev_gray = gray

    key = cv2.waitKey(23) & 0xFF
    if key == 27:  # ESC tuşu ile çık
        break
    elif key == 32:  # SPACE tuşu ile duraklat/devam et
        paused = not paused

cap.release()
cv2.destroyAllWindows()

# Toplam yaya ve araç sayısını yazdır
print(f"Toplam tespit edilen yayalar: {total_pedestrians}")
print(f"Toplam tespit edilen araçlar: {total_cars}")
