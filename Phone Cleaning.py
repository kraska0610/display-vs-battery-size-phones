"""
phonearena.com scraping and cleaning
"""


import requests
import pandas as pd
import matplotlib.pylab as plt
import plotly.express as px
from bs4 import BeautifulSoup
import pickle
import datetime

headers = {'User-Agent': 'Safari'}
base_url = "https://www.phonearena.com/phones/page/"
phonepage_urls = [base_url + str(i) for i in range(1,18)]

df = pd.DataFrame()
pd.set_option('display.max_columns', None)

for phonepage_url in phonepage_urls:
    
    print('---Getting Page: ' + phonepage_url.split("/")[-1] + '---')
    
    phonepage_req = requests.get(phonepage_url, headers=headers)
    phonepage_req.raise_for_status()
    phonepage = BeautifulSoup(phonepage_req.text, 'html.parser')
    
    phone_tags = phonepage.select('.thumbnail')
    phone_urls = [phone_tag.attrs['href'] for phone_tag in phone_tags]


    #scraping phonearena.com for data about phones
    for phone_url in phone_urls:
        
        phone_name = phone_url.split("/")[-1]
        print('\t' + phone_name)
        
        phone_dfs = pd.read_html(phone_url)
        
        
        if 'Size:' in phone_dfs[0].iloc[:,0].to_list():
            if 'Display' in phone_dfs[0].columns.values.tolist():
                df.loc[phone_name, 'Display Size'] = phone_dfs[0].loc[phone_dfs[0].Display == "Size:",'Display.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Display Size'] = phone_dfs[0].loc[phone_dfs[0]['Display  Benchmarks'] == "Size:",'Display  Benchmarks.1'].to_string(index = False)  
        else:
            df.loc[phone_name, 'Display Size'] = 'N/A'
            
        
        if 'Resolution:' in phone_dfs[0].iloc[:,0].to_list():
            if 'Display' in phone_dfs[0].columns.values.tolist():
                df.loc[phone_name, 'Resolution'] = phone_dfs[0].loc[phone_dfs[0].Display == "Resolution:",'Display.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Resolution'] = phone_dfs[0].loc[phone_dfs[0]['Display  Benchmarks'] == "Resolution:",'Display  Benchmarks.1'].to_string(index = False) 
        else:
            df.loc[phone_name, 'Resolution'] = 'N/A'
            
        if 'Refresh rate:' in phone_dfs[0].iloc[:,0].to_list():
            if 'Display' in phone_dfs[0].columns.values.tolist():
                df.loc[phone_name, 'Refresh Rate'] = phone_dfs[0].loc[phone_dfs[0].Display == "Refresh rate:",'Display.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Refresh Rate'] = phone_dfs[0].loc[phone_dfs[0]['Display  Benchmarks'] == "Refresh rate:",'Display  Benchmarks.1'].to_string(index = False) 
        else:
            df.loc[phone_name, 'Refresh Rate'] = 'N/A'
  
        
  
        if 'RAM:' in phone_dfs[1].iloc[:,0].to_list():
            if 'Hardware' in phone_dfs[1].columns.values.tolist():
                df.loc[phone_name, 'RAM'] = phone_dfs[1].loc[phone_dfs[1].Hardware == 'RAM:','Hardware.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'RAM'] = phone_dfs[1].loc[phone_dfs[1]['Hardware  Benchmarks'] == 'RAM:','Hardware  Benchmarks.1'].to_string(index = False)
        else:    
            df.loc[phone_name, 'RAM'] = 'N/A'
            
        if 'Internal storage:' in phone_dfs[1].iloc[:,0].to_list():     
            if 'Hardware' in phone_dfs[1].columns.values.tolist():
                df.loc[phone_name, 'Storage'] = phone_dfs[1].loc[phone_dfs[1].Hardware == 'Internal storage:','Hardware.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Storage'] = phone_dfs[1].loc[phone_dfs[1]['Hardware  Benchmarks'] == 'Internal storage:','Hardware  Benchmarks.1'].to_string(index = False)
        else:
            df.loc[phone_name, 'Storage'] = 'N/A'
        
        
        if 'Device type:' in phone_dfs[1].iloc[:,0].to_list():   
            if 'Hardware' in phone_dfs[1].columns.values.tolist():
                df.loc[phone_name, 'Device Type'] = phone_dfs[1].loc[phone_dfs[1].Hardware == 'Device type:','Hardware.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Device Type'] = phone_dfs[1].loc[phone_dfs[1]['Hardware  Benchmarks'] == 'Device type:','Hardware  Benchmarks.1'].to_string(index = False)
        else:    
            df.loc[phone_name, 'Device Type'] = 'N/A'
        
        
        
        if 'Capacity:' in phone_dfs[2].iloc[:,0].to_list():
            if 'Battery' in phone_dfs[2].columns.values.tolist():
                df.loc[phone_name, 'Battery Capacity'] = phone_dfs[2].loc[phone_dfs[2].Battery == 'Capacity:','Battery.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Battery Capacity'] = phone_dfs[2].loc[phone_dfs[2]['Battery  Benchmarks'] == 'Capacity:','Battery  Benchmarks.1'].to_string(index = False)
        else:
            df.loc[phone_name, 'Battery Capacity'] = 'N/A'
            
        
        if len(phone_dfs) == 9:
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 10:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 11:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 12:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 13:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 14:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 15:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 16:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A' 
        elif len(phone_dfs) == 17:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[16].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[16].loc[phone_dfs[16].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A'
        elif len(phone_dfs) == 18:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[16].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[16].loc[phone_dfs[16].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[17].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[17].loc[phone_dfs[17].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A'
        elif len(phone_dfs) == 19:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[16].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[16].loc[phone_dfs[16].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[17].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[17].loc[phone_dfs[17].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[18].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[18].loc[phone_dfs[18].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A'
        elif len(phone_dfs) == 20:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[16].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[16].loc[phone_dfs[16].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[17].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[17].loc[phone_dfs[17].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[18].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[18].loc[phone_dfs[18].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[19].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[19].loc[phone_dfs[19].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A'
        elif len(phone_dfs) == 21:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[16].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[16].loc[phone_dfs[16].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[17].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[17].loc[phone_dfs[17].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[18].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[18].loc[phone_dfs[18].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[19].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[19].loc[phone_dfs[19].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[20].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[20].loc[phone_dfs[20].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A'
        elif len(phone_dfs) == 22:    
            if 'Officially announced:' in phone_dfs[8].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[8].loc[phone_dfs[8].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[9].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[9].loc[phone_dfs[9].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[10].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[10].loc[phone_dfs[10].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[11].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[11].loc[phone_dfs[11].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[12].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[12].loc[phone_dfs[12].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[13].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[13].loc[phone_dfs[13].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[14].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[14].loc[phone_dfs[14].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[15].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[15].loc[phone_dfs[15].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[16].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[16].loc[phone_dfs[16].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[17].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[17].loc[phone_dfs[17].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[18].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[18].loc[phone_dfs[18].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[19].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[19].loc[phone_dfs[19].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[20].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[20].loc[phone_dfs[20].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            elif 'Officially announced:' in phone_dfs[21].iloc[:,0].to_list():
                df.loc[phone_name, 'Year'] = phone_dfs[21].loc[phone_dfs[21].Availability == 'Officially announced:','Availability.1'].to_string(index = False)
            else:
                df.loc[phone_name, 'Year'] = 'N/A'
        else:
            df.loc[phone_name, 'Year'] = 'N/A'    


#dropping devices that aren't smartphones
df = df[df['Device Type'].str.contains("Smartphone") == True]

#dropping devices with missing values
df = df[df['Display Size'].str.contains("inches") == True]
df = df[df['Resolution'].str.contains(" x ") == True]
df = df[df['Refresh Rate'].str.contains("Hz") == True]
df = df[df['RAM'].str.contains("GB") == True]
df = df[df['Storage'].str.contains("GB") == True]
df = df[df['Battery Capacity'].str.contains("mAh") == True]
df = df[df['Year'].str.contains("202") == True]

#cleaning the dataframe
Brand = []
Name = []
for line in df.index:
    split = line.split("-", maxsplit = 1)
    
    brand = split[0]
    Brand.append(brand)
    
    name = split[1]
    name = name.split("_id")
    name = name[:-1]
    name = ' '.join(name)
    name = name.replace("-"," ")
    Name.append(name)


Size = []
for line in df['Display Size']:
    split = line.split(' ')
    size = split[0]
    Size.append(size)


Resolution = []
for line in df['Resolution']:
    split = line.split(' pixels')
    resolution = split[0]
    Resolution.append(resolution)
 
Refresh_Rate = []
for line in df['Refresh Rate']:
    split = line.split('H')
    refresh = split[0]
    Refresh_Rate.append(refresh)
    
RAM = []
for line in df['RAM']:
    split = line.split('GB')
    ram = split[0]
    RAM.append(ram)


Battery = []
for line in df['Battery Capacity']:
    split = line.split(' ')
    battery = split[0]
    Battery.append(battery)
    

Storage = []
for line in df['Storage']:
    split = line.split('GB')
    storage = split[0]
    Storage.append(storage)

Month = []
Year = []
for line in df['Year']:
    split = line.split(' ')
    month = split[0]
    year = split[2]
    Month.append(month)
    Year.append(year)


Released = [x + ' ' + y for x,y in zip(Month, Year)]


#adding cleaned columns to data frame
df['Brand'] = Brand
df['Device Name'] =  Name
df['Display Size (inches)'] = Size
df['Display Resolution'] = Resolution
df['Refresh Rate (Hz)'] = Refresh_Rate
df['Battery (mAh)'] = Battery
df['RAM (GB)'] = RAM
df['Storage (GB)'] = Storage
df['Released'] = Released


#removing old columns to datafrmae
df = df.drop(['Device Type','Display Size', 'Resolution', 'Refresh Rate', 'RAM', 'Storage', 'Battery Capacity', 'Year'], axis = 1)


#removing smartphone brands outside of the list defined below
df = df.loc[df['Brand'].isin(['Samsung', 'Apple', 'Google', 'Huawei', 'Oppo', 'OnePlus', 'Sony', 'LG', 'Motorola', 'Nokia'])]


#converting release date to datetime format
df['Released'] = pd.to_datetime(df['Released'])
df['Released'] = df['Released'].dt.strftime("%b %Y")
df = df.sort_values(by = 'Released')


df = df[df['Released'].str.contains("202") == True]
phones_pickle = df.to_pickle('./phones.pkl')

# df.to_csv('/Users/karaska/Desktop/phones_csv')  
# phones = pd.read_csv('/Users/karaska/Desktop/phones_csv')


