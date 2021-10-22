# 10.3.6 Export to Python & clean code
#!/usr/bin/env python
# coding: utf-8

# # 10.3.3 Scrape Mars Data: The News
# 
# With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.
# 
# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as <ul class="item_list">.
# 
# Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.
#     
# e've assigned slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the <div /> element)? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it.
#     
# chained .find onto our previously assigned variable, slide_elem. When we do this, we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data." The data we're looking for is the content title, which we've specified by saying, "The specific data is in a <div /> with a class of 'content_title'."
#     
# added something new to our .find() method here: .get_text(). When this new method is chained onto .find(), only the text of the element is returned

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

# 10.5.3 Integrate MongoDB Into the Web App
#Initialize the browser.
#Create a data dictionary.
#End the WebDriver and return the scraped data.

# define this function as "scrape_all" and then initiate the browser
def scrape_all():
    # 10.3.6 Export to Python & clean code
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # set our news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now()
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data
    
 
# 10.5.2 Defining functions in the previous code
def mars_news(browser):
    
    # assign the url and instruct the browser to visit it
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    
    # Add try/except for error handling
    try:
        # assign the title and summary text to variables we'll reference later
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None
        
    return news_title, news_p

# # 10.3.4 Scrape Mars Data: Featured Image
# The next step is to scrape the featured image from another Mars website. Once the image is scraped, we'll want to add it to our web app as well.
# 
# Ultimately, with each item we scrape, we'll also save and then serve it on our own website.

# ### Featured Images
# we'll want Splinter to click the "Full Image" button
# 
# A new automated browser should open to the featured images webpage.
# 
# the <button> element has a two classes (btn and btn-outline-light) and a string reading "FULL IMAGE". First, let's use the dev tools to search for all the button elements.
# Since there are only three buttons, and we want to click the full-size image button, we can go ahead and use the HTML tag in our code.
#     
# the indexing chained at the end of the first line of code? With this, we've stipulated that we want our browser to click the second button.
#     
# With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL.
#     
# use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
#     An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
#     
# We were able to pull the link to the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL directly. This way, when JPL updates its image page, our code will still pull the most recent image.
#     
# look at our address bar in the webpage, we can see the entire URL up there already

def featured_image(browser):

    # set up the URL
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # new page loaded onto our automated browser needs to be parsed to scrape the full-size image URL
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # add the base URL to our code.
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url_rel, img_url

# # 10.3.5 Scrape Mars Data: Mars Facts
# collection of Mars facts. With news articles and high-quality images, a collection of facts
# 
# Tables in HTML are basically made up of many smaller containers. The main container is the <table /> tag. Inside the table is <tbody />, which is the body of the table—the headers, columns, and rows.
# 
# <tr /> is the tag for each table row. Within that tag, the table data is stored in (<td />) tags. This is where the columns are established.
# 
# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function. add import pandas as pd to the dependencies.
# 
# Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function
# 
# that we've gathered everything on Robin's list, we can end the automated browsing session. This is an important line to add to our web app also. Without it, the automated browser won't know to shut down—it will continue to listen for instructions and use the computer's resources (it may put a strain on memory or a laptop's battery if left on). We really only want the automated browser to remain active while we're scraping data.
# add browser.quit() and execute that cell to end the session.

def mars_facts():
    # Add try/except for error handling
    try:
        # scrape the entire table with Pandas into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
        
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
            
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# # IMPORTANT
# Live sites are a great resource for fresh data, but the layout of the site may be updated or otherwise changed. When this happens, there's a good chance your scraping code will break and need to be reviewed and updated to be used again.
# 
# For example, an image may suddenly become embedded within an inaccessible block of code because the developers switched to a new JavaScript library. It's not uncommon to revise code to find workarounds or even look for a different, scraping-friendly site all together.

# # 10.3.6 Export to Python
# 
# To fully automate it, it will need to be converted into a .py file.
# 
# The next step in making this an automated process is to download the current code into a Python file. It won't transition over perfectly, we'll need to clean it up a bit, but it's an easier task than copying each cell and pasting it over in the correct order.
