import csv

import requests

from xextract import String



NOBEL_QURAN_URL = "https://dusp.org/quran/noble-qurans/"
QURAN_AQIDAH_URL = "https://dusp.org/arabic/aqidah-fiqh/"
QURAN_FATWA_URL = "https://dusp.org/urdu/fatawa-qa/"
HINDI_QURAN_URL = "https://dusp.org/languages/hindi-books/"

ALL_QURAN_URLS_LIST = [NOBEL_QURAN_URL, QURAN_AQIDAH_URL, QURAN_FATWA_URL, HINDI_QURAN_URL, "https://dusp.org/english/hereafter-the-unseen/", "https://dusp.org/languages/farsi/"]

ALL_QURANS_LINKS_LIST = []

def get_quran_books():
    for url in ALL_QURAN_URLS_LIST:
        response = requests.get(url, verify=False)
        html = response.text
        get_title = String(xpath='//h3[@class="h3 product-title"]//a', attr="href").parse_html(html)
        for all_guran in get_title:
            print(all_guran)
            ALL_QURANS_LINKS_LIST.append(all_guran)

get_quran_books()

# page = 1

def get_quran_details():
    counter = 0  # Initialize counter variable
    for url_of_quran in ALL_QURANS_LINKS_LIST:
        counter += 1  # Increment counter for each URL
        print(f"Currently on URL number: {counter}")  # Print the URL number
        response = requests.get(url_of_quran, verify=False)
        html_quran = response.text
        title = String(xpath='//div[@class="col-md-6 product-page-right"]//h1[@class="h1 prod-title"]').parse_html(html_quran)[0]
        code = String(xpath='//*[@id="main"]/div[1]/div[2]/div[1]/strong').parse_html(html_quran)[0]
        price = String(xpath='//span[@itemprop="price"]').parse_html(html_quran)[0]
        try:
            translator = String(xpath='//td[strong[text()="Translator"]]/following-sibling::td').parse_html(html_quran)[0]
            if len(translator) == 0:
                translator = "No Translator"
        except:
            translator = "No Translator"
        try:
            blinding = String(xpath='//td[strong[text()="Binding"]]/following-sibling::td').parse_html(html_quran)[0]
            if len(blinding) == 0:
                blinding = "No Blinding"
        except:
            blinding = "No Blinding"
        try:
            pages = String(xpath='//td[strong[text()="Pages"]]/following-sibling::td').parse_html(html_quran)[0]
            if len(pages) == 0:
                pages = "No Pages"
        except:
            pages = "No Pages"
        try:
            size_in_inches = String(xpath='//td[strong[text()="Size in Inches"]]/following-sibling::td').parse_html(html_quran)[0]
            if len(size_in_inches) == 0:
                size_in_inches = "No Size in Inches"
        except:
            size_in_inches = "No Size in Inches"
        try:
            description_ = String(xpath='//div[@class="product-description"]//p | //div[@class="product-description"]//em').parse_html(html_quran)
            description = ' '.join(description_)

            # Removing extra spaces and newline characters
            description = ' '.join(description.split())
            if len(description) == 0:
                description = "No Description"

        except:
            description = "No Description"

        code_form = code.replace('\xa0', '').strip()
        code_formated = code_form.replace('Code', '').strip()

        header = ["Title, Code, Price, URL, Translator, Blinding, Pages, Size in Inches, Description"]

        with open('all_quran_data.csv', 'a+', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(header)

            writer.writerow(
                [title, code_formated, price, url_of_quran, translator, blinding, pages, size_in_inches, description])

        print("Data Saved in CSV File")

get_quran_details()


