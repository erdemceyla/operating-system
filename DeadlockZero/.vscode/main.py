import numpy as np
import random
import matplotlib.pyplot as plt

# Kendi yazdığımız modülleri içeri aktarıyoruz (Modüler Mimari)
from generator import generate_workload
from banker_algorithm import SystemManager
from genetic_scheduler import run_genetic_algorithm, calculate_waiting_time

if __name__ == "__main__":
    # Sonuçların her seferinde tutarlı olması için seed (tohum) ayarı
    np.random.seed(42)
    random.seed(42)
    
    # ==========================================
    # SİSTEM PARAMETRELERİ
    # ==========================================
    TOTAL_RAM = 4096                           # 4 GB Toplam RAM
    SYS_RESOURCES = [15, 10, 8]                # [Disk, Yazıcı, Ağ Portu] Kapasiteleri
    NUM_PROCESSES = 25                         # Sisteme gelecek toplam süreç sayısı
    
    print("="*60)
    print(" 🚀 İŞLETİM SİSTEMİ ÇEKİRDEK SİMÜLASYONU BAŞLIYOR ")
    print("="*60)
    
    # ==========================================
    # 1. AŞAMA: OLASILIKSAL YÜK ÜRETİMİ (generator.py)
    # ==========================================
    print("\n[1/3] Monte Carlo Olasılık Motoru ile süreçler üretiliyor...")
    raw_processes = generate_workload(
        n=NUM_PROCESSES, 
        lam=1.5, mu_burst=8.0, sig_burst=3.0, 
        mu_ram=500, sig_ram=200, max_resources=SYS_RESOURCES
    )
    print(f"      -> {NUM_PROCESSES} adet sanal süreç (Process) başarıyla üretildi.")
    
    # ==========================================
    # 2. AŞAMA: BANKER ALGORİTMASI VE RAM FİLTRESİ (banker_algorithm.py)
    # ==========================================
    print("\n[2/3] Banker Algoritması ile Kilitlenme (Deadlock) kontrolü yapılıyor...")
    os_manager = SystemManager(TOTAL_RAM, SYS_RESOURCES)
    ready_queue = [] # İşlemciye gitmeye hak kazanan güvenli süreçler
    
    for p in raw_processes:
        admitted, reason = os_manager.admit_process(p)
        if admitted:
            ready_queue.append(p)
        else:
            # RAM'e sığmayan veya sistemi kilitleyecek olanlar reddedilir
            print(f"      [REDDEDİLDİ] P{p.pid} -> Sebep: {reason}")
            
    print(f"      -> Sisteme Kabul Edilen Güvenli Süreç Sayısı: {len(ready_queue)} / {NUM_PROCESSES}")
    
    # ==========================================
    # 3. AŞAMA: YAPAY ZEKA İLE OPTİMİZASYON (genetic_scheduler.py)
    # ==========================================
    print("\n[3/3] Genetik Algoritma (GA) ile Kuyruk Optimizasyonu başlıyor...")
    
    # Önce standart yöntemin (Geliş sırasına göre - FCFS) skorunu bulalım
    fcfs_wait = calculate_waiting_time(ready_queue)
    print(f"      Standart FCFS (Geliş Sırası) Ortalama Bekleme Süresi: {fcfs_wait:.2f} ms")
    
    # Şimdi Yapay Zeka'ya en iyi sırayı bulduralım
    best_sequence, ga_history = run_genetic_algorithm(ready_queue, pop_size=50, generations=150, mutation_rate=0.15)
    ga_wait = calculate_waiting_time(best_sequence)
    
    print(f"      Genetik Algoritma (Optimize) Ortalama Bekleme Süresi: {ga_wait:.2f} ms")
    print(f"      İyileşme Oranı: %{((fcfs_wait - ga_wait) / fcfs_wait) * 100:.2f}")
    
    print(f"\n      🌟 Mükemmel Çalışma Sırası (Kromozom):")
    print("      " + " -> ".join([f"P{p.pid}" for p in best_sequence]))
    
    # ==========================================
    # 4. AŞAMA: SONUÇLARI GÖRSELLEŞTİRME
    # ==========================================
    plt.figure(figsize=(10, 5), constrained_layout=True)
    plt.plot(ga_history, color='teal', linewidth=2.5, label='GA Öğrenme Eğrisi (Evrim)')
    plt.axhline(y=fcfs_wait, color='red', linestyle='--', label='Geleneksel FCFS Skoru')
    
    plt.title('Yapay Zeka (Genetik Algoritma) ile OS Çizelgeleme Optimizasyonu', fontsize=14, fontweight='bold')
    plt.xlabel('Nesiller (Generations)', fontsize=12)
    plt.ylabel('Ortalama Bekleme Süresi (ms)\n[Daha düşük daha iyi]', fontsize=12)
    
    plt.legend(loc='upper right', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.savefig('final_simulation_result.png')
    print("\n✅ Simülasyon tamamlandı! Öğrenme grafiği ekranda açılıyor...")
    plt.show()