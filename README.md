# VOID-SENTINEL

██╗   ██╗███╗   ██╗██╗██████╗     ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██║   ██║████╗  ██║██║██╔══██╗    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
██║   ██║██╔██╗ ██║██║██║  ██║    ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
╚██╗ ██╔╝██║╚██╗██║██║██║  ██║    ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
╚████╔╝ ██║ ╚████║██║██████╔╝    ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚═══╝  ╚═╝  ╚═══╝╚═╝╚═════╝     ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝

> **[ APEX CORE v1.0 // Operator: LENY // Framework Standard: Enterprise ]**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/PLATFORM-Linux%20%7C%20Windows%20%7C%20WSL2-brightgreen.svg)
![Security](https://img.shields.io/badge/SECURITY-AES--256%20%7C%20PBKDF2-red.svg)

Siber güvenlik, adli bilişim (DFIR), kriptografi ve ağ analizi için geliştirilmiş üst düzey operasyonel terminal framework'ü.

---

## 🚀 Özellikler & Operasyon Modülleri

* **[1] DFIR & Sistem Triage Motoru (SystemTriage):**
  * Çalışan aktif süreçlerin tespiti ve SHA-256 dosya doğrulama kontrolü.
  * Sistem CPU/RAM kullanım analizi ve açık listening ağ portlarının adli incelemesi.
  * Triage sonuçlarının otomatik `.json` formatında adli rapor haline getirilmesi.

* **[2] Shannon Entropi & Paket Analiz Motoru (EntropyNet):**
  * Veri akışları, ağ paketleri veya metinler üzerinde Shannon Entropisi hesabı.
  * Yüksek entropili şifrelenmiş tünelleme trafiği veya zararlı yazılım payload tespiti.

* **[3] Kriptografik Vault & Shamir Secret Sharing (CryptVault):**
  * Galois Field altyapısıyla Shamir'in Gizli Paylaşım algoritması.
  * Hassas sistem anahtarlarını N parçaya bölme ve K eşik parçayla (Threshold Recovery) kayıpsız geri birleştirme.

* **[4] SAST & Statik Kod Güvenlik Denetçisi (CodeAudit):**
  * AST (Abstract Syntax Tree) ile Python kodlarında tehlikeli fonksiyon (`eval`, `exec`, `system`) analizi.
  * Kod satırlarında unutulmuş yüksek entropili API Key, JWT ve Token sızıntı taraması.

---

## 💻 Linux / Windows / WSL2 Kurulumu

### 1. Bağımlılıkları Yükleyin:
```bash
sudo apt update && sudo apt install python3 git -y
pip install psutil


