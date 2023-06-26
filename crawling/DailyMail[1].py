import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import commonFunctions
import html5lib
import platform
import urllib


#get list of links in the main navigatio panel
def get_list_of_nav_links():

    try:

        result_list = [] #final list variable

        URL = "https://www.dailymail.co.uk/home/latest/index.html#" #constant link

        topics = ["home", "news", "health", "sciencetech", "money"] #nav options relevant

        link = "https://www.dailymail.co.uk/home/latest/index.html#home" #start link

        site_response = requests.get(link) #request HTML skeleton
        site_response_souped = BeautifulSoup(site_response.content, "html.parser") #part the response

        alpha = site_response_souped.find(class_ = "alpha") #extract alpha part of site

        ul = alpha.find("ul") #look for unosorted links
        ul = ul.find_all("a") #extract <a> elements

        for li in ul: #iterate thru unordered list
            temp_str = li["href"] #extract link part from element
            res_str = temp_str[temp_str.index("=") +1 :] #slice front part of string
            for topic in topics: #iterate thru relevant nav options
                if topic == res_str:# if string is one of relevant topics
                    full_url = URL + res_str #make full link
                    result_list.append(full_url) #add to list

        print(result_list) #test
        return result_list #return list

    except Exception as e:
        print(e)

#scrape and store sites title, article text and link
def scrape_DailyMail_site(link):

    try:

        print("LINK WORKING WITH:")
        print(link)

        site_response = requests.get(link) #request HTML skeleton
        site_response_souped = BeautifulSoup(site_response.content, "html.parser") #part the response

        alpha = site_response_souped.find(class_ = "alpha") #get class element alpha
        article_body = site_response_souped.find("div", {"itemprop" : "articleBody"}) #get element with article body

        if alpha == None:
            gamma = site_response_souped.find(class_ = "gamma") #get class element gamma
            title = gamma.find("h2").text #extract title
        else:
            title = alpha.find("h2").text #extract title

        count = 1 #test
        full_article_string = "" #full article string variable

        for element in article_body: #iterate thru elements in article body
            if element.name == "p": #check if element is <p>
                full_article_string += element.text #if True then add to full article string
                count += 1 #test
            else:
                continue #if False, then continue

        print(title) #test
        print(full_article_string) #test

        return title, full_article_string #return title string and full article text string

    except Exception as e:
        print(e)

#scrape article titles and links to the articles in the given site page
def get_article_links_from_nav_site_option(list_of_nav_links):

    try:

        for link in list_of_nav_links:

            URL = "https://www.dailymail.co.uk" #constant site URL

            #link = "https://www.dailymail.co.uk/home/latest/index.html#home" #link to access firt nav bar option

            options = Options() #for chrome headless browser

            options.headless = True #for chrome headless browser

            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options) #initialize selenium driver
            driver.get(link) #get link

            lastHeight = driver.execute_script("return document.body.scrollHeight") #measures the height of the site
            print(lastHeight) #print last height

            pause = 3.5 #pause to lead website in selenium
            #code to scroll in selenium
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll
                time.sleep(pause) #pause
                newHeight = driver.execute_script("return document.body.scrollHeight") #scroll
                if newHeight == lastHeight: #scroll
                    break #scroll
                lastHeight = newHeight #scroll
                print(lastHeight) #scroll

            html = driver.page_source #selenium file to variable
            soup = BeautifulSoup(html, "html5lib") #convert to bs4 format

            alpha = soup.find(class_ = "alpha") #extract alpha part of site

            all_h3s = alpha.find_all("h3") #find all h3 elements

            #extract all links
            for h3 in all_h3s: #iterate thru every h3 element
                temp = h3.find("a")['href'] #cut off linl from every h3 element
                if "/sport/" in temp or "tvshowbiz" in temp or "femail" in temp: #omit irrelevant topics
                    continue #continue loop
                elif "/galleries/" in temp or "/video/" in temp: #omit irrelevant topics
                    continue #continue loop
                else:
                    print(URL + temp) #test
                    full_link = URL + temp #combine full link
                    title, article_text = scrape_DailyMail_site(full_link) #srapce title and article text to variables
                    if not commonFunctions.check_if_title_name_and_article_text_exist_in_file(title, article_text, "Daily_Mail_Data.csv", full_link): #check if no duplicates
                        commonFunctions.write_row_to_csv(title, article_text, "Daily_Mail_Data.csv", full_link) #write to csv if no duplicates

                

            print(f'SITE{link} IS FINISHED') #test

    except Exception as e:
        print(e)

#run this program
def run_daily_mail():

    try:

        nav_links = get_list_of_nav_links()

        get_article_links_from_nav_site_option(nav_links)

    except Exception as e:
        print(e)

