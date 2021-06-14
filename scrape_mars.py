from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # --- Visit Mars News site ---
    browser.visit('https://mars.nasa.gov/news/')

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first news title
    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[0].text

    # Get the corresponding paragraph text
    p_results = soup.find_all('div', class_='article_teaser_body')
    news_p = p_results[0].text

    # --- Visit JPL site for featured Mars image ---
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    time.sleep(1)

    # Click through to full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img = 'https://www.jpl.nasa.gov' + relative_img_path
    
    # --- Use Pandas to scrape Mars Space Facts ---
    tables = pd.read_html('https://space-facts.com/mars/')

    # Take second table for Mars facts
    df = tables[1]

    # Rename columns and set index
    df.columns=['description', 'value']
    
    # Convert table to html
    mars_facts_table = df.to_html(classes='data table', index=False, header=False, border=0)