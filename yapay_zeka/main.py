import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Sabitler
nokta_sayisi = 50  # İhtiyaç noktaları sayısı
depo_sayisi = 1    # Depo sayısı    

# Rastgele ihtiyaç noktaları ve depo koordinatları oluşturma
np.random.seed(0)  # Tekrar edilebilir sonuçlar için
ihtiyac_noktalari_koordinatlar = np.random.randint(0, 100, size=(nokta_sayisi, 2))
depo_koordinatlar = np.random.randint(49, 50, size=(depo_sayisi, 2))

# Koordinatları DataFrame formatında düzenleme
ihtiyac_noktalari_df = pd.DataFrame(ihtiyac_noktalari_koordinatlar, columns=['X', 'Y'])
ihtiyac_noktalari_df.index.name = 'Ihtiyac_Noktasi'
depo_koordinatlar_df = pd.DataFrame(depo_koordinatlar, columns=['X', 'Y'])
depo_koordinatlar_df.index.name = 'Depo'

# İhtiyaç noktaları arasındaki mesafeler
mesafeler_ihtiyac = cdist(ihtiyac_noktalari_koordinatlar, ihtiyac_noktalari_koordinatlar, metric='euclidean')
mesafeler_ihtiyac_df = pd.DataFrame(mesafeler_ihtiyac, index=ihtiyac_noktalari_df.index, columns=ihtiyac_noktalari_df.index)

# Depolar ile ihtiyaç noktaları arasındaki mesafeler
mesafeler_depolar = cdist(depo_koordinatlar, ihtiyac_noktalari_koordinatlar, metric='euclidean')
mesafeler_depolar_df = pd.DataFrame(mesafeler_depolar, index=depo_koordinatlar_df.index, columns=ihtiyac_noktalari_df.index)

# Mesafe tablosunu Excel'e kaydetme
with pd.ExcelWriter('C:/Users/90545/Desktop/yapay_zeka/output/Mesafe_Tablolari.xlsx') as writer:
    mesafeler_ihtiyac_df.to_excel(writer, sheet_name='Ihtiyac_Ihtiyac')
    mesafeler_depolar_df.to_excel(writer, sheet_name='Depolar_Ihtiyac')

print("Mesafe tablolari Excel dosyasina kaydedildi.")

# Talep miktarını sabit belirleme (0-20 birim arasında)
medikal_ihtiyac = np.random.randint(0, 20, size=(nokta_sayisi, 1))
gida_ihtiyac = np.random.randint(0, 20, size=(nokta_sayisi, 1))

# Yardım talep tablosunu oluşturma
ihtiyac_df = pd.DataFrame(
    {
        'Medikal_Ihtiyac': medikal_ihtiyac.flatten(),
        'Gida_Ihtiyac': gida_ihtiyac.flatten()
    },
    index=ihtiyac_noktalari_df.index
)

# Yardım talep tablosunu Excel'e kaydetme
ihtiyac_df.to_excel('C:/Users/90545/Desktop/yapay_zeka/output/Yardim_Talep_Tablolari.xlsx')

print("Yardim talep tablosu Excel dosyasina kaydedildi.")

# Görselleştirme
plt.figure(figsize=(10, 8))
plt.scatter(ihtiyac_noktalari_df['X'], ihtiyac_noktalari_df['Y'], c='blue', label='Ihtiyac Noktalari')
plt.scatter(depo_koordinatlar_df['X'], depo_koordinatlar_df['Y'], c='red', marker='x', s=100, label='Depolar')

# Grafikte etiketler ve başlık ekleyin
plt.xlabel("X Koordinati")
plt.ylabel("Y Koordinati")
plt.legend()
plt.title("Ihtiyac Noktalari ve Depolarin Koordinatlari")

# Görselleştirmeyi dosyaya kaydet
cikti_grafik_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Ihtiyac_Noktalari_ve_Depolar.png'
plt.savefig(cikti_grafik_yolu)

print(f"Grafik '{cikti_grafik_yolu}' dosyasina kaydedildi.")

# Yardım talep tablosunun görselleştirilmesi
plt.figure(figsize=(12, 6))
ihtiyac_df.plot(kind='bar', stacked=True, figsize=(12, 6), color=['skyblue', 'orange'])
plt.title("Ihtiyac Noktalarinin Yardim Talepleri")
plt.xlabel("Ihtiyac Noktalari")
plt.ylabel("Talep Miktari")
plt.legend(title="Yardim Turu")
plt.tight_layout()

# Yardım talep grafiğini kaydet
ihtiyac_grafik_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Yardim_Talepleri_Grafik.png'
plt.savefig(ihtiyac_grafik_yolu)

print(f"Yardim talep grafiği '{ihtiyac_grafik_yolu}' dosyasina kaydedildi.")
