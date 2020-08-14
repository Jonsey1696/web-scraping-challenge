from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # browser=init_browser()

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser= Browser("chrome", **executable_path, headless=False)

    #get news
    news_url="https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(5)
    news_html=browser.html
    soup = bs(news_html, 'lxml')
    article=soup.find('li', class_='slide')
    for art in article:
        title=soup.find('h3')
        title_only=title.find('span').text
        news_p=soup.find('div', class_='article_teaser_body').text
    #title=article.find('h3')
    #title_only=title.find('span').text
    #news_p=article.find('div', class_='article_teaser_body').text

    #get featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL')
    time.sleep(5)
    html=browser.html
    soup = bs(html, 'html.parser')
    url_pull=soup.find('img', class_='fancybox-image')['src']
    base_url="https://www.jpl.nasa.gov"
    featured_image_url=(f'{base_url}{url_pull}')

    #get twitter weather data
    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(5)
    html=browser.html
    soup = bs(html, 'html.parser')
    tweet=soup.find('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    weather_update=tweet.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    #get facts table
    table_url="https://space-facts.com/mars/"
    tables=pd.read_html(table_url)
    mars_table=tables[0]
    mars_table = mars_table.rename(columns={1: 'measurement'})
    mars_table = mars_table.rename(columns={0:'record'})
    fixed_mars_table=mars_table.to_html('mars_table.html')

    #get hemisphere images
    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(5)
    hemis=['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemisphere_image_urls=[]
    for x in hemis:
        browser.click_link_by_partial_text(x)
        time.sleep(5)
        html=browser.html
        soup=bs(html, 'lxml')
        img_url=soup.find('img', class_='wide-image')['src']
        title=soup.find('h2', class_='title').text
        img_dict={
            'title':title,
            'img_url':(f'https://astrogeology.usgs.gov{img_url}')
            }
        hemisphere_image_urls.append(img_dict)
        browser.visit(hemi_url)
        time.sleep(5)
    browser.quit()
    print(hemisphere_image_urls)

    #build dict
    mars_data={
        'title':title_only,
        'news':news_p,
        'featured_image': featured_image_url,
        'table_data': fixed_mars_table,
        'weather': weather_update,
        'hemispheres':hemisphere_image_urls
        }

    # #insert into mongodb
    # conn = "mongodb://localhost:27017"
    # client = pymongo.MongoClient(conn)

    # db = client.mars_db
    # mars_scrape = db.mars_scrape

    # mars_table.insert_one(mars_data)

    return(mars_data)