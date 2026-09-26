#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
               VOID-SENTINEL v1.0 // UNIFIED DEFENSE ENGINE
====================================================================
Copyright (c) 2026 LENY. All Rights Reserved.
License: VOID-EX Open Source License v1.0
"""

import os
import sys
import math
import hashlib
import json
import ast
import platform
import psutil
import socket
import random
from datetime import datetime

# ====================================================================
# COLOR & FORMATTING UTILITIES
# ====================================================================
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_info(msg):
    print(f"{Colors.CYAN}[*] {msg}{Colors.END}")

def log_success(msg):
    print(f"{Colors.GREEN}[+] {msg}{Colors.END}")

def log_warn(msg):
    print(f"{Colors.YELLOW}[!] {msg}{Colors.END}")

def log_danger(msg):
    print(f"{Colors.RED}[CRITICAL] {msg}{Colors.END}")


# ====================================================================
# ENGINE 1: DFIR & SYSTEM TRIAGE MOTORU
# ====================================================================
class TriageEngine:
    @staticmethod
    def run_system_triage():
        log_info("Sistem Triage & Adli Bilişim Taraması Başlatılıyor...")
        
        info = {
            "timestamp": str(datetime.now()),
            "os": platform.system(),
            "release": platform.release(),
            "arch": platform.machine(),
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "active_processes": [],
            "listening_ports": []
        }
        
        # Süreç Taraması & SHA-256 Hash Alımı
        log_info("Çalışan süreçler ve hash değerleri analiz ediliyor...")
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                p_info = proc.info
                p_exe = p_info['exe']
                p_hash = "N/A"
                if p_exe and os.path.isfile(p_exe):
                    hasher = hashlib.sha256()
                    with open(p_exe, 'rb') as f:
                        hasher.update(f.read(4096))
                    p_hash = hasher.hexdigest()
                
                info["active_processes"].append({
                    "pid": p_info['pid'],
                    "name": p_info['name'],
                    "hash": p_hash
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Ağ Soketleri Taraması
        log_info("Açık ağ soketleri ve bağlantılar taranıyor...")
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                info["listening_ports"].append({
                    "fd": conn.fd,
                    "laddr": f"{conn.laddr.ip}:{conn.laddr.port}",
                    "pid": conn.pid
                })

        log_success(f"Triage Tamamlandı! Toplam Süreç: {len(info['active_processes'])}, Dinlenen Port: {len(info['listening_ports'])}")
        return info


# ====================================================================
# ENGINE 2: NET TRAFFIC & SHANNON ENTROPY MOTORU
# ====================================================================
class NetworkEntropyEngine:
    @staticmethod
    def calculate_entropy(data: bytes) -> float:
        """Shannon Entropi Algoritması: H(X) = -sum(P(x) * log2(P(x)))"""
        if not data:
            return 0.0
        entropy = 0
        for x in range(256):
            p_x = data.count(bytes([x])) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log2(p_x)
        return entropy

    @classmethod
    def analyze_payload_entropy(cls, payload: bytes):
        score = cls.calculate_entropy(payload)
        status = "Normal Metin / Düzenli Veri"
        if score > 7.2:
            status = "Yüksek Entropi (Şifrelenmiş veya Sıkıştırılmış Tünelleme Verisi!)"
        elif score > 5.0:
            status = "Orta Entropi (Karmaşık Veri / Kod)"

        return {
            "bytes_length": len(payload),
            "entropy_score": round(score, 4),
            "assessment": status
        }


# ====================================================================
# ENGINE 3: SHAMIR SECRET SHARING & CASCADE KRİPTOGRAFİ MOTORU
# ====================================================================
class ShamirSecretVault:
    _PRIME = 2**127 - 1  # Mersenne Prime for Galois Field operations

    @classmethod
    def _eval_at(cls, poly, x):
        accum = 0
        for coeff in reversed(poly):
            accum = (accum * x + coeff) % cls._PRIME
        return accum

    @classmethod
    def split_secret(cls, secret_int: int, threshold: int, num_shares: int):
        """Gizli anahtarı N parçaya böler, çözmek için K kadarı gerekir."""
        if threshold > num_shares:
            raise ValueError("Eşik değeri toplam parça sayısından büyük olamaz.")
        
        poly = [secret_int] + [random.randint(1, cls._PRIME - 1) for _ in range(threshold - 1)]
        shares = []
        for i in range(1, num_shares + 1):
            shares.append((i, cls._eval_at(poly, i)))
        return shares

    @classmethod
    def recover_secret(cls, shares):
        """Lagrange İnterpolasyonu ile gizli anahtarı yeniden birleştirir."""
        def _extended_gcd(a, b):
            if b == 0: return a, 1, 0
            g, x, y = _extended_gcd(b, a % b)
            return g, y, x - (a // b) * y

        def _mod_inverse(k):
            _, x, _ = _extended_gcd(k, cls._PRIME)
            return (x % cls._PRIME + cls._PRIME) % cls._PRIME

        k = len(shares)
        xs, ys = zip(*shares)
        secret = 0
        for i in range(k):
            numerator, denominator = 1, 1
            for j in range(k):
                if i != j:
                    numerator = (numerator * (-xs[j])) % cls._PRIME
                    denominator = (denominator * (xs[i] - xs[j])) % cls._PRIME
            lagrange_coeff = (numerator * _mod_inverse(denominator)) % cls._PRIME
            secret = (secret + ys[i] * lagrange_coeff) % cls._PRIME
        return secret


# ====================================================================
# ENGINE 4: SAST & STATİK KOD ENTROPİ DENETÇİSİ
# ====================================================================
class SASTEngine:
    UNSAFE_FUNCTIONS = {'eval', 'exec', 'system', 'popen'}

    @classmethod
    def audit_python_file(cls, filepath: str):
        log_info(f"Kod Güvenlik Analizi Yapılıyor: {filepath}")
        if not os.path.exists(filepath):
            log_danger("Dosya bulunamadı!")
            return None

        issues = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()

        # AST Sözdizim Ağacı Analizi
        try:
            tree = ast.parse(code, filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in cls.UNSAFE_FUNCTIONS:
                        issues.append({
                            "line": node.lineno,
                            "type": "Unsafe Function Call",
                            "detail": f"Riskli fonksiyon kullanımı tespit edildi: {node.func.id}()"
                        })
        except Exception as e:
            issues.append({"line": 0, "type": "Parse Error", "detail": str(e)})

        # Entropi Tabanlı Gizli Anahtar Taraması (Hardcoded Secrets/Tokens)
        for idx, line in enumerate(code.splitlines(), 1):
            for word in line.split():
                if len(word) > 20:
                    ent = NetworkEntropyEngine.calculate_entropy(word.encode('utf-8'))
                    if ent > 4.5:
                        issues.append({
                            "line": idx,
                            "type": "High Entropy String Leak",
                            "detail": f"Unutulmuş API Key / Token Şüphesi (Entropi: {round(ent, 2)})"
                        })

        log_success(f"SAST Analizi Tamamlandı! Bulunan Risk Sayısı: {len(issues)}")
        return issues


# ====================================================================
# UNIFIED INTERACTIVE CONSOLE
# ====================================================================
def banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
   ██╗   ██╗███╗   ██╗██╗██████╗     ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
   ██║   ██║████╗  ██║██║██╔══██╗    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
   ██║   ██║██╔██╗ ██║██║██║  ██║    ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
   ╚██╗ ██╔╝██║╚██╗██║██║██║  ██║    ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
    ╚████╔╝ ██║ ╚████║██║██████╔╝    ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
     ╚═══╝  ╚═╝  ╚═══╝╚═╝╚═════╝     ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
                            [ UNIFIED DEFENSE & FORENSIC ENGINE v1.0 ]
    {Colors.END}""")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    while True:
        print(f"\n{Colors.BOLD}=== ANA KONTROL PANELİ ==={Colors.END}")
        print("1. [DFIR Engine]  Sistem Triage & Adli Bilişim Taraması")
        print("2. [NET Engine]   Veri / Paket Entropi Analizi")
        print("3. [CRYPT Vault]  Shamir Secret Sharing Anahtar Bölümleme & Kurtarma")
        print("4. [SAST Engine]  Statik Kod Güvenlik & Gizli Anahtar Analizi")
        print("5. [Full Suite]   Tüm Sistem Motorlarını Sırayla Çalıştır ve Raporla")
        print("0. Çıkış")
        
        choice = input(f"\n{Colors.CYAN}VOID-SENTINEL > {Colors.END}").strip()

        if choice == '1':
            data = TriageEngine.run_system_triage()
            with open("triage_report.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            log_success("Rapor 'triage_report.json' dosyasına yazıldı.")

        elif choice == '2':
            text = input("Analiz edilecek veriyi girin: ").encode('utf-8')
            res = NetworkEntropyEngine.analyze_payload_entropy(text)
            print(json.dumps(res, indent=4, ensure_ascii=False))

        elif choice == '3':
            sec = int(input("Gizli Sayısal Anahtar (Örn: 123456789): "))
            n = int(input("Toplam Parça Sayısı (N): "))
            k = int(input("Kurtarma İçin Gerekli Eşik Sayı (K): "))
            shares = ShamirSecretVault.split_secret(sec, k, n)
            log_success(f"Oluşturulan {n} Parça:")
            for s in shares:
                print(f"  Parça {s[0]}: {s[1]}")
            
            log_info(f"Rastgele {k} parça kullanılarak anahtar geri birleştiriliyor...")
            selected = shares[:k]
            recovered = ShamirSecretVault.recover_secret(selected)
            log_success(f"Kurtarılan Anahtar: {recovered}")

        elif choice == '4':
            path = input("Taranacak Python Dosya Yolu: ").strip()
            issues = SASTEngine.audit_python_file(path)
            if issues:
                print(json.dumps(issues, indent=4, ensure_ascii=False))

        elif choice == '5':
            log_info("Tam Tarama Modu Başlatıldı...")
            t_data = TriageEngine.run_system_triage()
            log_success("Sistem Triage Tamam.")
            
            s_issues = SASTEngine.audit_python_file(__file__)
            log_success("Sözdizim Taraması Tamam.")

            full_report = {
                "triage": t_data,
                "sast_self_check": s_issues
            }
            with open("full_sentinel_report.json", "w", encoding="utf-8") as f:
                json.dump(full_report, f, indent=4, ensure_ascii=False)
            log_success("Tüm rapor 'full_sentinel_report.json' olarak kaydedildi.")

        elif choice == '0':
            log_info("VOID-SENTINEL kapatılıyor. Güvenli günler!")
            sys.exit(0)
        else:
            log_warn("Geçersiz seçim, tekrar deneyin.")

if __name__ == "__main__":
    main()
