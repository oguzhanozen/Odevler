import cv2
import json
import os
import numpy as np

# Global değişkenler
drawing = False
current_points = []
regions = {"pedestrians": []}

def draw_polygon(event, x, y, flags, param):
    global drawing, current_points

    # Sol tıklama: Çokgenin bir noktasını ekle
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_points.append((x, y))

    # Sağ tıklama: Çokgeni tamamla
    elif event == cv2.EVENT_RBUTTONDOWN and drawing:
        drawing = False
        param["regions"].append(current_points.copy())
        current_points = []

def region_selector(video_path, output_path):
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
    cv2.namedWindow("Bölge Seçimi")
    cv2.setMouseCallback("Bölge Seçimi", draw_polygon, {"regions": regions["pedestrians"]})

    print("Yaya yollarını seçin (Sol tıklama ile nokta ekleyin, sağ tıklama ile tamamlayın).")
    print("Seçim bittikten sonra 'q' tuşuna basın.")
    while True:
        temp_frame = frame.copy()

        # Mevcut noktaları çizin
        for points in regions["pedestrians"]:
            cv2.polylines(temp_frame, [np.array(points, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        for point in current_points:
            cv2.circle(temp_frame, point, 5, (0, 255, 0), -1)

        cv2.imshow("Bölge Seçimi", temp_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 'q' tuşu: Çıkış
            break

    # Bölgeleri JSON formatında kaydet
    with open(output_path, "w") as f:
        json.dump(regions, f)

    print(f"Yaya yolları başarıyla {output_path} dosyasına kaydedildi.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Proje dosya yapısına göre yollar
    video_path = r"C:\Users\90545\Desktop\goruntu_isleme_proje\videos\Test.mp4"  # Video dosyası yolu
    output_path = r"C:\Users\90545\Desktop\goruntu_isleme_proje\output/regions.json"  # Çıktı JSON dosyası yolu

    # Bölge seçici çalıştır
    region_selector(video_path, output_path)
