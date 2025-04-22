from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import urllib.parse
import re
import xml.etree.ElementTree as ET


# Türkçe karakterleri normalize eden fonksiyon
def normalize_text(text):
    turkce_karakterler = str.maketrans("ıİğĞçÇşŞöÖüÜ", "iiggccssoouu")
    normalized_text = text.translate(turkce_karakterler)
    return normalized_text


# Sayılarla metin arasına boşluk eklemek için fonksiyon
def bosluk_ekle(malzeme):
    yeni_malzeme = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', malzeme)
    return yeni_malzeme


def main():
    # XML dosyasının temel yapısını oluşturuyoruz
    root = ET.Element("tarifler")

    # WebDriver'ı başlatıyoruz
    driver = webdriver.Chrome()

    try:
        # Yemek tariflerinin bulunduğu sayfanın URL'si
        url = "https://yemek.com/tarif/"
        driver.get(url)

        # Sayfanın dinamik olarak yüklenebilmesi için bir süre bekliyoruz
        time.sleep(5)

        # Sayfayı kaydırarak tüm tariflerin yüklenmesini sağlıyoruz
        for i in range(400):
            driver.find_element("tag name", "body").send_keys(Keys.END)
            time.sleep(1)

        # Sayfanın HTML içeriğini alıyoruz
        html_icerigi = driver.page_source
        soup = BeautifulSoup(html_icerigi, "html.parser")

        # Tarif başlıklarını buluyoruz
        tarifler = soup.find_all("h4", class_="BoxContent_boxTitle__xIYek")

        for tarif in tarifler:
            tarif_adi = tarif.text.strip()
            if ":" in tarif_adi:
                tarif_adi = tarif_adi.split(":")[1].strip()

            tarif_adi_normalized = normalize_text(tarif_adi)
            slug_tarif_adi = tarif_adi_normalized.replace(" ", "-").lower()
            detay_link = f"https://yemek.com/tarif/{slug_tarif_adi}"

            # Tarif XML elemanını oluşturuyoruz
            tarif_element = ET.SubElement(root, "tarif")

            baslik_element = ET.SubElement(tarif_element, "baslik")
            baslik_element.text = tarif_adi_normalized

            link_element = ET.SubElement(tarif_element, "detay_link")
            link_element.text = detay_link

            # Detay sayfasına gidiyoruz
            driver.get(detay_link)
            time.sleep(2)

            # Detay sayfasının HTML içeriğini alıyoruz
            detay_html = driver.page_source
            detay_soup = BeautifulSoup(detay_html, "html.parser")

            malzemeler_div = detay_soup.find("div", class_="Ingredients_ingredients__hk2Pb")

            malzemeler_element = ET.SubElement(tarif_element, "malzemeler")

            if malzemeler_div:
                malzeme_listesi = malzemeler_div.find_all("li")

                for malzeme in malzeme_listesi:
                    malzeme_text = malzeme.get_text(strip=True)
                    if malzeme_text:
                        malzeme_text_duzenli = bosluk_ekle(malzeme_text)
                        malzeme_element = ET.SubElement(malzemeler_element, "malzeme")
                        malzeme_element.text = malzeme_text_duzenli

                    # Sosu için malzemeler
                    if "sosu için" in malzeme_text.lower():
                        sosu_icin_element = ET.SubElement(tarif_element, "sosu_icin_malzemeler")
                        malzeme_sosu_element = ET.SubElement(sosu_icin_element, "malzeme")
                        malzeme_sosu_element.text = malzeme_text_duzenli

            else:
                print(f"{tarif_adi} için malzeme bulunamadı.")

            # Ana sayfaya geri dönüyoruz
            driver.back()
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nManuel olarak durduruldu. Toplanan veriler kaydediliyor...")

    except Exception as e:
        print(f"\nBir hata oluştu: {e}")

    finally:
        # XML ağacını oluşturuyoruz
        tree = ET.ElementTree(root)

        # XML dosyasını belirttiğiniz yola kaydediyoruz
        tree.write("C:/Users/ahmet/Desktop/tarifler.xml", encoding="utf-8", xml_declaration=True)

        # Dosyaya yazma işlemi tamamlandı mesajı
        print("XML dosyasına yazma işlemi tamamlandı.")

        # Tarayıcıyı kapatıyoruz
        driver.quit()


if __name__ == "__main__":
    main()

