from urllib.parse import urlparse
import time
import requests
from selenium import webdriver
import time
import math, requests, json
from scrapy.http import HtmlResponse
from datetime import datetime
from datetime import date

from gspread_pandas import Spread,Client
from datetime import timedelta
from sqlalchemy import create_engine
import psycopg2 
import io
import numpy as np
import pandas as pd
import requests
import warnings
warnings.filterwarnings('ignore')
import re
import schedule
from bs4 import BeautifulSoup

from selenium import webdriver
import os

print('start')

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

print('start1')

def job():
    now = datetime.now()
    d_1=date.today()

    d_11=d_1.strftime("%Y-%m-%d")
    print(d_11)


    browser = webdriver.Chrome()

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
      "type": "service_account",
      "project_id": "seraphic-gate-272015",
      "private_key_id": "598e7888e72a5b1392b28f6703a863b81f41aa0f",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDN9plscATX/Kx/\nbxNPWNP5LkPJKFAsZcZYdkrh78E7FuHXcHEorBY/uKY33xo3LWKpDq2DxfT5JPeQ\nSR4OQUkbTG+B0YmIdqCdp4FEliZuHIO9zWPDpGbEfnwIlgT4zjmUixKSc2g2pjb1\nF5dCwD9ixRq3brY29OINao9lbHUBqs7EVRqJwOkFv2mmZASGPgaaKSBHD5PoazjC\nw5ndec1w0aZgzbPqgcaRb4Xtmp+mt0lSfJf4IkAhKHiuUdrMfwJSUcukjHXBdD/v\nQyuXp2IX0cDrzBJQ8da2Oli/1yDf02xeX3+AqryghuZu9jb4cBwVoAkODpln87GD\nQW0C2nD/AgMBAAECggEAJwELPwDbufdsx1lGo+Eji23agm6y+CVx8XC9b5oS0tjb\nfgwaMeSc9gZG3A/RDB/5LiDMdUb4xHHevCFMotB0Qsov17rRu9kTQ6fkEBQLRRD7\nVedefD9XAuEdJhca6+9J8jqAEuHuG2NQxwtnpsl3d4HyNEiwEyo+4OGMNF3crqrN\n1llxxHtFlnYe6Ez6rzC3T452lq8XhUb3cChfvTRv9S7EoG/yoXXKZlCz/N0+BJ5Z\nLFbRbkEvXkkh2N5z2TlBRpSY5ybFz9ZULOSm3PP3E/4jQOYPM4aXmsLQzasuHJYV\nfqf9fB+oZob0XviceV7LBvN2uxYDwQDkQ7KBSGyeCQKBgQD7icWmzTSH4RGIIFev\nf/hsj8j9QbsjxDwXMe/K8qRyIyOheB0gpNWuSOJ8CsvGmot50FAZ7GYNlHDQ/OYy\no0tgzkq+TfPdFWJQaTomPWLSxl8b833qgPixOE9XYd7PJyHjGLBXEiVQ54CojO0B\nW2ynFTKTlwliBbz254IVQlqJCwKBgQDRnd92FunxBWo3nIimidJepnFrS1gQbNJm\nC1rVdvf8XaaOYfwG5d9VuohpdYryVsVcepqacpFnjQ7Huf7Au/Wtm0GKN+49aATm\nMhZkY4Me1zqtvFDgTsAMcY3H6Ui/dhCQAH3goJRilMvZY/G/XCLyMP5jxr+ann4n\nfEaNYhz4XQKBgQCltdrfi5rK1Yx+OIhr1wurQYJwzefipTnNMhm+guGxS9MCYiYW\nRmF7YwrKGzaqDVBLnN/YZDPLSHqWQ7XHsGpNSTpWavZ4NMlDHj+vx4sePo+T03Kl\nlffAkM88Sv7FTAt4F+C8S/kHdqv83nKZDUjkPgPG1Z7Z09vscRHyvXb1hwKBgBEg\nsECq8KSkB6DRpozNGCZpvTzCJEj7S1nRNbPZi7vQPyrFMN2zbMNJgZn0Y80Xb/r1\nfap/EAiBCyMgvIMtGI7976YGme3kkPnqP9AmHXGorn/Bsm4RoTmjEa2zDyGt2P6b\nO63eESHY/KsfsoIrWiOmAzNN6xwMNUyup+kniix1AoGBAKwbIytBL0mF1Lu9vCDb\nNCb7cEa1N5pf/fbcpOsIPmeXcpOm3BlUi3M3R6tB8ycJcIzXK8mKvZHAUsjFoE5U\nwo9H+J92SgxwDUNYv4bNw5MSVBU5apdgrZFWqm75UdMeRyJ/ykZ9VEo5PX2NK5H/\nBGzLrSf8o4euuIKSigJPDtXs\n-----END PRIVATE KEY-----\n",
      "client_email": "adnan-348@seraphic-gate-272015.iam.gserviceaccount.com",
      "client_id": "116030486813332346226",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/adnan-348%40seraphic-gate-272015.iam.gserviceaccount.com"
      }

    spread = Spread('IFB ASIN TRACKING',config=my_credentials) ## worksheet_name
    sheet=spread.open_sheet("Data") ##sheet_name
    table_updated=spread.sheet_to_df(sheet=sheet,index=0)
    x=table_updated.shape[0]


    # spread.df_to_sheet(df,index=False,start=(1,1),headers=True)
    spread.df_to_sheet(df,index=False,start=(x+2,1),headers=False)
    print('Pushed to ghseet')
    print(d_11)
    
    schedule.every().minute.at(":17").do(job)
    #schedule.every().day.at('09:00').do(job)
    
while True:
    schedule.run_pending()
    time.sleep(1) # wait one minute
