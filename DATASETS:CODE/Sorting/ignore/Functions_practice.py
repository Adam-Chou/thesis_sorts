"""
Adam Chou
Functions practice test

"""
def find_article(url):
    import requests
    from bs4 import BeautifulSoup
    import urllib.request,sys,time
    
    try:
         # this might throw an exception if something goes wrong.
         page=requests.get(url)  
         
         soup = BeautifulSoup(page.text, "html.parser")
         
         text = soup.find_all('p')
         #convert object to string
         time = str(soup.find_all('time')[0].text)
         # time = time.replace("<time>","").replace("</time>","")
         title = soup.find_all('title')[0].text
         
         #parse thorugh meta data to find time, title, author
         
         
         return time, text
    # this describes what to do if an exception is thrown
    except Exception as e:    
        
        # get the exception information
        error_type, error_obj, error_info = sys.exc_info()      
        
        #print the link that cause the problem
        print ('ERROR FOR LINK:',url)
        
        #print error info and line that threw the exception                          
        print (error_type, 'Line:', error_info.tb_lineno)
   
   
import random

def random_sample(num,low_range ,high_range):
    total_samples = []
    while(len(total_samples)<num+1):
        sample = random.SystemRandom().randint(low_range,high_range)
        if sample not in total_samples:
            total_samples.append(int(sample))
            
    return total_samples
     

print(random_sample(50,0, 8000))

    
"""

url = "http://feeds.foxnews.com/~r/foxnews/health/~3/OBgHmi8ltEw/"

# call function
ti, te = find_article(url)

print(ti, te)
"""