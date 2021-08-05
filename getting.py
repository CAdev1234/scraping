from bs4 import BeautifulSoup
import urllib.request
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import csv


scraping_url = ["https://www.kbauthority.com/duravit-bathroom-accessories/",
                "https://www.kbauthority.com/duravit-bath-vanities/",
                "https://www.kbauthority.com/duravit-storage-cabinets/",
                "https://www.kbauthority.com/duravit-medicine-cabinets/",
                "https://www.kbauthority.com/duravit-mirrors/",
                "https://www.kbauthority.com/duravit-shelves/",
                "https://www.kbauthority.com/duravit-benches/",
                "https://www.kbauthority.com/duravit-covers-and-panels/",
                "https://www.kbauthority.com/duravit-interior-systems/",
                "https://www.kbauthority.com/duravit-washbasins/",
                "https://www.kbauthority.com/duravit-bathtubs/",
                "https://www.kbauthority.com/duravit-shower-trays/",
                "https://www.kbauthority.com/duravit-showerscreens/",
                "https://www.kbauthority.com/duravit-bidets/",
                "https://www.kbauthority.com/duravit-sensowash/",
                "https://www.kbauthority.com/duravit-toilets/",
                "https://www.kbauthority.com/duravit-urinals/",
                "https://www.kbauthority.com/duravit-parts/",
                "https://www.kbauthority.com/duravit-robe-hooks/",
                "https://www.kbauthority.com/duravit-shower-baskets/",
                "https://www.kbauthority.com/duravit-shower-seats/",
                "https://www.kbauthority.com/duravit-soap-dishes/",
                "https://www.kbauthority.com/duravit-soap-dispensers/",
                "https://www.kbauthority.com/duravit-toilet-brush-holders/",
                "https://www.kbauthority.com/duravit-toilet-paper-holders/",
                "https://www.kbauthority.com/duraviit-towel-rails/",
                "https://www.kbauthority.com/duravit-towel-rings/",
                "https://www.kbauthority.com/duravit-tumbler-holders/",
                ]
filename = ['bathroom-accessories.csv',
            'Bath Vanities.csv',
            'Storage Cabinets.csv',
            'Medicine Cabinets.csv',
            'Mirrors.csv',
            'Shelves.csv',
            'Benches.csv',
            'Covers and Panels.csv',
            'Interior Systems.csv',
            'Bathroom Sinks.csv',
            'Bathtubs.csv',
            'Shower Trays.csv',
            'Shower Screens.csv',
            'Bidets.csv',
            'SensoWash.csv',
            'Toilets.csv',
            'Urinals.csv',
            'Parts.csv',
            'Robe Hooks.csv',
            'Shower Baskets.csv',
            'Shower Seats.csv',
            'Soap Dishes.csv',
            'Soap Dispensers.csv',
            'Toilet Brush Holders.csv',
            'Toilet Paper Holders.csv',
            'Towel Rails.csv',
            'Towel Rings.csv',
            'Tumbler Holders.csv']
# url_number = 9
#url_number = 5
# url_number = 17
url_number = 1

dic_data = {}
dic_list = []

# driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)


dic_data["Category"] = "Home > Bath > All Bath Brands > Duravit>" + filename[url_number].replace('.csv', '')
good_url = []
if os.path.exists(str(filename[url_number])):
    os.remove(filename[url_number])
products_detail_page = urllib.request.urlopen(scraping_url[url_number])
# good_url.append(scraping_url[url_number])
soup = BeautifulSoup(products_detail_page, 'html.parser')
n = 0

# if soup.find(name='ul', attrs={'class': 'paging'}) is not None:
#     paginator = soup.find(name='ul', attrs={'class': 'paging'}).find_all(name="a")
#     for i in range(0, len(paginator)-1):
#         good_url.append(paginator[i].get('href'))

good_url = ["https://www.kbauthority.com/duravit-bath-vanities/",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=2",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=3",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=4",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=5",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=6",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=7",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=8",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=9",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=10",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=11",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=12",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=13",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=14",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=15",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=16",
            "https://www.kbauthority.com/duravit-bath-vanities/?page=17",
            ]
count_num = 0
for url_item in good_url:
    print("good_url=", good_url)
    products_detail_page = urllib.request.urlopen(url_item)
    soup = BeautifulSoup(products_detail_page, 'html.parser')
    product_detail_page = soup.find_all(name='a', attrs={'class': 'product-title'})
    for item in product_detail_page:
        href = item.get('href')
        # Url
        dic_data['Url'] = href
        try:
            driver.get(href)
        except:
            print("driver get method error")

        individual_detail_page = driver.page_source
        individual_soup = BeautifulSoup(individual_detail_page, 'html.parser')
        # print(driver)

        # Title, Finish Option, SKU, Price, Save percent, Product list price, Image url
        # dic_data["Product Title"] = individual_soup.title.getText()
        dic_data["Product Title"] = individual_soup.find_all(name='span', attrs={'class': 'product-title'})[0].getText()
        if individual_soup.find(id="product_code") is not None:
            dic_data["SKU"] = "__@ " + str(individual_soup.find(id="product_code").getText())
        else:
            dic_data["SKU"] = ''
        if individual_soup.find(id="product_price") is not None:
            dic_data["Price"] = "__@ " + '$' + str(individual_soup.find(id="product_price").getText())
        else:
            dic_data["Price"] = "__@ " + '$' + str(0)
        if individual_soup.find(id="save_percent") is not None:
            dic_data["Save percent"] = "__@ " + str(individual_soup.find(id="save_percent").getText()) + str("%")
            # print(dic_data["Save percent"])
        else:
            dic_data["Save percent"] = ''
        if individual_soup.find(id="product_list_price", name='span') is not None:
            dic_data["Product list price"] = "__@ " + '$' + str(individual_soup.find(id="product_list_price", name='span').getText())
            # print(dic_data["Product list price"])
        else:
            dic_data["Product list price"] = ''
        dic_data["Image url"] = individual_soup.find(id="product_thumbnail").get('src')

        # Product details
        product_details = individual_soup.find(id="product_fulldescr")
        str_var = product_details.get_text()
        dic_data["Product details"] = "".join([s for s in str_var.strip().splitlines(True) if s.strip()])
        str_var = ''
        dic_data["ProductFullDescriptionHtml"] = product_details

        # Dimensions and measurements
        dimensions_measurements_name = individual_soup.find(id="descr").find_all(name='td', attrs={'class': 'spec-name'})
        dimensions_measurements_value = individual_soup.find(id="descr").find_all(name='td', attrs={'class': 'spec-val'})
        dimension_options = ["Theme",
                             "Feature",
                             "Number of Sinks",
                             "Finish",
                             "Type",
                             "Countertop Material",
                             "Collections",
                             "UPC",
                             "Sink Shape",
                             "Length",
                             "Material",
                             "Faucet Holes",
                             "Number of Basins",
                             "Shape",
                             "Installation Type",
                             "Gallons per Flush",
                             "Rough-In",
                             "LeverPlacement",
                             "Flush Type",
                             "Width",
                             "Front to Back",
                             "Depth",
                             "Height",
                             "Frame Finish",
                             "DoorType",
                             "Frame Type",
                             "GlassTickness",
                             "GlassType",
                             "Hardware Finish"]
        for dimension_option in dimension_options:
            dic_data[dimension_option] = ""
        for i in range(len(dimensions_measurements_name)):
            # if dimensions_measurements_name[i].string == "UPC":
            #     dic_data["UPC"] = "__@" + str(dimensions_measurements_value[i].getText())
            #     continue
            # if dimensions_measurements_name[i].string == "Width":
            #     dic_data["Width"] = str(dimensions_measurements_value[i].getText()) + " inch"
            #     continue
            dic_data[dimensions_measurements_name[i].string] = "__@ " + str(dimensions_measurements_value[i].getText())

        # Available Options and Finishes
        # plus_button = individual_soup.find(name="a", attrs={'class': 'show-more-toggler'})
        # if plus_button is not None:
        #     driver.find_element_by_class_name("show-more-toggler").click()
        if individual_soup.find(name="table", attrs={'class': 'var-table-box'}) is not None:
            available_options = individual_soup.find(name="table", attrs={'class': 'var-table-box'})
            var_num = 0
            str_var = ""
            for item in available_options.find_all("a"):
                if var_num == available_options.find_all("a").__len__()-1:
                    str_var = str_var + item.getText()
                else:
                    str_var = str_var + item.getText() + ";"
                var_num = var_num + 1
            dic_data["Available Options"] = str_var
        else:
            dic_data["Available Options"] = ""
        str_var = ''

        # Manufacturer Resources
        if individual_soup.find(id="pdfdocs") is not None:
            manufacturer_resources = individual_soup.find(id="pdfdocs").find_all(name='a')
            str_var = ''
            var_num = 0
            for manufacturer_resource in manufacturer_resources:
                if var_num == manufacturer_resources.__len__()-1:
                    str_var = str_var + manufacturer_resource.get('href')
                else:
                    str_var = str_var + manufacturer_resource.get('href') + ";"
                var_num = var_num + 1
            dic_data['Manufacturer Resources'] = str_var
        else:
            dic_data['Manufacturer Resources'] = ""
        str_var = ""

        # Product Gallery
        if individual_soup.find(id="gallery") is not None:
            product_gallerys = individual_soup.find(id="gallery").find_all(name="img")
            var_num = 0
            for product_gallery in product_gallerys:
                if var_num == product_gallerys.__len__() - 1:
                    str_var = str_var + product_gallery.get('src')
                else:
                    str_var = str_var + product_gallery.get('src') + ";"
                var_num = var_num + 1
            dic_data['Product Gallery'] = str_var
        else:
            dic_data['Product Gallery'] = ''

        # About the manufacturer
        str_var = ''
        if individual_soup.find(id="about_brand_info") is not None:
            str_var = individual_soup.find(id="about_brand_info").find(name="p").string
            dic_data["About the Manufacturer"] = "".join([s for s in str_var.strip().splitlines(True) if s.strip()])
        else:
            dic_data["About the Manufacturer"] = ''
        print(dic_data)
        dic_list.append(dic_data.copy())
        # print(dic_list)
        # break
# print(dic_list)
length_var = []
for item in dic_list:
    length_var.append(len(item))
keys = dic_list[length_var.index(max(length_var))].keys()
for item in dic_list:
    with open(str("scrapingResult/" + filename[url_number]), 'a+', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        if n == 0:
            dict_writer.writeheader()
            n = n + 1
        dict_writer.writerow(item)

