# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:02:22 2021

@author: choua
"""

#import packages
import pandas as pd
import os

#for url support
import requests
from bs4 import BeautifulSoup
import datetime


def find_article(url):
    try:
         page=requests.get(url, allow_redirects=True)  # this might throw an exception if something goes wrong.
         
         soup = BeautifulSoup(page.text, "html.parser")
         text = soup.find_all('p') #find all text
         
         return text
    # this describes what to do if an exception is thrown
    except Exception as e:
        return 


if __name__== "__main__":
    #get the files
    s_c = pd.read_csv('edited_data/covid_links.csv')
    s_e = pd.read_csv('edited_data/ebola_links.csv')
    
    dir_path = os.path.dirname(os.path.realpath(__file__)) #filepath
    
    #parse url
    dataset.iloc[data]["publish_date"].split()[0].split("-")[1]
    
    
    
    
    
    #dump into text files
    dir_path = os.path.dirname(os.path.realpath(__file__)) #filepath
    
    #dump into csv files
    s_c.to_csv(os.path.join(dir_path,'edited_data/media_covid_edited.csv'), index=False)
    s_e.to_csv(os.path.join(dir_path,'edited_data/media_ebola_edited.csv'), index=False)