# -*- coding: utf-8 -*-
"""
Author: Adam Chou

Readme:
    
    This program serves as a randomizer to select a range of dates
    within the prescribed edited media csv files. It uses random.systemrand()
    to make use of binary randomness, and then selects 20 articles from a range
    including articles from the aforementioned CSV.
    
"""

import pandas as pd
import random
import os

def range_finder(dataset, early, peak, end):
    
    grab_dates = { str(early) : ["unfilled","unfilled"],
                   str(peak) : ["unfilled","unfilled"], 
                   str(end) : ["unfilled","unfilled"]} #get the index of various months
    
    for data in range(len(dataset)): # for all data in dataset, classify it by date
        current_month = dataset.iloc[data]["publish_date"].split("-")[1] #get the publish date month
        if current_month in grab_dates.keys(): #find first and last date
            if grab_dates[current_month][0] == "unfilled":
                grab_dates[current_month][0] = data #first date
            else:
                grab_dates[current_month][1] = data
                
    def random_sample(num, low_range, high_range):
        total_samples = [] #hold random numbers
        
        while(len(total_samples)<num):
            sample = random.SystemRandom().randint(low_range,high_range)
            if sample not in total_samples:
                total_samples.append(int(sample))
        return total_samples
    
    for i in grab_dates.keys():
        temp_range = 20 #grab 20 samples
        grab_dates[i] = random_sample(temp_range, grab_dates[i][0], grab_dates[i][1])
    
    return grab_dates

def new_dataset(dataset):
    dataframe = pd.DataFrame(columns = dataset.columns) #new dataframe
    for data in range(len(dataset)): #check if its the month we need
        for i in dates.keys(): #if there is a match for the indexx and the month
            if data in dates[i]:
                dataframe = dataframe.append(dataset.iloc[data],ignore_index = True) #store row into array
    return dataframe

if __name__ == "__main__":
    print("reading files")
    s_c = pd.read_csv("edited_data/media_covid_edited.csv")
    s_e = pd.read_csv("edited_data/media_ebola_edited.csv")
    
    
    print("removing misc info....\n")
    s_c.drop(s_c[s_c['publish_date'] == "0000-00-00 00:00:00"].index, inplace = True)  
    s_e.drop(s_e[s_e['publish_date'] == "0000-00-00 00:00:00"].index, inplace = True)
    s_c = s_c[s_c.facebook_share_count != 0] #remove facebook shares not 0
    s_e = s_e[s_e.facebook_share_count != 0] #remove facebook shares not 0
    s_c = s_c.sort_values(by=["publish_date"], ascending=False)
    s_e = s_e.sort_values(by=["publish_date"], ascending=False)
    
    print("finding peaks for covid") #peaks for covid
    dates = range_finder(s_c, "01","03","06")
    n_s_c = new_dataset(s_c)
    print("finding peaks for ebola") #peaks for ebola
    dates = range_finder(s_e, "08","10","12")
    n_s_e = new_dataset(s_e)
    
    print("exporting files!") #export
    dir_path = os.path.dirname(os.path.realpath(__file__)) #filepath
    n_s_c.to_csv(os.path.join(dir_path,'edited_data/covid_links.csv'), index=False)
    n_s_e.to_csv(os.path.join(dir_path,'edited_data/ebola_links2.csv'), index=False)
    print("finished exporting, see you soon!")