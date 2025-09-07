🌐 Proxy Checker - Gelişmiş Proxy Kontrol Aracı
Bu araç, HTTP, SOCKS4 ve SOCKS5 proxy'lerini otomatik olarak kontrol eden, test eden ve listeleyen gelişmiş bir Python uygulamasıdır.

https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/Version-v2.0-orange

✨ Özellikler
🔍 Çoklu Kaynaklardan Proxy Çekme

⚡ Asenkron Proxy Testi (aiohttp ile yüksek hız)

🌍 Coğrafi Konum Tespiti (200+ ülke desteği)

🏆 Akıllı Puanlama Sistemi (1-100 arası kalite puanı)

📊 Detaylı İstatistikler ve Raporlama

💾 Çoklu Çıktı Formatları (TXT, JSON, Hidemy.io formatı)

🔄 Otomatik Güncelleme Kontrolü

🎨 Renkli ve Kullanıcı Dostu Arayüz

📦 Kurulum
Gereksinimler
Python 3.8 veya üzeri

pip (Python paket yöneticisi)

Yükleme Adımları
Depoyu klonlayın veya indirin:

bash
git clone https://github.com/bilisimindex/proksy.py.git
cd proksy.py
Gerekli kütüphaneleri yükleyin:

bash
pip install -r requirements.txt
Script'i çalıştırın:

bash
python proksy.py
requirements.txt İçeriği
text
requests>=2.28.0
aiohttp>=3.8.0
colorama>=0.4.0
tqdm>=4.64.0
backoff>=2.0.0
🚀 Kullanım
Programı çalıştırdığınızda otomatik olarak:

HTTP, SOCKS4 ve SOCKS5 proxy kaynakları listelenecek

Her protokol için kaynak seçimi yapabileceksiniz

Proxy'ler otomatik indirilecek ve test edilecek

Çalışan proxy'ler dosyalara kaydedilecek

Çıktı Dosyaları:

calisan_proxyler.txt - Detaylı proxy listesi

hidemy_io_format.txt - Hidemy.io uyumlu format

proxies.json - JSON formatında detaylı veri

🛠️ Yapılandırma
Kaynakları Özelleştirme
main() fonksiyonundaki kaynak listelerini düzenleyerek kendi proxy kaynaklarınızı ekleyebilirsiniz:

python
http_sources = [
    {"name": "🛡 Özel Kaynak", "url": "https://ornek.com/proxy.txt"},
    # Diğer kaynaklar...
]
Eşzamanlı İşlem Sayısını Ayarlama
test_all_proxies() fonksiyonundaki max_workers parametresini değiştirerek eşzamanlı test sayısını ayarlayabilirsiniz.

📊 Çıktı Örnekleri
Proxy Listesi Çıktısı
text
IP address            Port     Type     Speed    Country         Score  
--------------------------------------------------------------------------------
192.168.1.100         8080     http     0.23s    United States   87
45.77.132.215         3128     http     0.45s    Germany         76
İstatistikler Çıktısı
text
📊 İSTATİSTİKLER
► Toplam test edilen proxy: 2450
► Çalışan proxy sayısı: 587
► Başarı oranı: 23.96%
► Geçen süre: 125.43 saniye
► HTTP çalışan: 245 (ortalama yanıt: 0.34s, ortalama puan: 72.1)
► SOCKS4 çalışan: 187 (ortalama yanıt: 0.41s, ortalama puan: 68.5)
► SOCKS5 çalışan: 155 (ortalama yanıt: 0.38s, ortalama puan: 75.3)
🔧 Geliştirme
Yeni Özellik Eklemek
Proxy test metodlarını test_proxy_async() fonksiyonunda geliştirebilirsiniz

Yeni çıktı formatları için save_working_proxies() fonksiyonunu genişletebilirsiniz

Yeni istatistikler için show_stats() fonksiyonunu düzenleyebilirsiniz

Hata Ayıklama
Hata ayıklama modunda çalıştırmak için:

bash
python -m pdb proksy.py
🤝 Katkıda Bulunma
Fork edin

Feature branch'i oluşturun (git checkout -b feature/yeni-ozellik)

Değişikliklerinizi commit edin (git commit -am 'Yeni özellik eklendi')

Branch'i push edin (git push origin feature/yeni-ozellik)

Pull Request oluşturun

📝 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.

⚠️ Sorumluluk Reddi
Bu araç eğitim amaçlıdır. Proxy'leri kullanmadan önce yerel yasaları ve servis sağlayıcınızın kullanım koşullarını kontrol edin. Geliştirici, bu aracın kötüye kullanımından sorumlu değildir.

📞 İletişim
Sorularınız v önerileriniz için:

GitHub Issues: https://github.com/bilisimindex/proksy.py/issues

E-posta: bilisimindex@example.com

🌟 Yıldız Geçmişi
https://api.star-history.com/svg?repos=bilisimindex/proksy.py&type=Date

Not: Bu araç sürekli geliştirilmektedir. Yeni özellikler ve iyileştirmeler için sık sık güncelleme kontrol edin.
