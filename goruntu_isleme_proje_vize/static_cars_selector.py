import cv2
import json
import os
import numpy as np

# Global değişkenler
drawing = False
current_points = []
regions = {"static_cars": []}

def draw_rectangle(event, x, y, flags, param):
    global drawing, current_points

    # Sol tıklama: Dikdörtgenin başlangıç noktasını belirle
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_points = [(x, y)]

    # Fare hareket ederken: Dikdörtgeni geçici olarak göster
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        temp_frame = param["frame"].copy()
        cv2.rectangle(temp_frame, current_points[0], (x, y), (0, 255, 255), 2)
        cv2.imshow("Statik Araç Seçimi", temp_frame)

    # Sol tıklamayı bırakınca: Dikdörtgeni tamamla
    elif event == cv2.EVENT_LBUTTONUP and drawing:
        drawing = False
        current_points.append((x, y))
        param["regions"].append((current_points[0], current_points[1]))
        current_points = []

def static_car_selector(video_path, output_path):
    global regions

    # Çıkış klasörünü oluştur
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Video dosyasını aç ve ilk kareyi al
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Video okunamadı!")
        cap.release()
        return

    # Pencere oluştur ve fare geri çağırma fonksiyonunu bağla
    cv2.namedWindow("Statik Araç Seçimi")
    cv2.setMouseCallback("Statik Araç Seçimi", draw_rectangle, {"frame": frame, "regions": regions["static_cars"]})

    print("Statik araçları seçin (Sol tıklama ile dikdörtgen çizin).")
    print("Seçim bittikten sonra 'q' tuşuna basın.")
    while True:
        temp_frame = frame.copy()

        # İşaretlenmiş dikdörtgenleri çizin
        for (start, end) in regions["static_cars"]:
            cv2.rectangle(temp_frame, start, end, (0, 255, 255), 2)

        cv2.imshow("Statik Araç Seçimi", temp_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 'q' tuşu: Çıkış
            break

    # İşaretlenmiş statik araçları JSON formatında kaydet
    with open(output_path, "w") as f:
        json.dump(regions, f)

    print(f"Statik araçlar başarıyla {output_path} dosyasına kaydedildi.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Proje dosya yapısına göre yollar
    video_path = r"C:\Users\90545\Desktop\goruntu_isleme_proje\videos\Test.mp4"  # Video dosyası yolu
    output_path = r"C:\Users\90545\Desktop\goruntu_isleme_proje\output\static_cars.json"  # Çıktı JSON dosyası yolu

    # Statik araç seçici çalıştır
    static_car_selector(video_path, output_path)
