import os
import sys
import time
import requests
import aiohttp
import asyncio
import json
from colorama import Fore, Style, init
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import choice, shuffle, sample
import webbrowser
from datetime import datetime
from tqdm import tqdm
import math
import backoff
import socket
from typing import List, Dict, Tuple, Optional, Union
import ipaddress
import re

# `colorama`'yı başlatıyoruz
init(autoreset=True)

class ProxyManager:
    def __init__(self):
        self.working_proxies = {
            'http': [],
            'socks4': [],
            'socks5': []
        }
        self.working_proxies_file = "calisan_proxyler.txt"
        self.hidemy_io_file = "hidemy_io_format.txt"
        self.stats = {
            'total_tested': 0,
            'working_count': 0,
            'start_time': datetime.now(),
            'current_scan': {
                'total': 0,
                'scanned': 0,
                'working': 0,
                'failed': 0
            }
        }
        self.geoip_cache = {}
        
        # Coğrafi konum veritabanı (genişletilmiş versiyon)
        self.country_codes = {
            'US': 'United States', 'DE': 'Germany', 'FR': 'France', 
            'GB': 'United Kingdom', 'NL': 'Netherlands', 'RU': 'Russia',
            'JP': 'Japan', 'CA': 'Canada', 'TR': 'Turkey', 'BR': 'Brazil',
            'CN': 'China', 'IN': 'India', 'AU': 'Australia', 'IT': 'Italy',
            'ES': 'Spain', 'SE': 'Sweden', 'CH': 'Switzerland', 'NO': 'Norway',
            'DK': 'Denmark', 'FI': 'Finland', 'PL': 'Poland', 'UA': 'Ukraine',
            'SG': 'Singapore', 'HK': 'Hong Kong', 'KR': 'South Korea', 'TW': 'Taiwan',
            'TH': 'Thailand', 'VN': 'Vietnam', 'ID': 'Indonesia', 'MY': 'Malaysia',
            'PH': 'Philippines', 'SA': 'Saudi Arabia', 'AE': 'United Arab Emirates',
            'IL': 'Israel', 'EG': 'Egypt', 'ZA': 'South Africa', 'NG': 'Nigeria',
            'MX': 'Mexico', 'AR': 'Argentina', 'CL': 'Chile', 'CO': 'Colombia',
            'PE': 'Peru', 'VE': 'Venezuela', 'PT': 'Portugal', 'GR': 'Greece',
            'CZ': 'Czech Republic', 'HU': 'Hungary', 'RO': 'Romania', 'BG': 'Bulgaria',
            'RS': 'Serbia', 'HR': 'Croatia', 'SK': 'Slovakia', 'SI': 'Slovenia',
            'AT': 'Austria', 'BE': 'Belgium', 'IE': 'Ireland', 'LU': 'Luxembourg',
            'IS': 'Iceland', 'EE': 'Estonia', 'LV': 'Latvia', 'LT': 'Lithuania',
            'MT': 'Malta', 'CY': 'Cyprus', 'GE': 'Georgia', 'AZ': 'Azerbaijan',
            'AM': 'Armenia', 'KZ': 'Kazakhstan', 'UZ': 'Uzbekistan', 'PK': 'Pakistan',
            'BD': 'Bangladesh', 'LK': 'Sri Lanka', 'NP': 'Nepal', 'IR': 'Iran',
            'IQ': 'Iraq', 'SY': 'Syria', 'JO': 'Jordan', 'LB': 'Lebanon', 'KW': 'Kuwait',
            'QA': 'Qatar', 'OM': 'Oman', 'YE': 'Yemen', 'BH': 'Bahrain', 'AF': 'Afghanistan',
            'MN': 'Mongolia', 'KH': 'Cambodia', 'LA': 'Laos', 'MM': 'Myanmar', 'BT': 'Bhutan',
            'MV': 'Maldives', 'BN': 'Brunei', 'TP': 'East Timor', 'PG': 'Papua New Guinea',
            'FJ': 'Fiji', 'NC': 'New Caledonia', 'PF': 'French Polynesia', 'NZ': 'New Zealand',
            'CR': 'Costa Rica', 'PA': 'Panama', 'DO': 'Dominican Republic', 'CU': 'Cuba',
            'JM': 'Jamaica', 'HT': 'Haiti', 'TT': 'Trinidad and Tobago', 'BO': 'Bolivia',
            'EC': 'Ecuador', 'PY': 'Paraguay', 'UY': 'Uruguay', 'GY': 'Guyana', 'SR': 'Suriname',
            'GF': 'French Guiana', 'NI': 'Nicaragua', 'SV': 'El Salvador', 'HN': 'Honduras',
            'GT': 'Guatemala', 'BZ': 'Belize', 'BS': 'Bahamas', 'BB': 'Barbados', 'LC': 'Saint Lucia',
            'VC': 'Saint Vincent and the Grenadines', 'GD': 'Grenada', 'AG': 'Antigua and Barbuda',
            'DM': 'Dominica', 'KN': 'Saint Kitts and Nevis', 'WS': 'Samoa', 'TO': 'Tonga',
            'VU': 'Vanuatu', 'SB': 'Solomon Islands', 'KI': 'Kiribati', 'TV': 'Tuvalu',
            'FM': 'Micronesia', 'MH': 'Marshall Islands', 'PW': 'Palau', 'CK': 'Cook Islands',
            'NU': 'Niue', 'WF': 'Wallis and Futuna', 'AS': 'American Samoa', 'GU': 'Guam',
            'MP': 'Northern Mariana Islands', 'PR': 'Puerto Rico', 'VI': 'U.S. Virgin Islands',
            'KY': 'Cayman Islands', 'BM': 'Bermuda', 'AI': 'Anguilla', 'VG': 'British Virgin Islands',
            'MS': 'Montserrat', 'TC': 'Turks and Caicos Islands', 'FK': 'Falkland Islands',
            'GI': 'Gibraltar', 'AD': 'Andorra', 'MC': 'Monaco', 'SM': 'San Marino', 'VA': 'Vatican City',
            'LI': 'Liechtenstein', 'FO': 'Faroe Islands', 'GL': 'Greenland', 'SJ': 'Svalbard and Jan Mayen',
            'AX': 'Åland Islands', 'ME': 'Montenegro', 'XK': 'Kosovo', 'PS': 'Palestine',
            'EH': 'Western Sahara', 'CF': 'Central African Republic', 'CG': 'Congo',
            'CD': 'DR Congo', 'DJ': 'Djibouti', 'ER': 'Eritrea', 'ET': 'Ethiopia',
            'KE': 'Kenya', 'MG': 'Madagascar', 'MW': 'Malawi', 'MU': 'Mauritius',
            'YT': 'Mayotte', 'MZ': 'Mozambique', 'RE': 'Réunion', 'RW': 'Rwanda',
            'SC': 'Seychelles', 'SO': 'Somalia', 'SS': 'South Sudan', 'SD': 'Sudan',
            'TZ': 'Tanzania', 'UG': 'Uganda', 'ZM': 'Zambia', 'ZW': 'Zimbabwe',
            'DZ': 'Algeria', 'AO': 'Angola', 'BJ': 'Benin', 'BW': 'Botswana',
            'BF': 'Burkina Faso', 'BI': 'Burundi', 'CM': 'Cameroon', 'CV': 'Cape Verde',
            'TD': 'Chad', 'KM': 'Comoros', 'CI': 'Côte d'Ivoire', 'GQ': 'Equatorial Guinea',
            'GA': 'Gabon', 'GM': 'Gambia', 'GH': 'Ghana', 'GN': 'Guinea', 'GW': 'Guinea-Bissau',
            'LR': 'Liberia', 'LY': 'Libya', 'ML': 'Mali', 'MR': 'Mauritania', 'MA': 'Morocco',
            'NE': 'Niger', 'SN': 'Senegal', 'SL': 'Sierra Leone', 'TG': 'Togo', 'TN': 'Tunisia'
        }
    
    @backoff.on_exception(backoff.expo, 
                         (requests.exceptions.RequestException, 
                          requests.exceptions.Timeout,
                          socket.gaierror),
                         max_tries=3,
                         max_time=30)
    def send_request(self, url: str, retries: int = 3) -> Optional[str]:
        """Verilen URL'ye HTTP GET isteği gönderir ve dönen içeriği alır. Hata durumunda tekrar dener."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except (requests.exceptions.RequestException, 
                requests.exceptions.Timeout,
                socket.gaierror) as e:
            if retries > 0:
                print(f"{Fore.YELLOW}⏳ {retries} deneme kaldı. 2 saniye bekleniyor...{Style.RESET_ALL}")
                time.sleep(2)
                return self.send_request(url, retries - 1)
            else:
                print(f"{Fore.RED}❌ İstek başarısız: {e}{Style.RESET_ALL}")
                return None

    async def test_proxy_async(self, session: aiohttp.ClientSession, proxy: str, proxy_type: str) -> Optional[Dict]:
        """Proxy'yi asenkron olarak test eder."""
        try:
            proxies = f"{proxy_type}://{proxy}"
            
            # Test siteleri
            test_urls = [
                "https://httpbin.org/ip",
                "https://api.ipify.org?format=json",
                "https://ident.me"
            ]
            
            # Rastgele 2 farklı site ile test et
            test_sites = sample(test_urls, 2)
            success_count = 0
            response_time = 0
            
            for test_url in test_sites:
                try:
                    start_time = time.time()
                    async with session.get(test_url, proxy=proxies, timeout=8) as response:
                        if response.status == 200:
                            success_count += 1
                            response_time = time.time() - start_time
                except:
                    continue
            
            # 2 testten en az 1'inde başarılı olmalı
            if success_count >= 1:
                # Coğrafi konum bilgisini al
                country = await self.get_proxy_country(session, proxy, proxy_type)
                
                proxy_data = {
                    'proxy': proxy,
                    'type': proxy_type,
                    'response_time': response_time,
                    'country': country,
                    'tested_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'score': self.calculate_proxy_score(response_time, country)
                }
                
                return proxy_data
            else:
                return None
                
        except Exception:
            return None

    async def get_proxy_country(self, session: aiohttp.ClientSession, proxy: str, proxy_type: str) -> str:
        """Proxy'nin coğrafi konumunu belirler."""
        try:
            ip = proxy.split(':')[0]
            
            # Önbellekte varsa kullan
            if ip in self.geoip_cache:
                return self.geoip_cache[ip]
            
            # IP'yi doğrula
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                return "Unknown"
            
            # IP-API servisini kullan
            proxies = f"{proxy_type}://{proxy}"
            url = f"http://ip-api.com/json/{ip}?fields=countryCode"
            
            try:
                async with session.get(url, proxy=proxies, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        country_code = data.get('countryCode', 'Unknown')
                        country_name = self.country_codes.get(country_code, country_code)
                        self.geoip_cache[ip] = country_name
                        return country_name
            except:
                pass
            
            return "Unknown"
        except:
            return "Unknown"

    def calculate_proxy_score(self, response_time: float, country: str) -> int:
        """Proxy için bir kalite puanı hesaplar (1-100 arası)."""
        # Yanıt süresine göre puan (ne kadar hızlıysa o kadar iyi)
        time_score = max(0, 100 - (response_time * 20))
        
        # Ülkeye göre puan (belirli ülkeler daha yüksek puan alır)
        country_score = 50  # Varsayılan puan
        
        premium_countries = ['United States', 'Germany', 'United Kingdom', 'Netherlands', 'Japan']
        if country in premium_countries:
            country_score = 90
        elif country != "Unknown":
            country_score = 70
        
        # Nihai puan (ağırlıklı ortalama)
        final_score = int((time_score * 0.7) + (country_score * 0.3))
        return min(100, max(1, final_score))

    async def test_all_proxies_async(self, proxy_list: List[str], proxy_type: str, max_workers: int = 20) -> None:
        """Tüm proxy'leri asenkron olarak test eder."""
        print(f"\n{Fore.YELLOW}🔍 {proxy_type.upper()} proxy'leri test ediliyor... ({len(proxy_list)} adet){Style.RESET_ALL}")
        
        # İstatistikleri sıfırla
        self.stats['current_scan']['total'] = len(proxy_list)
        self.stats['current_scan']['scanned'] = 0
        self.stats['current_scan']['working'] = 0
        self.stats['current_scan']['failed'] = 0
        
        # İlerleme çubuğu oluştur
        with tqdm(total=len(proxy_list), desc=f"{proxy_type.upper()} Tarama", 
                 bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}",
                 unit="proxy", ncols=80) as pbar:
            
            connector = aiohttp.TCPConnector(limit=max_workers, limit_per_host=5)
            timeout = aiohttp.ClientTimeout(total=10, sock_connect=5, sock_read=5)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                for proxy in proxy_list:
                    task = asyncio.create_task(self.test_proxy_async(session, proxy, proxy_type))
                    tasks.append(task)
                
                for future in asyncio.as_completed(tasks):
                    result = await future
                    self.stats['current_scan']['scanned'] += 1
                    
                    if result:
                        self.working_proxies[proxy_type].append(result)
                        self.stats['working_count'] += 1
                        self.stats['current_scan']['working'] += 1
                    else:
                        self.stats['current_scan']['failed'] += 1
                    
                    # İlerleme çubuğunu güncelle
                    pbar.set_postfix_str(f"✅{self.stats['current_scan']['working']} ❌{self.stats['current_scan']['failed']}")
                    pbar.update(1)
        
        print(f"\n{Fore.GREEN}✅ {proxy_type.upper()} testi tamamlandı. Çalışan proxy: {len(self.working_proxies[proxy_type])}/{len(proxy_list)}{Style.RESET_ALL}")

    def test_all_proxies(self, proxy_list: List[str], proxy_type: str, max_workers: int = 15) -> None:
        """Tüm proxy'leri paralel olarak test eder (senkron versiyon)."""
        # Asenkron fonksiyonu çalıştır
        asyncio.run(self.test_all_proxies_async(proxy_list, proxy_type, max_workers))

    def save_working_proxies(self) -> None:
        """Çalışan proxy'leri dosyaya kaydeder ve hidemy.io için özel format oluşturur."""
        if not any(self.working_proxies.values()):
            print(f"{Fore.YELLOW}⚠️ Kaydedilecek çalışan proxy bulunamadı.{Style.RESET_ALL}")
            return
        
        try:
            # Normal kayıt
            with open(self.working_proxies_file, 'w', encoding='utf-8') as f:
                f.write("# ÇALIŞAN PROXY LİSTESİ\n")
                f.write(f"# Oluşturulma tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Toplam test edilen: {self.stats['total_tested']}\n")
                f.write(f"# Çalışan proxy sayısı: {self.stats['working_count']}\n")
                f.write(f"# Test süresi: {(datetime.now() - self.stats['start_time']).total_seconds():.2f} saniye\n\n")
                
                # Tablo başlığı
                f.write(f"{'IP address':<20} {'Port':<8} {'Type':<8} {'Speed':<8} {'Country':<15} {'Score':<6}\n")
                f.write("-" * 70 + "\n")
                
                for proxy_type, proxies in self.working_proxies.items():
                    if proxies:
                        f.write(f"\n# {proxy_type.upper()} PROXY'LERİ ({len(proxies)} adet)\n")
                        # Proxy'leri puanına göre sırala (en yüksek puanlılar üstte)
                        sorted_proxies = sorted(proxies, key=lambda x: x['score'], reverse=True)
                        for proxy_data in sorted_proxies:
                            ip, port = proxy_data['proxy'].split(':')
                            speed = f"{proxy_data['response_time']:.2f}s"
                            f.write(f"{ip:<20} {port:<8} {proxy_data['type']:<8} {speed:<8} {proxy_data['country'][:15]:<15} {proxy_data['score']:<6}\n")
            
            print(f"{Fore.GREEN}✅ Çalışan proxy'ler '{self.working_proxies_file}' dosyasına kaydedildi.{Style.RESET_ALL}")
            
            # Hidemy.io için özel format
            with open(self.hidemy_io_file, 'w', encoding='utf-8') as f:
                f.write("# Hidemy.io için proxy listesi\n")
                f.write("# Bu dosyayı https://hidemy.io/en/proxy-checker/ adresinde kullanabilirsiniz\n\n")
                
                for proxy_type, proxies in self.working_proxies.items():
                    if proxies:
                        for proxy_data in proxies:
                            f.write(f"{proxy_data['proxy']}\n")
            
            print(f"{Fore.GREEN}✅ Hidemy.io formatı '{self.hidemy_io_file}' dosyasına kaydedildi.{Style.RESET_ALL}")
            
            # JSON formatında da kaydet
            json_data = {
                "generated_at": datetime.now().isoformat(),
                "test_duration": (datetime.now() - self.stats['start_time']).total_seconds(),
                "total_tested": self.stats['total_tested'],
                "working_count": self.stats['working_count'],
                "proxies": []
            }
            
            for proxy_type, proxies in self.working_proxies.items():
                for proxy_data in proxies:
                    ip, port = proxy_data['proxy'].split(':')
                    json_data["proxies"].append({
                        "ip": ip,
                        "port": int(port),
                        "type": proxy_data['type'],
                        "response_time": proxy_data['response_time'],
                        "country": proxy_data['country'],
                        "score": proxy_data['score'],
                        "tested_at": proxy_data['tested_at']
                    })
            
            with open("proxies.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.GREEN}✅ JSON formatı 'proxies.json' dosyasına kaydedildi.{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Çalışan proxy'ler kaydedilirken hata oluştu: {e}{Style.RESET_ALL}")

    def show_stats(self) -> None:
        """İstatistikleri gösterir."""
        total_time = (datetime.now() - self.stats['start_time']).total_seconds()
        print(f"\n{Fore.CYAN}📊 İSTATİSTİKLER{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}► Toplam test edilen proxy: {self.stats['total_tested']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}► Çalışan proxy sayısı: {self.stats['working_count']}{Style.RESET_ALL}")
        if self.stats['total_tested'] > 0:
            success_rate = (self.stats['working_count'] / self.stats['total_tested']) * 100
            print(f"{Fore.YELLOW}► Başarı oranı: {success_rate:.2f}%{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}► Başarı oranı: 0.00%{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}► Geçen süre: {total_time:.2f} saniye{Style.RESET_ALL}")
        
        for proxy_type, proxies in self.working_proxies.items():
            if proxies:
                avg_time = sum(p['response_time'] for p in proxies) / len(proxies)
                avg_score = sum(p['score'] for p in proxies) / len(proxies)
                countries = [p['country'] for p in proxies if p['country'] != 'Unknown']
                unique_countries = set(countries)
                
                print(f"{Fore.YELLOW}► {proxy_type.upper()} çalışan: {len(proxies)} (ortalama yanıt: {avg_time:.2f}s, ortalama puan: {avg_score:.1f}){Style.RESET_ALL}")
                
                if unique_countries:
                    print(f"{Fore.YELLOW}  ► Ülkeler: {', '.join(sorted(unique_countries)[:5])}{'...' if len(unique_countries) > 5 else ''}{Style.RESET_ALL}")

    def show_proxy_table(self) -> None:
        """Çalışan proxy'leri tablo formatında gösterir."""
        if not any(self.working_proxies.values()):
            print(f"{Fore.YELLOW}⚠️ Gösterilecek çalışan proxy bulunamadı.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🌐 ÇALIŞAN PROXY LİSTESİ{Style.RESET_ALL}")
        print(f"{'IP address':<20} {'Port':<8} {'Type':<8} {'Speed':<8} {'Country':<15} {'Score':<6}")
        print("-" * 70)
        
        all_proxies = []
        for proxy_type, proxies in self.working_proxies.items():
            for proxy_data in proxies:
                all_proxies.append(proxy_data)
        
        # Proxy'leri puanına göre sırala (en yüksek puanlılar üstte)
        sorted_proxies = sorted(all_proxies, key=lambda x: x['score'], reverse=True)
        
        for proxy_data in sorted_proxies[:20]:  # İlk 20'yi göster
            ip, port = proxy_data['proxy'].split(':')
            speed = f"{proxy_data['response_time']:.2f}s"
            print(f"{ip:<20} {port:<8} {proxy_data['type']:<8} {speed:<8} {proxy_data['country'][:15]:<15} {proxy_data['score']:<6}")
        
        if len(sorted_proxies) > 20:
            print(f"{Fore.YELLOW}... ve {len(sorted_proxies) - 20} daha proxy (dosyaya kaydedildi){Style.RESET_ALL}")

    def check_for_updates(self) -> bool:
        """Güncelleme kontrolü yapar."""
        try:
            # Basit bir güncelleme kontrolü
            update_url = "https://api.github.com/repos/b3y4z/proxy-checker/releases/latest"
            response = requests.get(update_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('tag_name', 'v1.0')
                current_version = "v2.0"  # Bu değer dinamik olmalı
                
                if latest_version != current_version:
                    print(f"{Fore.YELLOW}⚠️ Yeni versiyon mevcut: {latest_version} (şu anki: {current_version}){Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}📥 İndirmek için: {data.get('html_url', '')}{Style.RESET_ALL}")
                    return True
            return False
        except:
            return False

def spinner(stop_event, message="Proxy verisi çekiliyor..."):
    """Beklerken dönen bir çark animasyonu."""
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{chars[i]} {message}")
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(chars)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")  # Spinner'ı temizle

def save_proxy_file(file, url, kaynak):
    """Proxy listelerini verilen dosyaya kaydeder."""
    proxy_manager = ProxyManager()
    content = proxy_manager.send_request(url)
    if content:
        try:
            # Spinner için
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner, args=(stop_event, f"{kaynak} çekiliyor..."))
            spinner_thread.daemon = True
            spinner_thread.start()

            # Proxy verisini kaydet
            file.write(f"### {kaynak} ###\n\n".encode())
            file.write(content.encode() if isinstance(content, str) else content)
            
            # Spinner'ı durdur
            stop_event.set()
            spinner_thread.join(timeout=1.0)
            
            sys.stdout.write("\r✅ Proxy verisi başarıyla kaydedildi!\n")
            sys.stdout.flush()

            print(f"{Fore.GREEN}[✓] {kaynak} başarıyla çekildi ve kaydedildi!{Style.RESET_ALL}")
            return content
        except Exception as e:
            print(f"{Fore.RED}Dosyaya yazılırken hata alındı: {e} ⚠️{Style.RESET_ALL}")
            return None
    else:
        print(f"{Fore.YELLOW}[!] {kaynak} kaynağından veri çekilemedi.{Style.RESET_ALL}")
        return None

def select_sources(protocol, sources):
    """Kullanıcıya kaynak seçimi yaptırır ve seçilen kaynağı döndürür."""
    print(f"\n{protocol} Protokolü İçin Kaynaklar:")
    for i, source in enumerate(sources, start=1):
        color = Fore.GREEN if protocol == 'HTTP' else (Fore.RED if protocol == 'SOCKS4' else Fore.YELLOW)
        print(f"{i}. {color}{source['name']}{Style.RESET_ALL}")

    while True:
        try:
            source_index = int(input(f"\n{protocol} protokolü için proxy listesi çekilecek kaynağın numarasını girin: "))
            if 1 <= source_index <= len(sources):
                break
            else:
                print(f"{Fore.RED}Geçersiz giriş. Lütfen geçerli bir seçenek numarası girin.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Geçersiz giriş. Lütfen bir tam sayı girin.{Style.RESET_ALL}")

    # Seçilen kaynağı ekranda göstermek ve önde gelen listeleri gizlemek
    selected_source = sources[source_index - 1]
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{protocol} protokolü için proxy listesi {selected_source['name']} kaynağından çekiliyor...\n")
    return selected_source

def parse_proxy_content(content, proxy_type):
    """Proxy içeriğini ayrıştırır ve temizler."""
    if not content:
        return []
    
    proxies = []
    ip_port_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b')
    
    for line in content.splitlines():
        line = line.strip()
        # Yorum satırlarını ve boş satırları atla
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        
        # IP:PORT formatını ayıkla
        matches = ip_port_pattern.findall(line)
        if matches:
            proxies.extend(matches)
    
    # Benzersiz proxy'leri al
    unique_proxies = list(set(proxies))
    print(f"{Fore.GREEN}✅ {proxy_type} için {len(unique_proxies)} proxy bulundu.{Style.RESET_ALL}")
    return unique_proxies

def open_browser_for_proxy_check():
    """Kullanıcıya proxy kontrolü için tarayıcıyı açıp açmak istemediğini sorar."""
    while True:
        choice = input(f"\n{Fore.YELLOW}Proxy testlerinizi doğrulamak için hidemy.io sitesini açmak ister misiniz?\n{Fore.CYAN}https://hidemy.io/en/proxy-checker/{Style.RESET_ALL}\n{Fore.YELLOW}Evet için 'E', Hayır için 'H' tuşlayın: {Style.RESET_ALL}")
        
        if choice.lower() == 'e':
            webbrowser.open("https://hidemy.io/en/proxy-checker/")
            print(f"{Fore.GREEN}Tarayıcınız açılıyor...{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Hidemy.io sitesine 'hidemy_io_format.txt' dosyasını yükleyerek proxy'leri doğrulayabilirsiniz.{Style.RESET_ALL}")
            break
        elif choice.lower() == 'h':
            print(f"{Fore.YELLOW}Bağlantıya gitmekten vazgeçtiniz.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Geçersiz giriş! Lütfen 'E' veya 'H' tuşlayın.{Style.RESET_ALL}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Renkli banner
    banner = f'''
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║                                                              ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.YELLOW}██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗███████╗  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.YELLOW}██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝██╔════╝  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.YELLOW}██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ █████╗    {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.YELLOW}██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝ ██╔══╝    {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.YELLOW}██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   ███████╗  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.YELLOW}╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║                                                              ║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.MAGENTA}🌐 GELİŞMİŞ PROXY KONTROL ve YÖNETİM ARACI 🌐  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.GREEN}[ Coded By B3ʯ4z - Gelişmiş Sürüm v2.0 ]  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}PROTOCOL: {Fore.GREEN}HTTP/S {Fore.WHITE}| {Fore.CYAN}SOCKS4 {Fore.WHITE}| {Fore.RED}SOCKS5 {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║  {Fore.WHITE}FEATURES: {Fore.CYAN}ASYNC {Fore.WHITE}| {Fore.YELLOW}GEOIP {Fore.WHITE}| {Fore.GREEN}SCORING {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║                                                              ║{Style.RESET_ALL}
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    '''
    print(banner)

    # Güncelleme kontrolü
    proxy_manager = ProxyManager()
    proxy_manager.check_for_updates()

    # Proxy dosyalarını aç
    with open('http.txt', 'wb') as http, open('socks4.txt', 'wb') as socks4, open('socks5.txt', 'wb') as socks5:

        # Kaynaklar
        http_sources = [
            {"name": "🛡 ProxyScrape HTTP", "url": "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all&skip=0&limit=2000"},
            {"name": "🛡 ProxyList HTTP", "url": "https://www.proxylist.day/http.txt"},
            {"name": "🛡 FreeProxyList HTTP", "url": "https://free-proxy-list.net/anonymous-proxy.html"},
        ]

        socks4_sources = [
            {"name": "🧦 ProxyScrape SOCKS4", "url": "https://api.proxyscrape.com/v4/free-proxy-list-get?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all&skip=0&limit=2000"},
            {"name": "🧦 SOCKS4 ProxyList", "url": "https://www.proxylist.day/socks4.txt"},
            {"name": "🧦 SocksProxy SOCKS4", "url": "https://www.socks-proxy.net/"},
        ]

        socks5_sources = [
            {"name": "🔥 ProxyScrape SOCKS5", "url": "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all&skip=0&limit=2000"},
            {"name": "🔥 SOCKS5 ProxyList", "url": "https://www.proxylist.day/socks5.txt"},
            {"name": "🔥 SocksProxy SOCKS5", "url": "https://www.socks-proxy.net/"},
        ]

        # Protokollere göre kaynak seçimi
        selected_http = select_sources("HTTP", http_sources)
        selected_socks4 = select_sources("SOCKS4", socks4_sources)
        selected_socks5 = select_sources("SOCKS5", socks5_sources)

        # Proxy listelerini dosyalara kaydet ve içerikleri al
        http_content = save_proxy_file(http, selected_http["url"], selected_http["name"])
        socks4_content = save_proxy_file(socks4, selected_socks4["url"], selected_socks4["name"])
        socks5_content = save_proxy_file(socks5, selected_socks5["url"], selected_socks5["name"])

    # Proxy listelerini ayrıştır
    http_proxies = parse_proxy_content(http_content, "HTTP")
    socks4_proxies = parse_proxy_content(socks4_content, "SOCKS4")
    socks5_proxies = parse_proxy_content(socks5_content, "SOCKS5")

    # Toplam proxy sayısını güncelle
    proxy_manager.stats['total_tested'] = len(http_proxies) + len(socks4_proxies) + len(socks5_proxies)

    # Proxy'leri test et
    if http_proxies:
        proxy_manager.test_all_proxies(http_proxies, "http")
    
    if socks4_proxies:
        proxy_manager.test_all_proxies(socks4_proxies, "socks4")
    
    if socks5_proxies:
        proxy_manager.test_all_proxies(socks5_proxies, "socks5")

    # Çalışan proxy'leri kaydet
    proxy_manager.save_working_proxies()
    
    # İstatistikleri göster
    proxy_manager.show_stats()
    
    # Proxy tablosunu göster
    proxy_manager.show_proxy_table()

    # Hidemy.io ile doğrulama
    open_browser_for_proxy_check()

    # Teşekkür ve çıkış
    print(f"\n{Fore.YELLOW}[ℹ️] Programı kapatabilirsiniz.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Araçlarımı kullandığınız için teşekkürler 😊{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Çıkış yapmak için Enter'a basın...{Style.RESET_ALL}")
    print(f"\n\n{Fore.MAGENTA}Made with ❤️ by b3y4z{Style.RESET_ALL}\n\n")

if __name__ == "__main__":
    # Asenkron işlemler için event loop politikasını ayarla
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    main()