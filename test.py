#
# Created by Berke Akyıldız on 30/December/2019
#
import time
import math
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

r = requests.get("https://www.trendyol.com/electronic-arts/fifa-2020-ps4-oyun-turkce-menu-p-31821531")
soup = BeautifulSoup(r.content, "html.parser")

xml_counter = ET.Element("product")

price = soup.find("span", attrs={"class": "prc-slg"}).text
name = soup.find("span", attrs={"class": "pr-in-nm"}).text
marka = soup.title.text.split(" | ")[0]
description = soup.find("div", attrs={"class": "pr-in-dt-cn"})
spec_list = description.find_all("ul")
spec_spans = spec_list[0].find_all("span")
specs = spec_spans[1].find_all("li")[1:]
image = soup.find("img", attrs={"class": "ph-gl-img"}).get("src")

print(image)

xml_name = ET.SubElement(xml_counter, "Name")
xml_name.text = name.strip()

xml_price = ET.SubElement(xml_counter, "Price")
xml_price.text = price.strip()

xml_image = ET.SubElement(xml_counter, "Image")
xml_image.text = image.strip()

xml_desc = ET.SubElement(xml_counter, "Description")


r.close()

# browser.close()
# s = ET.tostring(xml_counter, encoding='utf8')
# s = s.decode("utf8")
# s = s.split("\n")[1]
# with open("test" + ".xml", "w+", encoding="utf-8") as xml_file:
#     xml_file.write(s)
# print(s)
