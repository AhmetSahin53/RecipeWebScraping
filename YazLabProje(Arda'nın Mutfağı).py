from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.parse
import xml.etree.ElementTree as ET

# Türkçe karakterleri normalize eden fonksiyon
def normalize_text(text):
    turkce_karakterler = str.maketrans("ıİğĞçÇşŞöÖüÜ", "iiggccssoouu")
    return text.translate(turkce_karakterler)

def main():
    # WebDriver'ı başlatıyoruz
    driver = webdriver.Chrome()

    # XML kök elemanını oluştur
    root = ET.Element("tarifler")

    # Kaç sayfadan tarif çekeceğinizi belirleyin
    sayfa_sayisi = 32

    for sayfa in range(1, sayfa_sayisi + 1):
        if sayfa == 1:
            url = "https://www.ardaninmutfagi.com/category/icecekler"
        else:
            url = f"https://www.ardaninmutfagi.com/category/icecekler/page/{sayfa}/"

        driver.get(url)
        time.sleep(1)
        html_icerigi = driver.page_source
        soup = BeautifulSoup(html_icerigi, "html.parser")

        tarifler = soup.find_all("h4", class_="entry-title")

        for tarif in tarifler:
            tarif_adi = tarif.text.strip()
            tarif_adi_normalized = normalize_text(tarif_adi)
            slug_tarif_adi = tarif_adi_normalized.replace(" ", "-").lower()
            slug_tarif_adi = urllib.parse.quote(slug_tarif_adi)
            detay_link = f"https://www.ardaninmutfagi.com/yemek-tarifleri/icecekler/{slug_tarif_adi}"

            driver.get(detay_link)
            time.sleep(3)
            detay_html = driver.page_source
            detay_soup = BeautifulSoup(detay_html, "html.parser")

            tarif_elem = ET.SubElement(root, "Tarif", ad=tarif_adi)
            malzemeler_div = detay_soup.find("div", class_="mlz")

            if malzemeler_div:
                malzeme_texts = malzemeler_div.find_all(string=True)
                for malzeme in malzeme_texts:
                    malzeme = malzeme.strip()
                    if malzeme and malzeme != "Malzemeler":
                        malzeme_elem = ET.SubElement(tarif_elem, "Malzeme")
                        malzeme_elem.text = malzeme

            else:
                content_div = detay_soup.find("div", class_="content")
                if content_div:
                    br_elements = content_div.find_all("br")
                    if br_elements:
                        for br in br_elements:
                            malzeme = br.previous_sibling.strip() if br.previous_sibling else ""
                            if malzeme:
                                malzeme_elem = ET.SubElement(tarif_elem, "Malzeme")
                                malzeme_elem.text = malzeme

            driver.back()
            time.sleep(3)

    # Tarayıcıyı kapatıyoruz
    driver.quit()

    # XML dosyasını oluştur ve kaydet
    tree = ET.ElementTree(root)
    tree.write("C:/Users/kural/Desktop/ardaicecek.xml", encoding="utf-8", xml_declaration=True)
    print("XML dosyasına yazma işlemi tamamlandı.")

if __name__ == "__main__":
    main()

