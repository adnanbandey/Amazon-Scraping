print('start')

#from urllib.parse import urlparse
import os
import time
#import requests
from selenium import webdriver
import time
import math, requests, json
from datetime import datetime
from datetime import date

from gspread_pandas import Spread,Client
from datetime import timedelta
#from sqlalchemy import create_engine
#import psycopg2 
import io
import numpy as np
import pandas as pd

#import warnings
#warnings.filterwarnings('ignore')
import re
import schedule
from bs4 import BeautifulSoup

import schedule
import time

print('start1')

def job():
    now = datetime.now()
    d_1=date.today()

    d_11=d_1.strftime("%Y-%m-%d")
    print(d_11)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
    #browser = webdriver.Chrome()

    fd=pd.DataFrame(columns=['Ranking', 'Name', 'ASIN', 'Prices', 'Actual Price', 'Discount', 'Tags',
           'Ads', 'Brand', 'Number of ratings', 'Overall Rating',
           'Per Litre Price', 'Date', 'Keyword'])

    hour=int(datetime.now().strftime('%H'))

    url = "https://www.amazon.in"
    browser.get(url)
    time.sleep(2)

    pins=['560001']

    for pin in pins:

        #click to change pincode
        click=browser.find_element_by_xpath('//*[@id="nav-global-location-popover-link"]')
        click.click()
        time.sleep(4)

        #Enter pincode
        password=browser.find_element_by_id('GLUXZipUpdateInput')
        time.sleep(1)
        password.send_keys(pin)

        #click to apply new pincode
        click1=browser.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input')
        click1.click()
        time.sleep(1)

        stock=[]
        sold_by=[]
        fulfilled_by=[]
        ASIN=[]
        name=[]
        pincodes=[]
        asins=['B0866MZWBS','B0866ML94L','B0866MVRBT','B08N7HBMBC','B08N7JKLQ7','B0866ML94M']
        for i in asins:
            url = "https://www.amazon.in/dp/" + str(i)
            browser.get(url)

            html=browser.page_source
            soup = BeautifulSoup(html, "html.parser")

        #--------------------------#
            try:
                stock.append(soup.find("span", {"class": "a-size-medium a-color-success"}).get_text(strip=True))
            except:
                stock.append('None')
        #--------------------------#        
            try:
                sold_by.append(soup.find('a',{"id": "sellerProfileTriggerId"}).get_text())
            except:
                sold_by.append('None')
        #---------------------------#        
            try:
                fulfilled_by.append(soup.find('a',{"id": "SSOFpopoverLink"}).get_text())
            except:
                fulfilled_by.append('None')    
        #---------------------------#        
            try:
                ASIN.append(i)
            except:
                ASIN.append('None')
        #---------------------------#
            try:
                name.append(soup.find("span", {"class": "a-size-large product-title-word-break"}).get_text(strip=True))
            except:
                name.append('None')
        #----------------------------#
            try:
                pincodes.append(pin)
            except:
                pincodes.append('None')

            time.sleep(2)    

    df=pd.DataFrame(list(zip(stock,sold_by,fulfilled_by,ASIN,name,pincodes)),columns=['Availability','Seller','Fulfilled by','ASIN','Name','PIN'])
    df['Date']=d_1.strftime("%Y-%m-%d")        

    my_credentials= {
      }

    spread = Spread('IFB ASIN TRACKING',config=my_credentials) ## worksheet_name
    sheet=spread.open_sheet("Data") ##sheet_name
    table_updated=spread.sheet_to_df(sheet=sheet,index=0)
    x=table_updated.shape[0]

    # spread.df_to_sheet(df,index=False,start=(1,1),headers=True)
    spread.df_to_sheet(df,index=False,start=(x+2,1),headers=False)
    print('Pushed to ghseet')
    print(d_11)

    # schedule.every(10).seconds.do(job)
schedule.every(50).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every(5).to(10).minutes.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
