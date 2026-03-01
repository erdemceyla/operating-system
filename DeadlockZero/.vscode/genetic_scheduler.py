import random
import matplotlib.pyplot as plt

# ==========================================
# SÜREÇ (PROCESS) VERİ YAPISI
# ==========================================
class Process:
    """Sadece çizelgeleme için gereken temel süreç yapısı."""
    def __init__(self, pid, burst):
        self.pid = pid
        self.burst = burst # Sürecin CPU'da geçireceği zaman

    def __repr__(self):
        return f"P{self.pid}({self.burst}ms)"

# ==========================================
# GENETİK ALGORİTMA FONKSİYONLARI
# ==========================================
def calculate_waiting_time(sequence):
    """
    Verilen bir sürecin sıralamasına (kromozoma) göre ortalama bekleme süresini hesaplar.
    Her süreç, kendinden önceki süreçlerin toplam çalışma süresi kadar bekler.
    """
    waiting_time = 0
    total_waiting_time = 0
    
    for p in sequence[:-1]: # Son süreç hariç
        waiting_time += p.burst
        total_waiting_time += waiting_time
        
    return total_waiting_time / len(sequence)

def fitness(sequence):
    """
    Uygunluk fonksiyonu (Fitness Function).
    Bekleme süresi ne kadar düşükse, bu sıralamanın "hayatta kalma" şansı o kadar yüksektir.
    """
    avg_wait = calculate_waiting_time(sequence)
    # Sıfıra bölünme hatasını önlemek için küçük bir değer (1e-5) ekliyoruz
    return 1.0 / (avg_wait + 1e-5), avg_wait

def create_initial_population(processes, pop_size):
    """Rastgele sıralamalardan oluşan ilk nesli (popülasyonu) yaratır."""
    population = []
    for _ in range(pop_size):
        individual = processes.copy()
        random.shuffle(individual)
        population.append(individual)
    return population

def crossover(parent1, parent2):
    """
    Sıralı Çaprazlama (Order Crossover - OX1).
    Aynı sürecin kopyalanmasını veya bir sürecin unutulmasını engeller.
    """
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    child = [None] * size
    
    # 1. Ebeveyn 1'den genetik kesiti doğrudan al
    child[start:end] = parent1[start:end]
    
    # 2. Ebeveyn 2'deki eksik süreçleri sırayla doldur
    p2_idx = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_idx] in child:
                p2_idx += 1
            child[i] = parent2[p2_idx]
            
    return child

def mutate(sequence, mutation_rate=0.1):
    """
    Mutasyon: Rastgele iki sürecin yerini değiştirerek genetik çeşitlilik sağlar.
    Bu, algoritmanın yerel minimumlara (local minima) takılmasını önler.
    """
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(sequence)), 2)
        sequence[idx1], sequence[idx2] = sequence[idx2], sequence[idx1]
    return sequence

def run_genetic_algorithm(processes, pop_size=50, generations=100, mutation_rate=0.1):
    """Genetik Algoritma motorunu çalıştırır ve en iyi dizilimi döndürür."""
    if len(processes) <= 1:
        return processes, []

    population = create_initial_population(processes, pop_size)
    best_history = []
    
    for gen in range(generations):
        # 1. Popülasyonu uygunluk (fitness) değerine göre büyükten küçüğe sırala
        population.sort(key=lambda x: fitness(x)[0], reverse=True)
        
        # En iyi bireyin ortalama bekleme süresini kaydet (Grafik çizimi için)
        _, best_avg_wait = fitness(population[0])
        best_history.append(best_avg_wait)
        
        # 2. Seçilim (Elitizm): En iyi %20'yi doğrudan yeni nesle aktar ki iyi genler kaybolmasın
        next_generation = population[:int(pop_size * 0.2)]
        
        # 3. Çaprazlama ve Mutasyon ile yeni bireyler üret (Kalan %80'i doldur)
        while len(next_generation) < pop_size:
            # Sadece en iyi %50'lik dilimden ebeveyn seç (Doğal Seçilim)
            p1 = random.choice(population[:int(pop_size * 0.5)])
            p2 = random.choice(population[:int(pop_size * 0.5)])
            
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            next_generation.append(child)
            
        population = next_generation

    # Tüm nesiller bittikten sonra en iyi popülasyonu tekrar sırala ve 1. sıradakini ver
    population.sort(key=lambda x: fitness(x)[0], reverse=True)
    best_sequence = population[0]
    
    return best_sequence, best_history

# ==========================================
# TEST VE ÇALIŞTIRMA BLOĞU
# ==========================================
if __name__ == "__main__":
    # Testlerin her seferinde aynı sonucu vermesi için (İstersen kapatabilirsin)
    random.seed(42)
    
    # 1. Rastgele 20 süreç üretelim (İşlem süreleri 1 ile 30 ms arası olsun)
    NUM_PROCESSES = 20
    test_processes = [Process(i+1, random.randint(1, 30)) for i in range(NUM_PROCESSES)]
    
    print(f"--- {NUM_PROCESSES} SÜREÇ İÇİN GENETİK ALGORİTMA TESTİ ---")
    
    # 2. Geleneksel FCFS (Geliş Sırasına Göre) Bekleme Süresi
    fcfs_wait = calculate_waiting_time(test_processes)
    print(f"\n1. Standart FCFS Bekleme Süresi: {fcfs_wait:.2f} ms")
    
    # 3. Genetik Algoritmayı Çalıştır
    print("2. Genetik Algoritma Çalışıyor (50 Birey, 100 Nesil)...")
    best_seq, history = run_genetic_algorithm(
        test_processes, 
        pop_size=50, 
        generations=100, 
        mutation_rate=0.15
    )
    
    # 4. Sonuçları Görüntüle
    optimized_wait = calculate_waiting_time(best_seq)
    print(f"\n   GA Sonrası Optimize Bekleme Süresi: {optimized_wait:.2f} ms")
    print(f"   İyileşme Oranı: %{((fcfs_wait - optimized_wait) / fcfs_wait) * 100:.2f}")
    
    print("\nEn İyi Süreç Çalışma Sırası:")
    print(" -> ".join([f"P{p.pid}" for p in best_seq]))
    
    # 5. Görselleştirme
    plt.figure(figsize=(9, 5))
    plt.plot(history, color='#2ca02c', linewidth=2, label='GA Öğrenme Eğrisi')
    plt.axhline(y=fcfs_wait, color='#d62728', linestyle='--', label='Geleneksel FCFS')
    plt.title('Genetik Algoritma ile Görev Çizelgeleme Optimizasyonu', fontweight='bold')
    plt.xlabel('Nesiller (Generations)')
    plt.ylabel('Ortalama Bekleme Süresi (ms)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig('ga_standalone_test.png')
    plt.show()