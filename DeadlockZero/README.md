# 🧬 Evolutionary Kernel: AI-Driven OS Scheduler

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Field](https://img.shields.io/badge/Field-Operating%20Systems%20%26%20AI-orange)

**Evolutionary Kernel**, modern işletim sistemi çekirdek mimarisini; **Olasılık Kuramı**, **Banker Algoritması** ve **Genetik Algoritmalar** ile optimize eden gelişmiş bir simülasyon projesidir.



## 🚀 Proje Özeti
Bu çalışma, bir bilgisayar sistemine gelen iş yükünü istatistiksel modellerle simüle eder, kilitlenme (deadlock) risklerini matematiksel olarak bertaraf eder ve işlemci kuyruğunu yapay zeka kullanarak optimize eder.

## 🛠️ Temel Modüller ve Teknolojiler

### 1. Olasılıksal İş Yükü Üreticisi (`generator.py`)
Sistem, deterministik veriler yerine gerçek dünya karmaşıklığını modelleyen **Monte Carlo** yaklaşımlarını kullanır:
* **Geliş Süreleri:** Poisson Süreci (Üstel Dağılım) kullanılarak modellenmiştir.
* **Kaynak Talepleri:** CPU ve RAM ihtiyaçları Normal (Gauss) Dağılım ile üretilir.

### 2. Güvenlik ve Kaynak Yönetimi (`banker_algorithm.py`)
Sistemin kararlılığını sağlamak için iki aşamalı bir denetim mekanizması bulunur:
* **RAM Denetimi:** Fiziksel bellek sınırları içerisinde süreç kabulü yapılır.
* **Banker Algoritması:** Kaynak tahsisinde kilitlenme (deadlock) oluşma ihtimali matris operasyonlarıyla önceden tespit edilir ve sadece "Safe State" (Güvenli Durum) onaylanır.



### 3. Yapay Zeka Destekli Çizelgeleyici (`genetic_scheduler.py`)
Kuyruktaki süreçlerin sıralanması bir **NP-Hard** problemidir. Bu modül, en kısa bekleme süresini bulmak için evrimsel bir yaklaşım sergiler:
* **Kodlama:** Her sıralama bir "Kromozom" olarak temsil edilir.
* **Operatörler:** Sıralı Çaprazlama (OX1) ve Mutasyon teknikleri kullanılır.
* **Optimizasyon:** Geleneksel FCFS (İlk Gelen İlk Hizmet Alır) yöntemine göre bekleme süresinde ciddi iyileştirme sağlar.



## 📊 Kurulum ve Kullanım

### Gereksinimler
Projenin çalışması için gerekli bilimsel kütüphaneler:
```bash
pip install numpy scipy matplotlib seaborn