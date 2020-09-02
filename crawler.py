#
# Created by Berke Akyıldız on 29/December/2019
#
import time
import math
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

driver_path = "D:\Program Files\PycharmProjects\Trendyol-Scraper-Crawler\chromedriver.exe"

baseUrl = "https://www.trendyol.com/"


def getAllMainCategories():
    r = requests.get(baseUrl)
    soup = BeautifulSoup(r.content, "lxml")

    mainCategoryFile = open("main_categories.txt", "w+")

    categories = soup.find_all("a", attrs={"class": "category-header"})
    for category in categories:
        print(category.get("href"))
        mainCategoryFile.write(baseUrl + category.get("href") + "\n")


    mainCategoryFile.close()


def getSubCategories():
    r = requests.get(baseUrl)
    soup = BeautifulSoup(r.content, "lxml")

    subCategoryFile = open("subcategories.txt", "w+")
    categories = soup.find_all("a", attrs={"class": "sub-category-header"})
    for category in categories:
        print(category.get("href"))
        subCategoryFile.write(baseUrl + category.get("href") + "\n")

    subCategoryFile.close()


def getProductLinks(categoryUrl):
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get(categoryUrl)
    time.sleep(1)
    file = categoryUrl.split("/")
    fileName = file[len(file) - 1]
    linkFile = open(fileName + ".txt", "w+")

    elem = browser.find_element_by_tag_name("body")

    description = browser.find_element_by_class_name("dscrptn").text.split(" ")
    product_count = int(description[-3])

    page_count = math.ceil(product_count / 24)

    no_of_pagedowns = page_count * 6

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1

    links = browser.find_elements_by_class_name("p-card-chldrn-cntnr")
    print(len(links))
    for link in links:
        linkFile.write(link.get_attribute("href") + "\n")

    browser.close()


def getProductInformation(productFileName):
    root = ET.Element(productFileName.split(".")[0])
    count = 0

    with open(productFileName) as productFile:
        lines = productFile.readlines()

        for url in lines:
            count += 1
            print("\n" + count.__str__())
            xml_counter = ET.SubElement(root, "product")
            print(url)

            r = requests.get(url.strip())
            soup = BeautifulSoup(r.content, "html.parser")

            price = soup.find("span", attrs={"class": "prc-slg"}).text
            name = soup.title.text.split(" | ")[0]
            description = soup.find("div", attrs={"class": "pr-in-dt-cn"})
            spec_list = description.find_all("ul")
            spec_spans = spec_list[0].find_all("span")[1]
            specs = spec_spans.find_all("li")[1:]
            image = soup.find("img", attrs={"class": "ph-gl-img"}).get("src")

            xml_name = ET.SubElement(xml_counter, "Name")
            xml_name.text = name.strip()

            xml_price = ET.SubElement(xml_counter, "Price")
            xml_price.text = price.strip()

            xml_image = ET.SubElement(xml_counter, "Image")
            xml_image.text = image.strip()

            xml_desc = ET.SubElement(xml_counter, "Description")

            for spec in specs:
                spectext = spec.text
                if " : " in spectext:
                    specname = spectext.split(":")[0]
                    specvalue = spectext.split(":")[1]
                    # print(specname + " = " + specvalue)
                    xml_spec = ET.SubElement(xml_desc, specname.strip().replace(" ", "_").replace("(", "").replace(")", ""))
                    xml_spec.text = specvalue.strip()
            r.close()
            s = ET.tostring(xml_counter, encoding='utf8')
            s = s.decode("utf8")
            s = s.split("\n")[1]
            print(s)

            # browser.close()
    s = ET.tostring(root, encoding='utf8')
    s = s.decode("utf8")
    with open(productFileName.split(".")[0] + ".xml", "w+", encoding="utf-8") as xml_file:
        xml_file.write(s)



getProductInformation("oyun-ve-oyun-konsollari.txt")




