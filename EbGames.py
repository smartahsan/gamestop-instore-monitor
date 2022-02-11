import time
import datetime
from datetime import datetime
from threading import Thread
import requests
import json
import sys
import time
import csv

from discord_webhook import DiscordWebhook, DiscordEmbed

import colorama
from colorama import Fore, Back, Style
colorama.init()

# import config file
with open("config.csv", "r") as fd:
    next(fd)
    for line in fd.readlines():
        line = line.strip()
        if not line:
            continue
        global discordWebhook,delay
        seperator = line.split(",")
        discordWebhook = seperator[0]
        delay = seperator[1]

def instockWebhook(ProductID, ProductStatus, StoreName, Address, City, Province, Phone, imageUrl):
    webhook = DiscordWebhook(url=discordWebhook, username="EB Games Instore Monitor")
    embed = DiscordEmbed(color=14145495)
    embed.set_author(name='Store Has Stock!', icon_url='https://pbs.twimg.com/profile_images/1403834602490417154/am6u1CL5_400x400.jpg')
    embed.set_footer(text='Powered By anhbro#5696 | EB Games In Store')
    embed.set_thumbnail(url=imageUrl)
    embed.set_timestamp()
    embed.add_embed_field(name='Product ID', value=""+ProductID+"")
    embed.add_embed_field(name='Product Status', value=""+ProductStatus+"")
    embed.add_embed_field(name='Store Name', value=""+StoreName+"")
    embed.add_embed_field(name='Address', value=""+Address+"")
    embed.add_embed_field(name='City', value=""+City+"")
    embed.add_embed_field(name='Province', value=""+Province+"")
    embed.add_embed_field(name='Phones', value=""+Phone+"")
    webhook.add_embed(embed)
    response = webhook.execute()

def main(productId,imageUrl):

    print('\033[34m' + ('[' + datetime.now().strftime("%H:%M:%S.%f") + '] ['+productId+'] initializing monitor'))

    payload={}

    headers = {
    'authority': 'www.gamestop.ca',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'accept': '*/*',
    'x-newrelic-id': 'Vw4FUFNRGwEEVlVTAwEF',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.gamestop.ca/StoreLocator/Index?productId={productId}',
    'accept-language': 'en-US,en;q=0.9',
    }

    try:

        r = requests.get(f'https://www.gamestop.ca/StoreLocator/GetStoresForStoreLocatorByProduct?value={productId}&skuType=1&language=en-CA', headers=headers, data=payload)

        json_object = r.json()
    
    except Exception as e:

        print('\033[31m' + ('[' + datetime.now().strftime("%H:%M:%S.%f") + '] [ERROR] ['+productId+'] Unknown error initializing monitor' + str(e)))

    while True:
        try:

            print('\033[33m' + ('[' + datetime.now().strftime("%H:%M:%S.%f") + '] ['+productId+'] Monitoring'))

            payload={}

            headers = {
            'authority': 'www.gamestop.ca',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'accept': '*/*',
            'x-newrelic-id': 'Vw4FUFNRGwEEVlVTAwEF',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://www.gamestop.ca/StoreLocator/Index?productId={productId}',
            'accept-language': 'en-US,en;q=0.9',
            }


            r2 = requests.get(f'https://www.gamestop.ca/StoreLocator/GetStoresForStoreLocatorByProduct?value={productId}&skuType=1&language=en-CA', headers=headers, data=payload)

            json_object2 = r2.json()

            #Comparing previous response to new response to identify any changes in product availability

            for x in json_object:

                for y in json_object2:
                
                    if x['Id'] == y['Id']:

                        if x['ProductStatus'] != y['ProductStatus'] and y['ProductStatus'] == 'available':

                            print('\033[32m' + ('[' + datetime.now().strftime("%H:%M:%S.%f") + '] ['+productId+'] [Store '+str(y['Id'])+'] Product In Stock!'))
                            
                            ProductID = productId
                            ProductStatus = y['ProductStatus']
                            StoreName = y['Name']
                            Address = y['Address']
                            City = y['City']
                            Province = y['Province']
                            Phone = y['Phones']
                        
                            instockWebhook(ProductID, ProductStatus, StoreName, Address, City, Province, Phone, imageUrl)

            json_object = r2.json()

            time.sleep(int(delay))
        
        except Exception as e:
            
            print('\033[31m' + ('[' + datetime.now().strftime("%H:%M:%S.%f") + '] [ERROR] ['+productId+'] Unknown error monitoring ' + str(e)))
            time.sleep(3)
            continue

# Store threads
threads = []

def threadProducts():
    with open("products.csv", "r") as fd:
        next(fd)
        for line in fd.readlines():
            line = line.strip()
            if not line:
                continue
            task = line.split(',')
            productId = task[0]
            imageUrl = task[1]
            
            while True:
                try:   
                    t = Thread(target=main, args=(productId,imageUrl))
                    break
                except:
                    print('\033[31m' + ('[' + datetime.now().strftime("%H:%M:%S.%f") + '] [ERROR] ['+productId+'] Unknown error initializing monitor... Retrying'))
                    continue

            t.start()

            threads.append(t)                
        
threadProducts()

for t in threads:
    t.join()



