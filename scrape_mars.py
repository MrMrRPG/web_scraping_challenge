#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Dependencies
import os
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template
import requests
import pandas as pd
import pymongo


# In[ ]:

# The Scrape Function
def scrape():

    # Activating ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ## Mars News Titles

    # In[ ]:

    # Visiting the website
    redplanetscience = 'https://redplanetscience.com/'

    # response = requests.get(redplanetscience)
    browser.visit(redplanetscience)


    # In[ ]:


    for x in range(1):
        # Definitions
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('div', class_='col-md-8')

        # scrape loop
        # for result in results:
	
        # Parent div for article title and teaser paragraph
        news_title = soup.find_all('div', class_='content_title')[0].text
        news_p = soup.find_all('div', class_='article_teaser_body')[0].text

        # Prints
        print('---------------------------------')
        print(news_title)
        print(news_p)


    # ## JPL Mars Space Images - Featured Image

    # In[ ]:


    spaceimages = 'http://spaceimages-mars.com/'
    browser.visit(spaceimages)


    # In[ ]:


    for x in range(1):
        # Definitions
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('div', class_='floating_text_area')

        # scrape loop
        for result in results:

            # Find featured image
            a = result.find('a')
            href = a['href']

            # Prints
            print('---------------------------------')
            print(f"Link to Featured Space Image: {spaceimages}{href}")

    featured_image_url = spaceimages + href


    # ## Mars Facts

    # In[ ]:


    galaxyfacts_mars = 'https://galaxyfacts-mars.com/'


    # In[ ]:


    mars_tables = pd.read_html(galaxyfacts_mars)
    mars_tables


    mars_table = mars_tables[1].rename(columns={0:'Description', 1:'Mars'})

    # In[ ]:


    mars_fact_table = mars_table.to_html()
    mars_fact_table = mars_fact_table.replace('\n', '')
    mars_fact_table


    # ## Mars Hemispheres

    # In[ ]:


    marshemispheres = 'http://marshemispheres.com/'
    browser.visit(marshemispheres)


    # In[ ]:


    for x in range(1):
        # Definitions
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('div', class_='item')

        hemisphere_list = []
        img_url_list = []
        hemisphere_img_dict =[] 

        # scrape loop
        for result in results:

            # Find featured image and URL
            hem=result.find('div',class_='description')
            title=hem.h3.text
            a = result.find('a')
            href = a['href']
            img = a.find('img')
            src = img['src']
            alt = img['alt']

            # Getting rid of unwanted words in the statement
            word_list = ["Enhanced", "  "]

            for word in word_list:
                hemisphere = title.replace(word, "") 
                
            img_url = marshemispheres + src

            # Prints
            print('---------------------------------')
            # print('alt')
            print(f"{hemisphere}:")
            print(f"{img_url}")

            # Dictionary appends
            dict={'title':hemisphere,'image_url':img_url}
            hemisphere_img_dict.append(dict)


    # In[ ]:

    # Display newly created list of dictionaries
    hemisphere_img_dict


    # In[ ]:

    # quit browser


    mars_dict = {"headline": news_title,
                "paragraph": news_p,
                "featured_image_url": featured_image_url,
                "mars_fact_table": mars_fact_table,
                "mars_hemispheres": hemisphere_img_dict

            }



    browser.quit()
    return mars_dict