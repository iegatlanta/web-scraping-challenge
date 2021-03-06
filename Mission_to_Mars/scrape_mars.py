#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_all():

    mars={}
    url_mars_news = 'https://redplanetscience.com/'
    browser.visit(url_mars_news)
    
    # html object
    html = browser.html
    
    # Parse with Beautiful Soup
    soup = bs(html, 'html.parser')
    mars_news_title = soup.find("div", class_="content_title").text
    news_title_scrape = mars_news_title
    news_title_scrape
    mars["news_title"]=news_title_scrape
    mars_news_paragraph = soup.find("div", class_="article_teaser_body").text
    news_p_scrape = mars_news_paragraph
    news_p_scrape
    mars["news_p"]=news_p_scrape
    
    mars_url = "https://spaceimages-mars.com/"
    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Retrieve featured image link
    relative_image_path = soup.find_all('img')[1]["src"]
    featured_image_url_scrape = mars_url+relative_image_path
    featured_image_url_scrape
    mars["featured_image"]=featured_image_url_scrape
    
    mars_profile = 'https://galaxyfacts-mars.com/'
    mars_profile_table = pd.read_html(mars_profile)
    mars_table_df = mars_profile_table[1]
    new_mars_df = mars_table_df.rename(columns={0:'Mars Planet Profile', 1:''})
    new_mars_df
    mars_facts_scrape = new_mars_df.to_html()
    mars["facts"]=mars_facts_scrape
       
    mars_hemi_pics='https://marshemispheres.com/'
    browser.visit(mars_hemi_pics)
    html = browser.html
    soup = bs(html, 'html.parser')
    main_urls = soup.find_all('div',class_='item')
   
    # Create list to hold dicts
    urls_for_h_images_scrape=[]
   
    for main_url in main_urls:
        hemisphere_image_dict = {}
        h_title = main_url.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
        h_images = mars_hemi_pics + main_url.find('a',class_='itemLink product-item')['href']
        browser.visit(h_images)
        html = browser.html
        soup = bs(html, 'html.parser')
        full_image_url = soup.find('div',class_='downloads').a['href']
        
        #print(full_image_url)
        # Append title and image urls of hemisphere to dictionary
        hemisphere_image_dict['h_title'] = h_title
        hemisphere_image_dict['full_img_url'] = 'https://marshemispheres.com/'+full_image_url
        urls_for_h_images_scrape.append(hemisphere_image_dict)        
        mars["hemispheres"]=urls_for_h_images_scrape

    return mars
    
if __name__ == "__main__":
    print(scrape_all())





