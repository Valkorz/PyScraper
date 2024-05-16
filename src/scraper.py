import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Scrape target website with defined search query and html elements from webConfig.json
def scrapePrices(url : str, target : str, attribute : str, 
                 priceTag : str, priceClass : str, 
                 nameTag : str, nameClass: str, form = True):
    
    newUrl = url + target.replace(' ', '-')
    print(newUrl)
    response = requests.get(newUrl)
    
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        prices = []
        items = soup.find_all('div', class_=attribute)
        data = []
        for item in items:
            name = item.find(nameTag, class_=nameClass).text.strip()
            price_element = item.find(priceTag, class_=priceClass)
            if price_element:
                price = float(price_element.text.replace('.', '').replace(',','.'))
                data.append({'name': name, 'price': price})
        
        prices = [item['price'] for item in data]
        names = [item['name'] for item in data]
        if form: return format(prices, names, target, 2)
        else: return data
    else:
        if response.status_code == 503:
            print(503, ": Access denied.")
        else:
            print("Error", response.status_code, " in ", url)
        return []

def scrapeImage(url : str, target : str, imageClass : str):
    driver = webdriver.Firefox()
    newUrl = url + target.replace(' ', '-')
    response = requests.get(newUrl)
    driver.get(newUrl)
    img = None
            
    try:
    # Wait up to 10 seconds for the page to load
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, imageClass))
        )
    finally:
        # Now that the page is loaded, we can scrape the image
        img = driver.find_element_by_class_name(imageClass).get_attribute('src')
        print(img)
    
    driver.quit()
    return img
    
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

    
