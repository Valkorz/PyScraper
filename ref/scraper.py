import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs

#Webscraper for the site: Mercado livre
def scrapePrices(target : str, form = True):
    url = f"https://lista.mercadolivre.com.br/{target.replace(' ', '-')}"
    response = requests.get(url)
    
    
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')  
        prices = []
        items = soup.find_all('div', class_='ui-search-result__content-wrapper')
        data = []
        for item in items:
            name = item.find('h2', class_='ui-search-item__title').text.strip()
            print(name)
            price_element = item.find('span', class_='andes-money-amount__fraction')
            if price_element:
                price = float(price_element.text.replace('.', '').replace(',', '.'))
                print(price)
                data.append({'name': name, 'price': price})
                
        prices = [item['price'] for item in data]
        names = [item['name'] for item in data]
        if form: return format(prices, names, target, 2)
        else: return data
    else:
        print("Error. Could not reach ", url)
        return []
    
#Remove outliers and return average
def format(prices : float, names : str, target : str, treshold = 2):
    
    filtered_prices = []
    for price, name in zip(prices, names):
        if target.lower() in name.lower():
            if "kit" in name.lower() or "devkit" in name.lower() or "conjunto" in name.lower(): continue
            else: filtered_prices.append(price)
    
    meanPrice = np.mean(filtered_prices)
    stdDev = np.std(filtered_prices)
    
    lowerLimit = meanPrice - treshold * stdDev
    upperLimit = meanPrice + treshold * stdDev
    
    filtered_prices = [price for price in prices if lowerLimit <= price <= upperLimit]
    
    return filtered_prices
