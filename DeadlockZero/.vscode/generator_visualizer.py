import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from generator import generate_workload, Process

NP = 200
LAMBDA_ARRIVAL = 1.8   
MU_BURST = 7.0         
SIGMA_BURST = 2.5      
MU_RAM = 450           
SIGMA_RAM = 180        
SYSTEM_RESOURCES = [15, 10, 8] 

print(f"{NP} adet süreç olasılıksal modelle üretiliyor ve görselleştiriliyor...")
processes = generate_workload(NP, LAMBDA_ARRIVAL, MU_BURST, SIGMA_BURST, 
                              MU_RAM, SIGMA_RAM, SYSTEM_RESOURCES)

arrival_times = [p.arrival for p in processes]
burst_times = [p.burst for p in processes]
ram_reqs = [p.ram_req for p in processes]
inter_arrival_times = np.diff(arrival_times)

# YENİ EKLENEN KISIM: constrained_layout=True ve figsize(13, 8)
fig, axs = plt.subplots(2, 2, figsize=(13, 8), constrained_layout=True)
fig.suptitle('İstatistiksel İş Yükü Profili', fontsize=16, fontweight='bold')

sns.histplot(burst_times, kde=True, color='#2ca02c', ax=axs[0, 0], stat="density")
axs[0, 0].set_title(fr'CPU İşlem Süreleri (Normal Dağılım: $\mu$={MU_BURST}, $\sigma$={SIGMA_BURST})')
axs[0, 0].set_xlabel('Zaman (ms)')
axs[0, 0].set_ylabel('Yoğunluk (Density)')
axs[0, 0].grid(axis='y', linestyle='--', alpha=0.5)

sns.histplot(ram_reqs, kde=True, color='#1f77b4', ax=axs[0, 1], stat="density")
axs[0, 1].set_title(fr'RAM İhtiyaçları (Normal Dağılım: $\mu$={MU_RAM}, $\sigma$={SIGMA_RAM})')
axs[0, 1].set_xlabel('Bellek (MB)')
axs[0, 1].set_ylabel('Yoğunluk (Density)')
axs[0, 1].grid(axis='y', linestyle='--', alpha=0.5)

sns.histplot(inter_arrival_times, kde=True, color='#d62728', ax=axs[1, 0], stat="density")
axs[1, 0].set_title(fr'Gelişler Arası Süreler (Poisson/Üstel Dağılım: $\lambda$={LAMBDA_ARRIVAL})')
axs[1, 0].set_xlabel('Süre (ms)')
axs[1, 0].set_ylabel('Yoğunluk (Density)')
axs[1, 0].grid(axis='y', linestyle='--', alpha=0.5)

axs[1, 1].plot(arrival_times, np.arange(1, NP+1), color='purple', linewidth=2)
axs[1, 1].set_title(f'Zamanla Birikimli Süreç Gelişleri (Poisson: {LAMBDA_ARRIVAL} süreç/ms)')
axs[1, 1].set_xlabel('Zaman (ms)')
axs[1, 1].set_ylabel('Toplam Süreç Sayısı')
axs[1, 1].grid(True, linestyle='--', alpha=0.5)

# tight_layout'u sildik çünkü yukarıda constrained_layout=True kullandık.
plt.savefig('statistical_workload_profile.png')
plt.show()