import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from main import depo_koordinatlar, ihtiyac_noktalari_df

# Küme sayısı
kume_sayisi = 4

# KMeans algoritmasını uygulayın
kmeans = KMeans(n_clusters=kume_sayisi, random_state=0)
kmeans.fit(ihtiyac_noktalari_df)

# Kümeleri ihtiyaç noktalarına atayın
ihtiyac_noktalari_df['Kume'] = kmeans.labels_

# Daha önceden oluşturulan talep tablosunu içe aktarma
talep_tablo_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Yardim_Talep_Tablolari.xlsx'
talep_verisi = pd.read_excel(talep_tablo_yolu)

# Küme bilgilerini ve ihtiyaç noktalarını birleştirme
ihtiyac_talep_kume_verisi = talep_verisi.copy()  # Talep verisinin bir kopyasını oluştur
ihtiyac_talep_kume_verisi['Kume'] = ihtiyac_noktalari_df['Kume']  # Küme bilgilerini talep verisine ekle

# Detaylı tabloyu Excel'e kaydetme
detayli_cikti_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Kumeleme_Sonuclari.xlsx'
ihtiyac_talep_kume_verisi.to_excel(detayli_cikti_yolu, index=False)

print(f"Detaylı küme ihtiyaç bilgileri Excel dosyasına '{detayli_cikti_yolu}' yolunda kaydedildi.")


# Sonuçları görselleştirme
plt.figure(figsize=(10, 6))
for kume_id in range(kume_sayisi):
    kume_noktalari = ihtiyac_noktalari_df[ihtiyac_noktalari_df['Kume'] == kume_id]
    plt.scatter(kume_noktalari['X'], kume_noktalari['Y'], label=f'Kume {kume_id + 1}')

# Depo konumlarını da görsele ekleyelim
plt.scatter(depo_koordinatlar[:, 0], depo_koordinatlar[:, 1], color='black', marker='x', s=100, label='Depolar')
plt.xlabel('X Koordinati')
plt.ylabel('Y Koordinati')
plt.legend()
plt.title('Ihtiyac Noktalarinin KMeans ile Kumeleme Sonuclari')

# Görseli PNG olarak kaydetme
cikti_gorsel_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Kumeleme_Sonuclari.png'
plt.savefig(cikti_gorsel_yolu)

print(f"Kumeleme sonuç görseli '{cikti_gorsel_yolu}' dosyasina kaydedildi.")

