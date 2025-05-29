import matplotlib.pyplot as plt
from collections import defaultdict


trace_file = r"C:\Users\Oguzhan\Desktop\22010903114_22010903068\topology9.tr"
node_id = "0"
interval = 0.1
throughput_data = {} 
total_bytes_sent = 0
bytes_per_target = defaultdict(int)
send_times = []
all_nodes = set()

# Her düğüm için zaman serisine göre gönderilen byte verisi
node_time_series = defaultdict(lambda: defaultdict(int))

# .tr dosyasını satır satır oku ve verileri ayrıştır
with open(trace_file, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 12:
            continue  # geçersiz satırları atla

        event = parts[0]               # Olay tipi ('+', '-', 'r' gibi)
        time = float(parts[1])         # Zaman
        src_node = parts[2]            # Gönderen düğüm
        dst_node = parts[3]            # Alıcı düğüm
        pkt_size = int(parts[5])       # Paket boyutu (byte)

        all_nodes.add(src_node)
        all_nodes.add(dst_node)

        # Zamanı belirli aralıklara (interval) göre gruplandır
        time_slot = round(time / interval) * interval

        # Sadece gönderim olaylarını dikkate al
        if event == "+":
            node_time_series[src_node][time_slot] += pkt_size

            # Eğer analiz edilen düğümse ek kayda al
            if src_node == node_id:
                if time_slot not in throughput_data:
                    throughput_data[time_slot] = 0
                throughput_data[time_slot] += pkt_size
                total_bytes_sent += pkt_size
                bytes_per_target[dst_node] += pkt_size
                send_times.append(time)

# Gönderim süresini hesapla (ilk ve son gönderim zamanı)
if send_times:
    min_time = min(send_times)
    max_time = max(send_times)
    duration = max_time - min_time
else:
    min_time = max_time = duration = 0.0

# Düğüme hiç veri gönderilmemişse bile 0 atamak için
for node in all_nodes:
    if node not in bytes_per_target:
        bytes_per_target[node] = 0

# Throughput değerlerini (kbps) hesapla
x = sorted(throughput_data.keys())
y = [8 * throughput_data[t] / 1000 / interval for t in x]  # Byte → kbps

print(f"\n Düğüm {node_id} tarafından gönderilen toplam veri:")
print(f"- {total_bytes_sent} byte")
print(f"- Gönderim süresi: {min_time:.2f} s → {max_time:.2f} s (Toplam: {duration:.2f} saniye)\n")

print(f"➤ Düğüm {node_id} → Diğer Düğümlere Veri Dağılımı (byte cinsinden):")
for target in sorted(bytes_per_target.keys(), key=int):
    print(f"  → Düğüm {target}: {bytes_per_target[target]} byte")

# Topolojide tanımlı tüm düğümler (0'dan 8'e kadar)
expected_nodes = set(str(i) for i in range(9))

# .tr dosyasında hiç görünmeyen (yani veri gönderip almayan) düğümler
inactive_nodes = expected_nodes - all_nodes

# Bu düğümleri kullanıcıya bildir
if inactive_nodes:
    print("\n Veri akışına dahil olmayan düğümler (topolojide var ama .tr içinde hiç görünmemiş):")
    for node in sorted(inactive_nodes, key=int):
        print(f" - Düğüm {node}")
else:
    print("\n Tüm düğümler veri akışına en az bir kez dahil olmuş.")

plt.figure()
plt.plot(x, y, marker='o')
plt.xlabel("Zaman (s)")
plt.ylabel("Throughput (kbps)")
plt.title(f"Düğüm {node_id} için Throughput Grafiği")
plt.grid(True)
plt.tight_layout()
plt.show()

# Tüm zaman dilimlerini belirle
all_time_slots = set()
for stats in node_time_series.values():
    all_time_slots.update(stats.keys())
all_time_slots = sorted(all_time_slots)

# Her düğüm için grafiği ayrı ayrı çiz
plt.figure()
for node in sorted(all_nodes, key=int):
    y_series = []
    for t in all_time_slots:
        byte_val = node_time_series[node].get(t, 0)
        throughput_kbps = 8 * byte_val / 1000 / interval
        y_series.append(throughput_kbps)
    plt.plot(all_time_slots, y_series, marker='o', label=f"Düğüm {node}")

plt.xlabel("Zaman (s)")
plt.ylabel("Throughput (kbps)")
plt.title("Tüm Düğümler İçin Toplu Throughput Grafiği")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
