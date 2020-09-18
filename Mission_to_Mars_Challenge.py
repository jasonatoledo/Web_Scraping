#!/usr/bin/env python
# coding: utf-8

# In[256]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np


# In[72]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[319]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[14]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[17]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[18]:


slide_elem.find("div", class_='content_title')


# In[19]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[20]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[21]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[22]:


full_image_elem = browser.find_by_id('full_image')


# In[23]:


full_image_elem


# In[24]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[25]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[26]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[27]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[28]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[29]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[30]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[31]:


df.to_html()


# ### Mars Weather

# In[32]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[33]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[34]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[320]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[321]:


# Get BS4 working

html = browser.html
moons_soup = soup(html, 'html.parser')


# In[322]:


hemis = moons_soup.find_all("a", class_="itemLink product-item")
hemis


# In[323]:


hemilist = []


# In[324]:


for hemi in hemis:
    hemilist.append(hemi.get("href"))


# In[325]:


hemilist


# In[326]:


hemilist = np.unique(hemilist)
hemisp = hemilist.tolist()


# In[327]:


hemisp


# In[330]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
site = 'https://astrogeology.usgs.gov/'
# 3. Write code to retrieve the image urls and titles for each hemisphere.


# Write for loop to iterate through the tags/CSS elements

for hemi in hemisp:
        
    # Create dictionary object inside the for loop
    hem_dict = {}    
    
    # click the link
    browser.visit(f"{site}{hemi}")
      
    # Reset the parser
    html2 = browser.html
    moons_soup = soup(html2, 'html.parser')
    
    # get the image link for the full sized image
    imgtarget = moons_soup.select_one('li a').get('href')
    
    # get the title for the image
    imgtitle = moons_soup.select_one('h2').get_text()
    
    # Update the dictionary with this info
    hem_dict.update({'img_url': imgtarget, 'title':imgtitle})
    
    # Append the dictionary to the URL list
    hemisphere_image_urls.append(hem_dict)
        
    # For loop will: Click on each link, navigate to full-res image and pull image URL string and title for each image
    browser.back()
    # browser.visit(url)


# In[331]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[98]:


# 5. Quit the browser
browser.quit()


# In[ ]:




