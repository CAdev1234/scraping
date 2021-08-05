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

# dd = '{"product":{"id":5942012805287,"gid":"gid:\/\/shopify\/Product\/5942012805287","vendor":"OFM","type":"Chairs","variants":[{"id":36990428577959,"price":22572,"name":"Bonded Leather Manager Chair, High Back Office Chair for Computer Desk (568) - Black","public_title":"Black","sku":"568-BLK"}]},"page":{"pageType":"product","resourceType":"product","resourceId":5942012805287},"page_view_event_id":"dffb91b3e4337255e551c5263fafcac7b686d3b9d5020c4a6b36a2e65f246917","cart_event_id":"63a3d227c81304afa52b457eab4da36801c4caf5620e0095c264b495e7154dd0"}'
# print(json.loads(dd))
# exit()


index = 0
file_name = 'ofminc_result.csv'


dic_list = []


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)

if os.path.exists(str(file_name)):
    os.remove(file_name)

# products_detail_page = urllib.request.urlopen(scraping_url)
#
# soup = BeautifulSoup(products_detail_page, 'html.parser')


count_num = 0
for indexi in range(1, 8):
    url_item = 'https://ofminc.com/collections/all?page=' + str(indexi)
    print(url_item)
    products_detail_page = urllib.request.urlopen(url_item)
    soup = BeautifulSoup(products_detail_page, 'html.parser')
    product_detail_page = soup.find_all(name='a', attrs={'class': 'boost-pfs-filter-product-item-title'})
    for item in product_detail_page:
        dic_data = {
            'Website': '',
            'SKU': '',
            'Link(from where we get info)': '',
            'Name': '',
            'Type of product': '',
            'Model/Color': '',
            'Material': '',
            'Price': '',
            'Promo Price': '',
            'Description of a product (romantic)': '',
            'Size': '',
            'Info from the file': '',
            'Width': '',
            'Depth': '',
            'Height': '',
            'Weight': '',
            'Bullet1': '',
            'Bullet2': '',
            'Bullet3': '',
            'Bullet4': '',
            'Bullet5': '',
            'Bullet6': '',
            'Bullet7': '',
            'Bullet8': '',
            'Bullet9': '',
            'Bullet10': '',
            'Bullet11': '',
            'Bullet12': '',
            'Bullet13': '',
            'Bullet14': '',
            'Bullet15': '',
            'Name of the document1': '',
            'Downloads1': '',
            'Name of the document2': '',
            'Downloads2': '',
            'Image1': '',
            'Image2': '',
            'Image3': '',
            'Image4': '',
            'Image5': '',
            'Image6': '',
            'Image7': '',
            'Image8': '',
            'Image9': '',
            'Image10': ''
        }
        href = 'https://ofminc.com' + str(item.get('href')).replace('/collections/all', '')
        print(href)
        # Url
        try:
            driver.get(href)
        except:
            print("driver get method error")

        individual_detail_page = driver.page_source
        individual_soup = BeautifulSoup(individual_detail_page, 'html.parser')
        print("Encoded method:", individual_soup.original_encoding)
        if len(individual_soup.find_all(name='label')) == 0:
            soup_text = str(individual_detail_page)
            meta_data_start = soup_text.find('var meta =') + 11
            meta_data_end = soup_text.find('for (var attr in meta) {') - 1
            meta_data = soup_text[meta_data_start:meta_data_end]
            meta_data = meta_data[0:meta_data.find(';')]
            meta_data = json.loads(meta_data)

            dic_data['Website'] = 'https://ofminc.com/'
            dic_data['SKU'] = meta_data['product']['variants'][0]['sku']
            dic_data['Link(from where we get info)'] = href
            dic_data['Name'] = individual_soup.find(name='h1').getText()
            if dic_data['Name'].find('Desk') != -1:
                dic_data['Type of product'] = 'Desk'
            elif dic_data['Name'].find('Chair') != -1:
                dic_data['Type of product'] = 'Chair'
            elif dic_data['Name'].find('Table') != -1:
                dic_data['Type of product'] = 'Table'
            dic_data['Model/Color'] = meta_data['product']['variants'][0]['public_title']
            dic_data['Material'] = ''
            dic_data['Price'] = int(meta_data['product']['variants'][0]['price']) / 100

            des_ele = individual_soup.find(id='product-description')
            des_text = des_ele.getText()
            if len(individual_soup.find(id='product-description').findChildren('ul')) != 0:
                bullet_ele = individual_soup.find(id='product-description').findChildren('ul')[0]
                bullet_text = bullet_ele.getText()

                index3 = 0
                for item3 in bullet_ele.findChildren('li'):
                    bullet_str = item3.getText()
                    if bullet_str.find('L x') != -1:
                        dic_data['Size'] = bullet_str[bullet_str.find('are') + 3:len(bullet_str)]
                        dic_data['Width'] = dic_data['Size'][0:dic_data['Size'].find('L x')]
                        dic_data['Depth'] = dic_data['Size'][dic_data['Size'].find('L x') + 3:dic_data['Size'].find('D x')]
                        dic_data['Height'] = dic_data['Size'][dic_data['Size'].find('D x') + 3: len(dic_data['Size']) - 2]
                    if bullet_str.find('weight capacity') != -1:
                        dic_data['Weight'] = bullet_str[0:bullet_str.find('weight capacity')]
                    dic_data['Bullet' + str(index3 + 1)] = item3.getText()
                    # item3.decompose()
                    index3 = index3 + 1
                dic_data['Description of a product (romantic)'] = '<p>' + des_text.replace(bullet_text, '') + '</p>'
            else:
                dic_data['Description of a product (romantic)'] = '<p>' + des_text + '</p>'
            download_ele = individual_soup.find('div', attrs={'class': 'product-downloads'})
            if download_ele != None:
                for item4 in download_ele.findChildren('li'):
                    if item4.getText().find('Assembly') != -1:
                        dic_data['Name of the document1'] = 'Assembly Instructions'
                        dic_data['Downloads1'] = item4.findChildren('a')[0].get('href')
                    elif item4.getText().find('Tear') != -1:
                        dic_data['Name of the document2'] = 'Tear Sheet'
                        dic_data['Downloads2'] = item4.findChildren('a')[0].get('href')
                        dic_data['Info from the file'] = dic_data['Downloads2']

            img_ele = individual_soup.find('div', attrs={'class': 'prod-thumbs'})
            index5 = 0
            for item5 in img_ele.findChildren('div'):
                if item5.has_attr('data-image'):
                    dic_data['Image' + str(index5 + 1)] = 'https:' + item5['data-image']
                if index5 == 9:
                    break
                index5 = index5 + 1
            print(dic_data)
            dic_list.append(dic_data.copy())
        else:
            index2 = 0
            for item2 in individual_soup.find_all(name='label'):
                dic_data['Website'] = 'https://ofminc.com/'
                dic_data['SKU'] = item2['data-sku']
                dic_data['Link(from where we get info)'] = href
                dic_data['Name'] = individual_soup.find(name='h1').getText()
                if dic_data['Name'].find('Desk') != -1:
                    dic_data['Type of product'] = 'Desk'
                elif dic_data['Name'].find('Chair') != -1:
                    dic_data['Type of product'] = 'Chair'
                elif dic_data['Name'].find('Table') != -1:
                    dic_data['Type of product'] = 'Table'
                dic_data['Model/Color'] = item2['data-variant']
                dic_data['Material'] = ''
                price_ele = BeautifulSoup(item2['data-price'], 'html.parser')
                dic_data['Price'] = price_ele.find(name='div', attrs={'class': 'price'}).getText()
                dic_data['Price'] = dic_data['Price'][0:dic_data['Price'].find(' ')]
                dic_data['Price'] = dic_data['Price'].replace('$', '')
                dic_data['Price'] = "".join([s for s in dic_data['Price'].strip().splitlines(True) if s.strip()])

                if price_ele.find(name='span', attrs={'class': 'compare-price'}) != None:
                    dic_data['Promo Price'] = price_ele.find(name='span', attrs={'class': 'compare-price'}).getText()
                    dic_data['Promo Price'] = dic_data['Promo Price'].replace('$', '')
                des_ele = individual_soup.find(id='product-description')
                des_text = des_ele.getText()
                if len(individual_soup.find(id='product-description').findChildren('ul')) != 0:
                    bullet_ele = individual_soup.find(id='product-description').findChildren('ul')[0]
                    bullet_text = bullet_ele.getText()

                    index3 = 0
                    for item3 in bullet_ele.findChildren('li'):
                        bullet_str = item3.getText()
                        if bullet_str.find('L x') != -1:
                            dic_data['Size'] = bullet_str[bullet_str.find('are') + 3:len(bullet_str)]
                            dic_data['Width'] = dic_data['Size'][0:dic_data['Size'].find('L x')]
                            dic_data['Depth'] = dic_data['Size'][dic_data['Size'].find('L x') + 3:dic_data['Size'].find('D x')]
                            dic_data['Height'] = dic_data['Size'][dic_data['Size'].find('D x') + 3 : len(dic_data['Size']) - 2]
                        if bullet_str.find('weight capacity') != -1:
                            dic_data['Weight'] = bullet_str[0:bullet_str.find('weight capacity')]
                        dic_data['Bullet' + str(index3 + 1)] = item3.getText()
                        # item3.decompose()
                        index3 = index3 + 1
                    dic_data['Description of a product (romantic)'] = '<p>' + des_text.replace(bullet_text, '') + '</p>'
                else:
                    dic_data['Description of a product (romantic)'] = '<p>' + des_text + '</p>'

                download_ele = individual_soup.find('div', attrs={'class': 'product-downloads'})
                if download_ele != None:
                    for item4 in download_ele.findChildren('li'):
                        if item4.getText().find('Assembly') != -1:
                            dic_data['Name of the document1'] = 'Assembly Instructions'
                            dic_data['Downloads1'] = item4.findChildren('a')[0].get('href')
                        elif item4.getText().find('Tear') != -1:
                            dic_data['Name of the document2'] = 'Tear Sheet'
                            dic_data['Downloads2'] = item4.findChildren('a')[0].get('href')
                            dic_data['Info from the file'] = dic_data['Downloads2']

                img_ele = individual_soup.find('div', attrs={'class': 'prod-thumbs'})
                index5 = 0
                print(len(img_ele.findChildren('div')))
                for item5 in img_ele.findChildren('div'):
                    print(item5.get('data-featured-set'))
                    if index5 == 9:
                        break
                    if item5.get('data-featured-set') == 'Item-' + str(index2 + 1) and item5.has_attr('data-image'):
                        print(item5)
                        dic_data['Image' + str(index5 + 1)] = 'https:' + item5['data-image']
                    else:
                        continue
                    index5 = index5 + 1
                print(dic_data)
                dic_list.append(dic_data.copy())
                index2 = index2 + 1

keys = dic_list[0].keys()
for item in dic_list:
    with open(str(file_name), 'a+', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        if index == 0:
            dict_writer.writeheader()
            index = index + 1
        dict_writer.writerow(item)