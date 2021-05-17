"""
Author: Adam Chou


Readme:
    
    Program dedicates itself to sorting csv documents into a parsable form. 
    All dates that are not identifiable within the given range for each are
    removed. Data is then sorted such that dates are in descending order 
    from recent to not so recent.

"""

#import packages
import pandas as pd
import os
import numpy as np
from time import time

#for url support
import requests
from bs4 import BeautifulSoup
import datetime

#retrieve missing dates/time
def find_time(url):
    # print("attempting to find date")
    try:
         page=requests.get(url, allow_redirects=True)  # this might throw an exception if something goes wrong.
         
         soup = BeautifulSoup(page.text, "html.parser") #find all text - scrapped # text = soup.find_all('p')
         #convert object to string
         time=""
         for node in soup.findAll('time'):
             time +=''.join(node.findAll(text=True))
             if len(time)>0:
                 break
         time = str(time) #change datetime
         if len(time) > 3:
             #if you cant find 2020 or 2019
             if time.find("2020") == -1 and time.find("2019") == -1:
                 #see what month it is
                 for i in ("November","December", "January", "February", "March", "April", "June", "July"):
                     #if its a match
                     if time.find(i) > -1:
                         #find if its november or december
                         if time.find("November") == -1 or time.find("December") ==-1:
                             time = time+ ", 2019"
                         else:
                             time = time+ ", 2020"
                 time = " " + str(time.strip())
             #else, make the time
             time = str(datetime.datetime.strptime(time.strip(), "%B %d, %Y"))
         else: 
              return "0000-00-00 00:00:00"
         return time
    # this describes what to do if an exception is thrown
    except Exception as e:
        return "0000-00-00 00:00:00"
    
def change_date(data):
        #replace bad data
        data.fillna(0)
        data.replace([float("Nan"),np.nan,"undateable", ""],"0000-00-00 00:00:00", inplace=True)
        for i in range(len(data)):
            if data.iloc[i]["publish_date"] == "0000-00-00 00:00:00": #if date is unavailable
                data.at[i,"publish_date"] = find_time(data.iloc[i]["url"]) #then find it
            #check month
            month_checker = data.iloc[i]["publish_date"].split()[0].split("-")
            if (month_checker[0] == "2019") and (month_checker[1] in ("01", "02","03", "04", "05", "06","07")):
                print("x",sep="",end="")
                data.at[i,"publish_date"] = "2020-" + str(month_checker[1]) + "-" + str(month_checker[2]) + " 00:00:00" #format is year, month, day
            
        return data

if __name__== "__main__":
    start_time = time() #start time
    dir_path = os.path.dirname(os.path.realpath(__file__)) #filepath
    
    pd.set_option('display.max_columns', None) #configure show all columns

    print ("reading files!") #upload covid stories
    s_c = pd.read_csv('original_data/media_covid.csv')
    s_e = pd.read_csv('original_data/media_ebola.csv')
    
    #edit media list to drop all inconvenient columns
        #create array of strings to filter
    delete_list = ["stories_id","media_id","media_inlink_count","inlink_count","outlink_count","post_count","author_count", "channel_count"]
        #delete them
    s_c = s_c.drop(columns=delete_list)
    s_e = s_e.drop(columns=delete_list)
    
    date_count = {} #dictionary for couting dates
    #replace bad dates
    print("changing dates!\n")
    s_c = change_date(s_c)
    s_e = change_date(s_e)
    
    s_c = s_c[~s_c.publish_date.str.contains("0000")]
    
    s_e = s_e[~s_e.publish_date.str.contains("0000")]
    
    #dump into csv files
    s_c.to_csv(os.path.join(dir_path,'edited_data/media_covid_edited.csv'), index=False)
    s_e.to_csv(os.path.join(dir_path,'edited_data/media_ebola_edited.csv'), index=False)
    
    print ("finished  moving files!")
    print("Program took", str(datetime.timedelta(seconds=time() - start_time))