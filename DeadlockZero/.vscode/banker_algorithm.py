import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# GÜVENLİK VE KAYNAK YÖNETİCİSİ (BANKER ALGORİTMASI)
# ==========================================
class SystemManager:
    """
    İşletim sisteminin RAM ve Donanım kaynaklarını yöneten sınıf.
    Kilitlenmeleri (Deadlock) önlemek için Banker Algoritmasını kullanır.
    """
    def __init__(self, total_ram, total_resources):
        # RAM Yönetimi
        self.total_ram = total_ram
        self.available_ram = total_ram
        
        # Donanım Yönetimi (Vektör şeklinde: Örn. [10 Disk, 5 Yazıcı, 8 Port])
        self.total_resources = np.array(total_resources)
        self.available_resources = np.array(total_resources)
        
        # Banker Algoritması Matrisleri ve Takip
        self.admitted_pids = [] # Kabul edilen süreçlerin ID'leri
        self.allocation = []    # Şu an süreçlere verilmiş kaynaklar
        self.need = []          # Süreçlerin işi bitirmek için ihtiyaç duyduğu ekstra kaynaklar

    def is_safe(self, test_available, test_allocation, test_need):
        """Banker Algoritması Güvenlik Kontrolü"""
        num_procs = len(test_allocation)
        if num_procs == 0: 
            return True
            
        work = test_available.copy()
        finish = [False] * num_procs
        
        count = 0
        while count < num_procs:
            found = False
            for p in range(num_procs):
                if not finish[p] and np.all(test_need[p] <= work):
                    work += test_allocation[p]
                    finish[p] = True
                    found = True
                    count += 1
            if not found:
                return False 
        return True

    def admit_process(self, process):
        """Gelen bir süreci RAM ve Banker kontrolünden geçirir."""
        if process.ram_req > self.available_ram:
            return False, f"Yetersiz RAM (İstenen: {process.ram_req}MB, Boş: {self.available_ram}MB)"
            
        test_available = self.available_resources - process.resource_req
        if np.any(test_available < 0):
            return False, "Yetersiz Donanım Kaynağı"
            
        test_allocation = self.allocation + [process.resource_req]
        test_need = self.need + [np.zeros_like(process.resource_req)] 
        
        if self.is_safe(test_available, test_allocation, test_need):
            self.available_ram -= process.ram_req
            self.available_resources -= process.resource_req
            self.allocation.append(process.resource_req)
            self.need.append(np.zeros_like(process.resource_req))
            self.admitted_pids.append(process.pid) # Çizim için PID'yi kaydet
            return True, "Güvenli ve Onaylandı"
        else:
            return False, "Deadlock Riski Tespit Edildi"

    def visualize_state(self):
        """İşletim sisteminin anlık kaynak dağılımını görselleştirir."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 1. Grafik: RAM Kullanımı (Pasta Grafiği)
        used_ram = self.total_ram - self.available_ram
        ax1.pie([used_ram, self.available_ram], labels=['Kullanılan RAM', 'Boş RAM'], 
                autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=90, explode=(0.1, 0))
        ax1.set_title(f"Sistem RAM Durumu\n(Toplam: {self.total_ram} MB)")

        # 2. Grafik: Donanım Kaynakları (Yığılmış Bar Grafiği - Stacked Bar)
        num_res = len(self.total_resources)
        ind = np.arange(num_res)
        width = 0.5
        
        used_resources = self.total_resources - self.available_resources
        
        p1 = ax2.bar(ind, used_resources, width, color='#ffcc99', label='Tahsis Edilen (Allocated)')
        p2 = ax2.bar(ind, self.available_resources, width, bottom=used_resources, color='#99ff99', label='Boşta (Available)')
        
        ax2.set_ylabel('Birim Sayısı')
        ax2.set_title('Donanım Kaynakları Dağılımı\n(Örn: R1=Disk, R2=Yazıcı, R3=Ağ)')
        ax2.set_xticks(ind)
        ax2.set_xticklabels([f'Kaynak {i+1}' for i in range(num_res)])
        ax2.legend()

        plt.tight_layout()
        plt.savefig('banker_state_dashboard.png')
        plt.show()

# ==========================================
# BAĞIMSIZ TEST BLOĞU
# ==========================================
if __name__ == "__main__":
    class MockProcess:
        def __init__(self, pid, ram_req, res_req):
            self.pid = pid
            self.ram_req = ram_req
            self.resource_req = np.array(res_req)

    print("--- BANKER ALGORİTMASI GÖRSELLEŞTİRME TESTİ ---")
    os_manager = SystemManager(total_ram=2048, total_resources=[15, 10, 8])
    
    # Sisteme rastgele süreçler sokalım
    processes_to_test = [
        MockProcess(1, 512, [3, 2, 2]),
        MockProcess(2, 256, [5, 1, 3]),
        MockProcess(3, 800, [2, 4, 1]),
        MockProcess(4, 1024, [6, 4, 4]), # Bu büyük ihtimalle reddedilecek (RAM/Deadlock)
        MockProcess(5, 128, [1, 1, 1])
    ]

    for p in processes_to_test:
        admitted, reason = os_manager.admit_process(p)
        durum = "KABUL" if admitted else "RED"
        print(f"P{p.pid} -> {durum} ({reason})")

    print("\nGörsel Dashboard oluşturuluyor...")
    
    
    
    # Görselleştirme fonksiyonunu çağır
    os_manager.visualize_state()