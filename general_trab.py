#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from googlesearch import search


links = []
query = 'https://www.dafiti.com.br/campanha-'
i = 0
for j in search(query, tld="com.br", num=50, pause=2): 
	if j.startswith('https://www.dafiti.com.br/campanha-'):
                links.append(j)

for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')

        products = soup.find_all('div', class_='product-box')

        sku_array = []

        for product in products[1:]:
                sku = product.find_all('div', class_='product-box-image')[0].get('id')
                
                sku_array.append(sku)

                preco = product.find_all('span', class_='product-box-price-from')[0]\
                        .getText()
                desconto = True if product.find_all(
                        'span', class_='product-box-price-to') else False
                produto_novo = True if product.find_all(
                        'div', class_='product-new-info') else False

        try:
                with open('sku_anterior_' + link.split('/')[3] + '.csv', 'r') as x:
                        sku_anterior = x.read().split(';\n')
        except:
                sku_anterior = []

        print set(sku_array) - (set(sku_anterior) & set(sku_array))

        with open('sku_anterior_' + link.split('/')[3] +'.csv', 'w') as x:
        	x.write(';\n'.join(sku_array))