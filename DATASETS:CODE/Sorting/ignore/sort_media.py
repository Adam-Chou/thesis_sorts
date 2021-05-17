"""
Adam Chou

"""

#import packages
import pandas as pd
import os
    #styler
from matplotlib import pyplot as plt

#filepath
dir_path = os.path.dirname(os.path.realpath(__file__))

#configure show all columns
pd.set_option('display.max_columns', None)

#read files (media outlet specific)
m_c = pd.read_csv('original_data/media_outlets_covid.csv')
m_e = pd.read_csv('original_data/media_outlets_ebola.csv')

#edit media list to drop all inconvenient columns
    #create array of strings to filter
delete_list = ["sum_media_inlink_count","inlink_count","outlink_count","media_inlink_count","fake_news", "sum_author_count","sum_channel_count", "sum_post_count"]
    #delete them
m_e = m_e.drop(columns=delete_list)
m_c = m_c.drop(columns=delete_list)

#send files out
m_c.to_csv(os.path.join(dir_path,'edited_data/media_outlets_covid_edited1.csv'))
m_e.to_csv(os.path.join(dir_path,'edited_data/media_outlets_ebola_edited1.csv'))

#sort, ascending
m_e = m_e.sort_values('story_count', ascending=True)
m_c = m_c.sort_values('story_count', ascending=True)


#filter before making chart
media_plot_e = pd.DataFrame(columns=['News Outlet', "Stories"])

media_plot_e["Stories"] = (m_e["story_count"])
media_plot_e["News Outlet"] = (m_e["name"])

print(media_plot_e)

media_plot_c = pd.DataFrame(columns=['News Outlet', "Stories"])

media_plot_c["Stories"] = m_c["story_count"]
media_plot_c["News Outlet"] = m_c["name"]

print(media_plot_c)

#create charts for individual outlets
media_plot_c.plot(x="News Outlet", y="Stories", kind="bar")
plt.title("Number of Stories per News Outlet regarding the COVID-19 Virus")
plt.xlabel("News Outlet")
plt.ylabel("Number of Stories")

media_plot_e.plot(x="News Outlet", y="Stories", kind="bar")
plt.title("Number of Stories per News Outlet regarding the Ebola Virus")
plt.xlabel("News Outlet")
plt.ylabel("Number of Stories")

#create dataframes for total stories
total_media = pd.DataFrame()
total_media['Virus'] = ['Covid-19', 'Ebola']
total_media['Story Count'] = [m_c["story_count"].sum(), m_e["story_count"].sum()]

#create charts for total stories
total_media.plot(x="Virus", y="Story Count", kind="bar")
plt.title("Total Media Stories for Viral Cases")
plt.xlabel("Epidemic Case")
plt.ylabel("Story Count")


