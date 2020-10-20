#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from selenium import webdriver
import requests as req

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()


#MARS NEWS
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    #pause
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    #pause
    time.sleep(1)

    #collect article
    article = soup.find('div', class_='list_text')

    #collect title
    first_title = article.find('div', class_='content_title').text

    #collect paragraph
    first_para = article.find('div', class_='article_teaser_body').text

#MARS IMAGE
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image_url)
    #pause
    time.sleep(1)

    html = browser.html
    image_soup = bs(html, 'html.parser')

    #pause
    time.sleep(1)

    #collect image
    browser.links.find_by_partial_text('FULL IMAGE').click()

    #pause
    time.sleep(1)

    #find image url by clicking 'more info'
    browser.links.find_by_partial_text('more info').click()

    #pause
    time.sleep(1)

    #read html on this page
    html = browser.html
    image_soup = bs(html, 'html.parser')

    #find image id/source
    image = image_soup.select_one("figure", class_='lede')

    image_id = image.find('img')["src"]
    image_url = f"https://www.jpl.nasa.gov{image_id}"

    #define image url
    image_url = f"https://www.jpl.nasa.gov{image_id}"

#MARS FACTS
    #define url and only look at first table
    facts_url = "https://space-facts.com/mars/"

    #read in pandas
    facts_df = pd.read_html(facts_url)
    facts_df

    #only look at first table
    mars_facts = facts_df[0]
    mars_facts

    #edit the df
    mars_facts.columns = ['Description', 'Value(s)']
    mars_facts

#MARS HEMISPHERES
    #scrape https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')

    #pause
    time.sleep(1)

    #find hemisphere titles
    hemis = []

    results = hemi_soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    #get and store
    for name in hemispheres:
        hemis.append(name.text)

    # find urls for image thumbnails
    thumbnails = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnails:
        if (thumbnail.img):
            thumbnail_url = f'https://astrogeology.usgs.gov/{thumbnail}'
            thumbnail_links.append(thumbnail_url)

    #need only href for links...
    # find urls for image thumbnails
    thumbnails = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnails:
        if (thumbnail.img):
            thumbnail_url = 'https://astrogeology.usgs.gov/' + thumbnail['href']
            thumbnail_links.append(thumbnail_url)

    #find urls for full sized images
    full_images = []

    for url in thumbnail_links:
        
        #Read into each page from thumbnail link
        browser.visit(url)
        
        html = browser.html
        full_soup = bs(html, 'html.parser')
        
        results = full_soup.find_all('img', class_='wide-image')
        image_path = results[0]['src']
        
        image_link = f'https://astrogeology.usgs.gov/{image_path}'
        
        full_images.append(image_link)

    #combine the lists
    hemis_df = pd.DataFrame(hemis)
    hemis_df['URL'] = full_images
    hemis_df.rename(columns={0:"Title"})

    #store in dictionary
    mars_data = {
    "Title": first_title,
    "Paragraph": first_para,
    "Image": image_url,
    "Mars Facts": mars_facts,
    "Hemispheres": hemis_df
    }

    #quit browser
    browser.quit()

    #return results
    return mars_data