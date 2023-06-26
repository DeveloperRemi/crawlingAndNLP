import requests
from bs4 import BeautifulSoup
import commonFunctions
from time import sleep
import random
import csv
import sys

#variable for storing long strings to csv
csv.field_size_limit(sys.maxsize)

#urls to sections to scrape
urls = ["https://www.mirror.co.uk/news/", "https://www.mirror.co.uk/news/politics/", "https://www.mirror.co.uk/money/"] #site url

#scrape and store title and article text of a given URL
def scrape_title_and_article_text(url):

    try:

        print(url)

        headers = { #header needed for this site because would sent 403 FORBIDDEN with simple request
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }

        
        #lead_title_container =  siteSouped.find("div", class_ = "lead-content") #search for all <article> tags

        #print("LEAD TITLE CONTAINER")
        #print(lead_title_container)

        while(True):
            try:
                site_response = requests.get(url, headers=headers) #send request with parameters

                siteSouped = BeautifulSoup(site_response.content, "html.parser") #make soup from site response

                lead_title_container =  siteSouped.find("div", class_ = "lead-content") #search for all <article> tags
            except AttributeError as e:
                print(e)    
            if lead_title_container != None:
                break
            else:
                print(lead_title_container)
                ran_num = random.randint(1,5)
                print(ran_num)
                sleep(ran_num)
            

        h1 = lead_title_container.find('h1').text #extract main header

        print(h1) #test

        final_article_string = "" #initialize article string

        try: #check if there is a subheading section
            lead_title_container_p = lead_title_container.find("p").text #extract main heading subsection
            final_article_string += lead_title_container_p #add main heading subsection to article string    
        except AttributeError as e: #catch error if there is one
            print(e) #print error, test

        

        article_text_soup = siteSouped.find('div', class_ = "article-body") #look for article body class

        for element in article_text_soup: #loop thru elements in article body
            if element.name == "div" or element.name == "aside" or element.name == "embed-html": #look for elements without article text
                continue #omit elements with no article text
            elif element.name == "section": #more contidions to check if element has article text
                continue #omit if not an article text element+
            else:
                final_article_string += element.text #add element to article string
                print(element.text) #test
        
        if not commonFunctions.check_if_title_name_and_article_text_exist_in_file(h1, final_article_string, "mirror_Data.csv", url): #check if title ant text exist in csv
            commonFunctions.write_row_to_csv(h1, final_article_string, "mirror_Data.csv", url) #write to csv if no duplicates detected
        else:
            print("SAME")#test
        print("--------------") #test
        print(final_article_string) #test

    except Exception as e:
        print(e)

#scrape titles and links to them in a given site
def scrape_all_article_links_in_site(url):

    try:

        headers = { #header needed for this site because would sent 403 FORBIDDEN with simple request
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }

        site_response = requests.get(url, headers=headers) #send request with parameters

        siteSouped = BeautifulSoup(site_response.content, "html.parser") #make soup from site response

        articles =  siteSouped.find_all("article") #search for all <article> tags

        for article in articles: #loop thru article tags
            h2 = article.find("h2") #look for title
            print(h2) #test
            if h2 == None: #will catch a bunch of empty elemenets, need to filter out
                print(article) #test
            else: #condition with normal article
                a = article.find("a") #extract link from article element
                print(a['href']) #test
                single_article_link = a['href'] #initialize variable
                scrape_title_and_article_text(single_article_link) #run function to scrape title and article text
            print("-----------------------")#test

    except Exception as e:
        print(e)

#run program
def run_mirror_scrape():

    try:

        for url in urls:

            scrape_all_article_links_in_site(url)
            print(url)

    except Exception as e:
        print(e)

