import random
import requests
from bs4 import BeautifulSoup
from time import sleep
import commonFunctions

#list of variables needed for this class
error_list = []

list_of_odd = []

a_list = []

classes_list = []

#extract and store title and article text
def extract_data_using_link(link):

    try:

        site_response = requests.get(link) #request HTML skeleton
        site_response_souped = BeautifulSoup(site_response.content, "html.parser") #part the response

        title = site_response_souped.find("h1") #get mani heading element
        title = title.text #convert main heading to text
        print("PRINT TITLE") #test
        print(title)#test

        #handle AttributeError if there is no standFirst section in article because sometimes there is none.
        try: 
            stand_first = site_response_souped.find("div", {"data-gu-name": "standfirst"}) #look for section
            stand_first = stand_first.find("p") #look for paragraph section <p>
            stand_first = stand_first.text #get str from paragraph
        except AttributeError as e: #handle error if present
            print(e) #print error

        soup = site_response_souped.find("div", {"id": "maincontent"}) #get article body soup
        text_element_list = soup.find_all("p") #extract paragraph element from article soup

        article_str = stand_first #add stand_first section
        if article_str is None:
            article_str = ""
        else:
            article_str += ". " #add full stop and space after stand_first section

        

        #combine main article string
        for element in text_element_list: #loop through elements
            if element.parent.parent.name == "figure" or element.parent.parent.parent.name == "figure": #skip non-article text if present in the body
                continue 
            else:
                article_str += element.text #extract text from element and add to string
                article_str += " " #add space after every text element
                

            
                
        print("PRINT ARTICLE STRING") #test
        print(article_str) #test
        return title, article_str

    except Exception as e:
        print(e)

#wait function
def random_time_sleep():
    x = round(random.uniform(2.00, 66.66), 2)
    return sleep(x)

#get articles and links to them in the first two pages of given site
def crawl_first_two_site_pages(site):
    try:
        nr_list = list(range(1,3)) #set range from 1 to 3(not included)

        for nr in nr_list: #run thru numbers
            full_link = check_for_rare_links(site) #check for rare links function
            full_link = f"{full_link}?page={nr}" #combine link with page request and number
            print(full_link) #test
            test = requests.get(full_link) #test
            print(test) #test
            loop_through_links(full_link) #send full link to fucntion for article links extraction
    
    except Exception as e:
        print(e)

#loop through given set of links
def loop_through_links(link):

    try:

        site_response = requests.get(link) #send get request to site

        siteSouped = BeautifulSoup(site_response.content, "html.parser") #parse to soup

        h3_list = siteSouped.find_all("h3") #look for h3 HTML elements 

        for h3 in h3_list: #loop thru all found h3 elements
            result = h3.find("a") #extract <a> element from h3 elements
            result = result['href'] #extract link from <a> attribute elements

            if '/picture/' in result or 'tv-and-radio' in result: #check if theres is gallery links
                continue #skip gallery links if present
            elif '/video/' in result:# check there this is not ONLY video link
                continue #skip in link is ONLY video
            elif '/ng-interactive/' in result: #check there this is not interactive link
                continue #skip in link is ONLY video
            else: 
                a_list.append(result) #add wanted links to list
                title, article = extract_data_using_link(result)

                if not commonFunctions.check_if_title_name_and_article_text_exist_in_file(title, article, "Guardian_Data.csv", result):
                    commonFunctions.write_row_to_csv(title, article, "Guardian_Data.csv", result)

            print(result) #test

    except Exception as e:
        print(e)

#check for links like ads
def check_for_rare_links(link):
    try:
        if link == "https://www.theguardian.com/world/asia":
            return "https://www.theguardian.com/world/asia-pacific+world/south-and-central-asia"
        else:
            return link
    except Exception as e:
        print(e)

#get main navigation site options
def get_main_navigation_options_links():

    try:

        site_response = requests.get("https://www.theguardian.com/uk")

        siteSouped = BeautifulSoup(site_response.content, "html.parser")

        news_nav =  siteSouped.find("li", {"data-section-name" : "News"})

        news_nav_links = news_nav.find_all("a")

        news_nav_links_list = []

        for link in news_nav_links:
            just_link = link['href']
            if just_link == "https://www.theguardian.com/football":
                continue
            else:
                news_nav_links_list.append(just_link)

        print(news_nav_links_list)

        return news_nav_links_list

    except Exception as e:
        print(e)

#crawl through sutopic section of the site
def run_through_subtopics_panel(site_link):

    try:

        print("NEXT SITE") #test
        print(site_link) #test

        world_response = requests.get(site_link) #send site request
        worldSouped = BeautifulSoup(world_response.content, "html.parser") #make bs object
        world_subNav = worldSouped.find("ul", {"data-pillar-title" : "News"})# #look for unordered list <ul> element
        world_subNav_link = world_subNav.find_all("a") #find links <a> in element
        first_link_class = world_subNav_link[0]['class'] #extract class for further checks
        

        if len(first_link_class) > 1: #check if site has subnav section
            print(True) #test

            for i in range(1, (len(world_subNav_link))): #iterate through every subnav site
                link = world_subNav_link[i]["href"] #extract link
                print(link) #test

                crawl_first_two_site_pages(link) #send link to function

        else: #if site has no subnav section
            (print('NO SUBTOPICS PANEL')) #test
            crawl_first_two_site_pages(site_link) #send link to function

    except Exception as e:
        print(e)

#run this program
def run_the_guardian():

    try:

        main_navigation_options_links_list = get_main_navigation_options_links()

        print("MAIN NAVIGATION OPTIONS")

        for link in main_navigation_options_links_list:
            print(link)
            run_through_subtopics_panel(link)

    except Exception as e:
        print(e)
