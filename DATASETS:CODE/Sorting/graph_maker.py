# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 11:54:46 2021

@author: choua
"""

#import packages
import pandas as pd
import os
from time import time
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
#this takes so long, going to try threading
import threading

#functions
def get_outlet_article_count(data):
        #create dictionary
        outlet_count = {}
        for i in range(0,len(data)):
            #get the outlet
            temp_outlet = str(data.iloc[i]["media_name"])
            #check for duplicates for the american conservative
            if temp_outlet == "The American Conservative" or temp_outlet == "American Conservative":
                    if "The American Conservative" in outlet_count.keys():
                        outlet_count["The American Conservative"]+=1
                        continue
                    else:
                        outlet_count["The American Conservative"]=1
                        continue
                        
            if temp_outlet not in outlet_count.keys():
                    outlet_count[temp_outlet] = 1
            else:
                    outlet_count[temp_outlet]+=1
        return outlet_count
    
    
def get_date_article_count(data):
    #create dictionary for storage
    date_count = {}
    
    for i in range(0,len(data)):
        #get the date
        temp_date = str(data.iloc[i]["publish_date"]).split()[0][0:7]
        # temp_date = str(data.iloc[i]["publish_date"])
        if temp_date not in date_count.keys():
            if temp_date == 'nan':
                date_count["000000"] = 1
            else:
                date_count[temp_date] = 1
        else:
            date_count[temp_date]+=1
    return date_count

#create models for facebook shares.
def get_data_share_count(data):
    share_count = {}
    for i in range(0,len(data)):
        #get the outlet
        temp_outlet = str(data.iloc[i]["media_name"])
        #get the share count
        temp_share = int(data.iloc[i]["facebook_share_count"])
        #check for duplicates for the american conservative
        if temp_outlet == "The American Conservative" or temp_outlet == "American Conservative":
                if "The American Conservative" in share_count.keys():
                    share_count["The American Conservative"]+= temp_share
                    continue
                else:
                    share_count["The American Conservative"] = 0
                    continue
                    
        if temp_outlet not in share_count.keys():
                share_count[temp_outlet] = 1
        else:
                share_count[temp_outlet]+=temp_share
    return share_count


if __name__== "__main__":
    #get data
        #filepath
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    #configure show all columns
    pd.set_option('display.max_columns', None)
    
    #upload stories
    s_c = pd.read_csv('edited_data/media_covid_edited.csv')
    s_e = pd.read_csv('edited_data/media_ebola_edited.csv')
    
    #group together by dates and display chunks on line graph
    
    #start
    start_time = time()
    print("running!")
    #create dataframes
        #covid
    print("creating data frames!")
    covid_outlets = pd.DataFrame(get_outlet_article_count(s_c).items(), columns=['News Outlets', 'Num_articles']).sort_values(by="Num_articles", ascending=True)
    covid_dates = pd.DataFrame(get_date_article_count(s_c).items(), columns=['Dates', 'Num_articles']).sort_values(by="Dates", ascending=True)
    covid_shares = pd.DataFrame(get_data_share_count(s_c).items(), columns=['Outlets', 'Facebook_Shares']).sort_values(by="Facebook_Shares", ascending=False)
    
        #ebola
    ebola_outlets = pd.DataFrame(get_outlet_article_count(s_e).items(), columns=['News Outlets', 'Num_articles']).sort_values(by="Num_articles", ascending=True)
    ebola_dates = pd.DataFrame(get_date_article_count(s_e).items(), columns=['Dates', 'Num_articles']).sort_values(by="Dates", ascending=True)
    ebola_shares = pd.DataFrame(get_data_share_count(s_e).items(), columns=['Outlets', 'Facebook_Shares']).sort_values(by="Facebook_Shares", ascending=False)
    """
    #create models for news stories
    print("\n\ncreating outlet plots!")
        #covid
    covid_outlets.plot(x="News Outlets", y="Num_articles", kind="bar", legend=False)
    plt.ylim(covid_outlets["Num_articles"].min(), 32500)
    plt.title("Number of Stories per News Outlet regarding Covid-19")
    plt.xlabel("News Outlets")
    plt.ylabel("Number of Stories")
    
        #ebola
    ebola_outlets.plot(x="News Outlets", y="Num_articles", kind="bar", legend=False)
    plt.ylim(ebola_outlets["Num_articles"].min(), 1000)
    plt.title("Number of Stories per News Outlet regarding Ebola")
    plt.xlabel("News Outlets")
    plt.ylabel("Number of Stories")
    
    print("\n\ncreating date plots!")
    covid_dates.plot(x="Dates", y="Num_articles", kind="line", legend=False)
    plt.ylim(covid_dates["Num_articles"].min(), 30000)
    plt.title("Number of Stories per Month regarding Covid-19")
    plt.xlabel("Time")
    plt.ylabel("Number of Stories")
    
    ebola_dates.plot(x="Dates", y="Num_articles", kind="line", legend=False)
    plt.ylim(ebola_dates["Num_articles"].min(), 2000)
    plt.title("Number of Stories per Month regarding Ebola")
    plt.xlabel("Time")
    plt.ylabel("Number of Stories")
    
    print("\n\ncreating share plots!")
    ebola_shares.plot(x="Outlets", y="Facebook_Shares", kind="bar", legend=False)
    plt.ylim(ebola_shares["Facebook_Shares"].min(), 700000)
    plt.title("Total Number of Facebook Shares per Outlet Ebola")
    plt.xlabel("Outlets")
    plt.ylabel("Number of Shares")
    
    covid_shares.plot(x="Outlets", y="Facebook_Shares", kind="bar", legend=False)
    plt.ylim(covid_shares["Facebook_Shares"].min(), 40000000)
    plt.title("Total Number of Facebook Shares per Outlet Covid-19")
    plt.xlabel("Outlets")
    plt.ylabel("Number of Shares in the Tens of Millions")
    """
    #export files
    print ("exporting files out")
    dataframes = {"covid_outlets": covid_outlets,"ebola_outlets":ebola_outlets,"covid_dates":covid_dates,"ebola_dates":ebola_dates,"covid_shares" : covid_shares,"ebola_shares": ebola_shares}
    
    dir_path_edit = os.path.join(dir_path, "edited_data")
    for d in dataframes.keys():
        print("exporting " + str(d))
        dataframes[d].to_csv(os.path.join(dir_path_edit, str(d) + '.csv'))
        
    
    #end time
    end_time = time()
    
    # print(covid_outlets)
    # print(covid_dates)
    print('\nTime:', format(end_time-start_time, ".2f"))