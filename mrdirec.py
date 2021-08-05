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

scraping_urls = [
    {
        'url': 'https://www.mrdirectint.com/catalog/sink/kitchen',
        'file_name': 'sink-kitchen.csv'
    },
    {
        'url': 'https://www.mrdirectint.com/catalog/sink/bathroom',
        'file_name': 'sink-bathroom.csv'
    },
    {
        'url': 'https://www.mrdirectint.com/catalog/faucet/kitchen',
        'file_name': 'faucet-kitchen.csv'
    },
    {
        'url': 'https://www.mrdirectint.com/catalog/faucet/bathroom',
        'file_name': 'faucet-bathroom.csv'
    },
    {
        'url': 'https://www.mrdirectint.com/catalog/faucet/shower-tub',
        'file_name': 'faucet-shower-tbb.csv'
    },
    {
        'url': 'https://www.mrdirectint.com/catalog/accessory/kitchen',
        'file_name': 'accessory-kitchen.csv'
    },
    {
        'url': 'https://www.mrdirectint.com/catalog/accessory/bathroom',
        'file_name': 'accessory-bathroom.csv'
    },
    # {
    #     'url': 'https://www.mrdirectint.com/catalog/faucet-accessories',
    #     'file_name': 'accessory-faucet.csv'
    # },
    # {
    #     'url': 'https://www.mrdirectint.com/catalog/accessory/pro-care',
    #     'file_name': 'accessory-pro-care.csv'
    # }
]

host_name = 'https://www.mrdirectint.com'

dic_data_keys = [
    'Link',
    'Full Name',
    'SKU',
    'Summary',
    'Price Currency',
    'Price',
    'Availability',
    'PriceValidUntil',
    'Aggregate Rating',
    'Review Count',
    'Available Finishes / Color',
    'Feature 1',
    'Feature 2',
    'Feature 3',
    'Feature 4',
    'Feature 5',
    'Feature 6',
    'Feature 7',
    'Feature 8',
    'Feature 9',
    'Feature 10',
    'Feature 11',
    'Feature 12',
    'Feature 13',
    'Feature 14',
    'Feature 15',
    'Image 1',
    'Image 2',
    'Image 3',
    'Image 4',
    'Image 5',
    'Image 6',
    'Image 7',
    'Image 8',
    'Image 9',
    'Image 10',
    'Image 11',
    'Image 12',
    'Image 13',
    'Image 14',
    'Image 15',
    'Image 16',
    'Image 17',
    'Image 18',
    'Image 19',
    'Image 20',
    'Specifications',
    'Faucet Installation',
    'cUPC Certification',
    'NSF Certification',
    'Lead Free',
    'Undermount Installation',
    'Flush DXF',
    'Full DXF',
    'Negative DXF',
    'Water Sense',
    'Topmount Installation',
    'Apron Installation',
    'Undermount To Laminate Installation',
    'Warranty',
    'Care and Cleaning Manual',
    'ICC Certification',
    'Installation',
    'Specification',
    'Vessel Installation'
]

dic_data = {}
dic_list = []

def removeBreakLineFromStr(str):
    return "".join([s for s in str.strip().splitlines(True) if s.strip()])

def getProductInfo(dic_data_keys, scraping_url, page_num, file_name):
    print(page_num)
    product_list_page_url = scraping_url + "?sd=0&p=" + str(page_num)
    product_list_page = urllib.request.urlopen(product_list_page_url)
    product_list_page_soup = BeautifulSoup(product_list_page, 'html.parser')
    product_list_li = product_list_page_soup.find_all(name='li', attrs={'class': 'c-categoryProducts--product'})
    print(len(product_list_li))
    for product_item in product_list_li:
        dic_data = {key: "" for key in dic_data_keys}
        print(product_item.findChildren('a', attrs={'class': 'o-productListing--image'}))
        if product_item.findChildren('a', attrs={'class': 'o-productListing--image'}) == []:
            continue
        print(product_item.findChildren('a', attrs={'class': 'o-productListing--image'})[0]['href'])
        # exit()
        product_detail_href = product_item.findChildren('a', attrs={'class': 'o-productListing--image'})[0]['href']
        product_detail_page = urllib.request.urlopen(host_name + product_detail_href)
        product_detail_soup = BeautifulSoup(product_detail_page, 'html.parser')
        available_finish_li = product_detail_soup.find_all('li', attrs={'class': 'o-productRelated--item'})
        if len(available_finish_li) != 0 and available_finish_li != None:
            for indexi in range(0, len(available_finish_li)):
                sub_product_href = available_finish_li[indexi].findChildren('a', attrs={'class': 'o-productRelated--link'})[0]['href']
                sub_product_page = urllib.request.urlopen(host_name + sub_product_href)
                sub_product_soup = BeautifulSoup(sub_product_page, 'html.parser')
                if str(sub_product_soup.find('script', type='application/ld+json')) != '<script type="application/ld+json"></script>':
                    script_data = json.loads(sub_product_soup.find('script', type='application/ld+json').contents[0])
                    dic_data['Link'] = host_name + sub_product_href
                    dic_data['Full Name'] = script_data['name']
                    dic_data['SKU'] = script_data['sku']
                    dic_data['Summary'] = script_data['description']
                    dic_data['Price Currency'] = script_data['offers']['priceCurrency']
                    dic_data['Price'] = script_data['offers']['price']
                    dic_data['Availability'] = script_data['offers']['availability']
                    dic_data['PriceValidUntil'] = script_data['offers']['priceValidUntil']
                    dic_data['Aggregate Rating'] = script_data['aggregateRating']['ratingValue']
                    dic_data['Review Count'] = script_data['aggregateRating']['reviewCount']
                    dic_data['Available Finishes / Color'] = available_finish_li[indexi].findChildren('span')[0].getText()

                features = sub_product_soup.find_all('li', attrs={'class': 'c-productSpecifications--item'})
                for index in range(0, len(features)):
                    dic_data['Feature ' + str(index + 1)] = removeBreakLineFromStr(features[index].getText())

                images = sub_product_soup.find('ul', attrs={'id': 'feature_nav'}).findChildren('img')
                for index in range(0, len(images)):
                    dic_data['Image ' + str(index + 1)] = host_name + images[index].get('src')

                download_items = sub_product_soup.find_all('li', attrs={'class': 'c-productSupport-download-item'})
                for index in range(0, len(download_items)):
                    download_item = download_items[index].findChildren("a")[0]
                    dic_data[removeBreakLineFromStr(download_item.getText())] = host_name + download_item['href']

                print(dic_data)
                dic_list.append(dic_data)

                with open("mrdirec_result/" + file_name, 'a', newline='', encoding='utf-8-sig') as output_file:
                    dict_writer = csv.DictWriter(output_file, dic_data_keys)
                    dict_writer.writerow(dic_data)
        else:
            if str(product_detail_soup.find('script',
                                         type='application/ld+json')) != '<script type="application/ld+json"></script>':
                script_data = json.loads(product_detail_soup.find('script', type='application/ld+json').contents[0])
                dic_data['Link'] = host_name + product_detail_href
                dic_data['Full Name'] = script_data['name']
                dic_data['SKU'] = script_data['sku']
                dic_data['Summary'] = script_data['description']
                dic_data['Price Currency'] = script_data['offers']['priceCurrency']
                dic_data['Price'] = script_data['offers']['price']
                dic_data['Availability'] = script_data['offers']['availability']
                dic_data['PriceValidUntil'] = script_data['offers']['priceValidUntil']
                dic_data['Aggregate Rating'] = script_data['aggregateRating']['ratingValue']
                dic_data['Review Count'] = script_data['aggregateRating']['reviewCount']

            features = product_detail_soup.find_all('li', attrs={'class': 'c-productSpecifications--item'})
            for index in range(0, len(features)):
                dic_data['Feature ' + str(index + 1)] = removeBreakLineFromStr(features[index].getText())

            images = product_detail_soup.find('ul', attrs={'id': 'feature_nav'}).findChildren('img')
            for index in range(0, len(images)):
                dic_data['Image ' + str(index + 1)] = host_name + images[index].get('src')

            download_items = product_detail_soup.find_all('li', attrs={'class': 'c-productSupport-download-item'})
            for index in range(0, len(download_items)):
                download_item = download_items[index].findChildren("a")[0]
                dic_data[removeBreakLineFromStr(download_item.getText())] = host_name + download_item['href']

            print(dic_data)
            dic_list.append(dic_data)

            with open("mrdirec_result/" + file_name, 'a', newline='', encoding='utf-8-sig') as output_file:
                dict_writer = csv.DictWriter(output_file, dic_data_keys)
                dict_writer.writerow(dic_data)


for index in range(0, len(scraping_urls)):
    # Create csv file
    print(scraping_urls[index]['file_name'])
    if os.path.exists('mrdirec_result/'+scraping_urls[index]['file_name']):
        os.remove('mrdirec_result/' + scraping_urls[index]['file_name'])
    with open(str('mrdirec_result/' + scraping_urls[index]['file_name']), 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, dic_data_keys)
        dict_writer.writeheader()
    # Number of items per page and Number of pages
    first_page_url = scraping_urls[index]['url'] + "?sd=0&p=1"
    first_page = urllib.request.urlopen(first_page_url)
    first_page_soup = BeautifulSoup(first_page, 'html.parser')
    product_count = first_page_soup.find('div', attrs={'class': 'o-pager--range'})

    if product_count is None:
        print("hazard")
        getProductInfo(dic_data_keys, scraping_urls[index]['url'], 1, scraping_urls[index]['file_name'])
    else:
        product_count = product_count.getText()
        number_per_page = product_count[product_count.find('- ') + 2: product_count.find('of') - 1]
        number_per_page = int(number_per_page)
        total_num = product_count[product_count.find('of') + 3: product_count.find('Results') - 1]
        total_num = int(total_num)
        print(total_num)
        print(number_per_page)
        print(int((total_num - total_num % number_per_page) / number_per_page))
        for page_num in range(0, int((total_num - total_num % number_per_page) / number_per_page) if total_num % number_per_page == 0 else int((total_num - total_num % number_per_page) / number_per_page) + 1):
            getProductInfo(dic_data_keys, scraping_urls[index]['url'], page_num + 1, scraping_urls[index]['file_name'])


