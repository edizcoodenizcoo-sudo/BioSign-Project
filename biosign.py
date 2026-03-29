import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# --- 1. SİMÜLASYON VERİSİ ---
x = np.linspace(400, 4000, 1000)
baseline = 0.3 * np.exp(-((x - 1000) / 500)**2) + 0.2 * np.exp(-((x - 2500) / 800)**2)
noise = np.random.normal(0, 0.04, len(x))
biosignature = 0.25 * np.exp(-((x - 2920) / 25)**2) # Biyo-iz (Karbonat/Organik)
raw_signal = baseline + noise + biosignature

# --- 2. ANALİZ ---
cleaned = savgol_filter(raw_signal, 41, 3)
peaks, _ = find_peaks(cleaned, height=0.1, prominence=0.05)

# --- 3. VERİ VE RENK HAZIRLIĞI ---
table_data = []
cell_colors = [] # Hücre renklerini tutacak liste

for p in peaks:
    pos = x[p]
    if 2800 <= pos <= 3100:
        mineral, color_hex, status = "Organik Karbonat / C-H", "#FF0000", "BİYO-İZ ADAYI!" # Kırmızı
    elif 1500 <= pos < 2800:
        mineral, color_hex, status = "Sülfat Tuzları / Ca", "#00FF00", "Jeolojik / Su İzli" # Yeşil
    elif 800 <= pos < 1500:
        mineral, color_hex, status = "Olivin / Mg-Si", "#D2B48C", "Volkanik Arka Plan" # Tan/Sarımsı
    else:
        mineral, color_hex, status = "Pyroxene / Feldspar", "#0000FF", "Genel Jeoloji" # Mavi
    
    table_data.append([f"{pos:.1f}", mineral, "", status]) # Renk sütununu boş bırakıyoruz
    # Tablo hücreleri için renk matrisi: [Pik, Mineral, RENK HÜCRESİ, Durum]
    cell_colors.append(["#FFFFFF", "#FFFFFF", color_hex, "#FFFFFF"])

# --- 4. GÖRSELLEŞTİRME (GRAFİK + RENKLİ TABLO) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})


ax1.plot(x, cleaned, color='#1f77b4', linewidth=2.5, label='İşlenmiş Spektrum Sinyali')
for p in peaks:
    peak_color = "#FF0000" if 2800 <= x[p] <= 3100 else "#333333"
    ax1.scatter(x[p], cleaned[p], color=peak_color, s=100, zorder=5, edgecolors='white')

ax1.set_title("BioSign-Sim: Otonom Spektrum Analizi ve Kimyasal Eşleştirme", fontsize=16, pad=20)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()


ax2.axis('tight')
ax2.axis('off')
columns = ("Pik Konumu (cm⁻¹)", "Mineral/Bağ Yapısı", "PIXL Işıma Rengi", "Analiz Notu")

the_table = ax2.table(cellText=table_data, 
                      colLabels=columns, 
                      cellColours=cell_colors, 
                      loc='center', 
                      cellLoc='center')

the_table.auto_set_font_size(False)
the_table.set_fontsize(11)
the_table.scale(1.2, 2.2) 

plt.tight_layout()
plt.show()