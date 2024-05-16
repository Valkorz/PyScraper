import json
import pandas as pd
import scraper

outputDir = "data/"

def scrapeFrom(target : str, returnAvg = True): 
    with open("config/webConfig.json") as f:
        data = json.load(f)
    
    websites = list(data['Websites'].items())
    dataList = []
    
    for i in range(len(data['Websites'])):
        itemPrice = websites[i][1]['ItemPrice']
        print(itemPrice)
        print(websites[i][1]['Url'])
        
        dataList = {"url" : websites[i][0], "data" : scraper.scrapePrices(websites[i][1]['Url'], target, itemPrice['Attribute'],
                             itemPrice['PriceTag'], itemPrice['PriceClass'], 
                             itemPrice['NameTag'], itemPrice['NameClass'], False)}
        
    return dataList

def avg(dataList, target : str):
    prices = [item['price'] for item in dataList['data']]
    names = [item['name'] for item in dataList['data']]
    print(prices, names)
    return scraper.format(prices, names, target)

def toSheet():
    print("todo")