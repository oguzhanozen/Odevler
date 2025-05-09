import pandas as pd
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from main import ihtiyac_noktalari_df, depo_koordinatlar
from kmeans import ihtiyac_noktalari_df, kume_sayisi

# En kısa yolu bulmak için depolar ile her bir ihtiyaç noktaları arasındaki mesafeleri hesaplama

def en_yakin_depo(nokta, depolar):
    mesafeler = np.linalg.norm(depolar - nokta, axis=1)
    en_yakin_indeks = np.argmin(mesafeler)
    return en_yakin_indeks, mesafeler[en_yakin_indeks]

# Her ihtiyaç noktasını en yakın depoya bağlama
cizim_kenarlari = []
for i, nokta in ihtiyac_noktalari_df.iterrows():
    en_yakin_depo_indeks, mesafe = en_yakin_depo(nokta[['X', 'Y']].values, depo_koordinatlar)
    cizim_kenarlari.append((i, 'depo_' + str(en_yakin_depo_indeks)))  # Ihtiyaç noktası ile en yakın depo arasında bir kenar ekle

# Görselleştirme
plt.figure(figsize=(10, 6))
for kume_id in range(kume_sayisi):
    kume_noktalari = ihtiyac_noktalari_df[ihtiyac_noktalari_df['Kume'] == kume_id]
    plt.scatter(kume_noktalari['X'], kume_noktalari['Y'], label=f'Kume {kume_id + 1}')

# Depo konumlarını çizme
plt.scatter(depo_koordinatlar[:, 0], depo_koordinatlar[:, 1], color='black', marker='x', s=100, label='Depolar')

# Ihtiyaç noktalarını en yakın depoya bağlayan kenarları çizme
pozisyonlar = {i: (satir['X'], satir['Y']) for i, satir in ihtiyac_noktalari_df.iterrows()}  # Ihtiyaç noktalarının pozisyonları
depo_pozisyonlar = {f'depo_{i}': (depo[0], depo[1]) for i, depo in enumerate(depo_koordinatlar)}  # Depo pozisyonları
pozisyonlar.update(depo_pozisyonlar)  # Depo pozisyonlarını da ekle

# Çizilecek kenarları (en kısa yollar) gösterme
G = nx.Graph()
G.add_edges_from(cizim_kenarlari)
nx.draw_networkx_edges(G, pozisyonlar, edgelist=cizim_kenarlari, edge_color='r', width=2, style='dashed')

plt.xlabel('X Koordinati')
plt.ylabel('Y Koordinati')
plt.legend()
plt.title('Kumeleme ve En Kisa Depo Baglantilari')

# Görseli PNG olarak kaydetme
cikti_gorsel_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Kumeleme_ve_En_Kisa_Depo_Baglantilari.png'
plt.savefig(cikti_gorsel_yolu)

print(f"Kumeleme ve En Kisa Depo Baglantilari sonuc görseli '{cikti_gorsel_yolu}' dosyasina kaydedildi.")
