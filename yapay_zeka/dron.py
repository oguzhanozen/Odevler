import pandas as pd

# Daha önceden oluşturduğumuz talep tablosunu içe aktarma
talep_tablo_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Yardim_Talep_Tablolari.xlsx'
talep_verisi = pd.read_excel(talep_tablo_yolu)

# Daha önceki KMeans kümeleme sonuçlarına göre ihtiyaç noktalarının küme bilgilerini içe aktarma
kumeleme_sonuc_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Kumeleme_Sonuclari.xlsx'
kumeleme_verisi = pd.read_excel(kumeleme_sonuc_yolu)

# Kümelere göre tıbbi malzeme ve yiyecek talebini toplama
talep_verisi['Kume'] = kumeleme_verisi['Kume']  # İhtiyaç noktalarının kümelerini ekleyin
kume_bazli_talepler = talep_verisi.groupby('Kume').sum().reset_index()  # Küme bazında toplam talepleri hesaplayın

# Drone kapasitesi
drone_kapasitesi = 30

# Yükleme stratejisi fonksiyonu
def drone_yuk_hesapla(ihtiyac, kapasite):
    drone_yukleri = []
    toplam_dron = ihtiyac // kapasite  # Tam kapasiteyle kaç dron gerekli
    kalan_yuk = ihtiyac % kapasite  # Kapasite dolduktan sonra kalan yük
    drone_yukleri.extend([kapasite] * toplam_dron)  # Tam dolu dronları ekle
    if kalan_yuk > 0:
        drone_yukleri.append(kalan_yuk)  # Kalan yük için ek dron
    return drone_yukleri

# Her küme için yük dağıtımını hesaplayın
kume_bazli_talepler['Tibbi_Drone_Yukleri'] = kume_bazli_talepler['Medikal_Ihtiyac'].apply(lambda x: drone_yuk_hesapla(x, drone_kapasitesi))
kume_bazli_talepler['Gida_Drone_Yukleri'] = kume_bazli_talepler['Gida_Ihtiyac'].apply(lambda x: drone_yuk_hesapla(x, drone_kapasitesi))

# Verileri metin dosyasına kaydetme
cikti_dosya_yolu = 'C:/Users/90545/Desktop/yapay_zeka/output/Kume_Yukleme_Bilgileri.txt'
with open(cikti_dosya_yolu, 'w') as dosya:
    for i, satir in kume_bazli_talepler.iterrows():
        dosya.write(f"Kume {satir['Kume'] + 1}:\n")
        dosya.write(f"  Tibbi Malzeme Ihtiyac: {satir['Medikal_Ihtiyac']} birim\n")
        dosya.write(f"  Gerekli Drone Yukleri (Tibbi): {satir['Tibbi_Drone_Yukleri']}\n")
        dosya.write(f"  Yiyecek Ihtiyac: {satir['Gida_Ihtiyac']} birim\n")
        dosya.write(f"  Gerekli Drone Yukleri (Yiyecek): {satir['Gida_Drone_Yukleri']}\n")
        dosya.write("\n")

print(f"Veriler '{cikti_dosya_yolu}' dosyasina kaydedildi.")

