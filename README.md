# Grup-116-YazLab-Projesi-
### README

# Tarif Toplama Web Kazıma Projesi

Bu proje, iki farklı web sitesinden yemek tariflerini toplayarak XML formatında saklar. Toplanan veriler, tarif isimleri, malzeme listeleri ve detaylı tarif sayfası bağlantılarını içerir. Proje, web sayfalarıyla etkileşim kurmak, HTML içeriklerini ayrıştırmak ve gerekli bilgileri çıkarmak için Python kütüphanelerini kullanır.

## Proje Özeti

Bu kod:
- **Yemek tariflerini kazır**: `https://yemek.com/tarif/` ve `https://www.ardaninmutfagi.com/category/icecekler` sitelerinden veri toplar.
- **Türkçe karakterleri normalize eder** ve özel biçimlendirmeleri işler.
- **Toplanan verileri** yapılandırılmış XML dosyaları olarak saklar.

Oluşturulan XML dosyalarında:
- **Tarif isimleri**
- **Malzeme listeleri**
- **Tarif detay bağlantıları** yer alır.

## Geliştirme Ortamı

- **Dil**: Python 3.x
- **Kütüphaneler**:
  - `selenium` - Tarayıcı otomasyonu için
  - `BeautifulSoup` (`bs4` içinde) - HTML ayrıştırma için
  - `urllib.parse` - URL düzenleme için
  - `xml.etree.ElementTree` - XML oluşturma için
- **Tarayıcı Sürücüsü**: Chrome WebDriver (Chrome sürümünüzle uyumlu olmasına dikkat edin)

## Kurulum ve Ayarlar

1. **Gerekli Python Kütüphanelerini Yükleyin**:  
   Aşağıdaki komutla gerekli paketleri yükleyin:
   ```bash
   pip install selenium beautifulsoup4
   ```

2. **Chrome WebDriver İndirin**:  
   Chrome WebDriver'ı, scriptin bulunduğu dizine veya sistem yolunuza ekleyin.

3. **Scriptleri Çalıştırın**:  
   - Script 1 `yemek.com` adresinden tarifleri çeker.
   - Script 2 `ardaninmutfagi.com` adresinden tarifleri çeker.

   Gerekirse her scriptteki kayıt yolunu ayarlayın.

## Kullanım

1. **Dizine Gidin**:  
   Terminal veya komut istemcisini açın ve scriptlerin bulunduğu dizine gidin.

2. **Scriptleri Çalıştırın**:  
   Her bir scripti aşağıdaki gibi çalıştırın:
   ```bash
   python script1.py  # yemek.com için
   python script2.py  # ardaninmutfagi.com için
   ```

3. **Çıktıyı Görüntüleyin**:  
   XML dosyaları (`tarifler.xml` ve `ardaicecek.xml`), belirtilen dizine kaydedilecektir.

## XML Yapısı Örneği

Her tarif, aşağıdaki yapıda XML formatında kaydedilir:

```xml
<tarifler>
    <tarif>
        <baslik>Tarif Adı</baslik>
        <detay_link>Tarif Linki</detay_link>
        <malzemeler>
            <malzeme>Malzeme 1</malzeme>
            <malzeme>Malzeme 2</malzeme>
        </malzemeler>
        <sosu_icin_malzemeler>
            <malzeme>Sos Malzemesi 1</malzeme>
        </sosu_icin_malzemeler>
    </tarif>
</tarifler>
```

## Sorun Giderme

- **Selenium hataları**: Chrome WebDriver sürümünüzün Chrome tarayıcınızla uyumlu olduğundan emin olun.
- **Zaman aşımı sorunları**: Sayfaların yüklenme süresine bağlı olarak, scriptteki bekleme süresini ayarlamanız gerekebilir.
