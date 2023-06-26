import requests
from bs4 import BeautifulSoup
import commonFunctions

URL = "https://www.bbc.co.uk" #main URL


#get list of elements in the site main navigation panel
def get_nav_site_list():

    try:

        START_URL = "https://www.bbc.co.uk/news"

        site_list = []

        page  = requests.get(START_URL) #send request of site

        soup = BeautifulSoup(page.content, "html.parser") #parse the content

        results = soup.find("nav", class_="nw-c-nav__wide", role="navigation") #navigation bar div

        links = results.find_all("a", href = True) #link extraction

        #make list of links
        for link in links:
            full_url = URL + link["href"] #temp variable
            print(URL + link["href"]) #connect with domain URL

            #few conditions to avoid going to BBC sites to avoid redudant topics, like personal stories, sports etc
            if "/av/" in full_url: #chech for video reports
                pass #NOT include in list if link is a video report
            elif 'news/stories' in full_url: #check for BBC stories rubric
                pass #NOT include in list if link is BBC stories rubric
            elif 'news/world_radio' in full_url: #check for world radio tv rubric
                pass #NOT include in the list if from world radio tv rubric
            elif 'news/newsbeat' in full_url: #check for newsbeat rubric
                pass #NOT include in the list if link from newsbear rubric
            elif full_url == "https://www.bbc.co.uk/news": #exclude first site, no latest updates section there
                pass
            else:
                site_list.append(full_url) #append list


        print(site_list) #test
        return site_list #return list
    
    except Exception as e:
        print(e)

#get list of articles at the end of the site
def get_links_from_latest_updates_section(soup):

    try:

        print("------------ LINK LIST IN SITE ------------") #test

        latest_updates_section = soup.find(id = "latest-updates") #find organised list element, usually one per BBC site
        ol = latest_updates_section.parent #select parent element which will contain all links
        links = ol.find_all("a", href = True) # extract links

        temp_list = [] #temp list initialization for checking for duplicate links
        for link in links: #in every link
            if "/terms/" in link["href"] or "/correspondents" in link["href"]: # check if link is not to terms site, frequent in this part of the site
                continue #finish this loop round
            elif "instagram.com" in link['href']:
                continue
            elif "/twitter.com/" in link["href"] or "nhs.uk" in link["href"] or "punchng.com" in link["href"]: #check if the link is from twitter or nhs
                continue
            elif "gov.uk" in link["href"] or ".org" in link["href"] or "parliament.uk" in link["href"]: #check if link is from gov or any .org site
                continue
            elif link["href"] in temp_list: #check if links duplicate
                continue #finish this loop round
            elif "bbc.co.uk" in link["href"] or "bbc.com" in link["href"]:#if link comes with site domain part, cut to end link. Domain is added later in all links anyway
                test_link = link['href']
                print("WITH DOMAIN") #test
                print(test_link)
                if "bbc.com" in test_link:
                    cut_link = "/" + link["href"][link["href"].index("m")+2 :] #cut the bbc domain part
                    print(cut_link)
                if "bbc.co.uk" in test_link:
                    cut_link = "/" + link["href"][link["href"].index("k")+2 :] #cut the bbc domain part
                    print(cut_link)
                if cut_link in temp_list: #check for duplicates
                    continue #dont append list if duplicate
                else:
                    temp_list.append(cut_link) #append temp list
            else:
                print(link["href"]) #test print link
                temp_list.append(link["href"]) #add link to temp list to avoid duplicates

        return temp_list #return link list

    except Exception as e:
        print(e)

#scrape and store title, article text and link
def scrape_bbc_title_and_article_text(site_link):

    try:

        page = requests.get(site_link) #send request to site link
        soup = BeautifulSoup(page.content, "html.parser") # soup and parse content

        h1 = soup.find("h1")
        title = h1.text

        text = soup.find_all("div", { "data-component" : "text-block" }) #find all text-block components on acticle site

        print("TEXT STARTS HERE --------") #test

        full_text_string = "" #initiale variable to contain full string

        for i in text: #loop to connect all text element to one string

            print(i.text) #test
            print("") #test
            full_text_string += i.text #every text component
            full_text_string += " " # add a space after every text component

        print("FULL TEXT STRING: ---------") #test

        print(full_text_string) #test

        return title, full_text_string #return title and full article text in separate variables

    except Exception as e:
        print(e)

#collect articles and links to them in the page
def scrape_site_in_navigation_bar(navigation_bar_site_link):

    try:

        page = requests.get(navigation_bar_site_link)# send request
        soup = BeautifulSoup(page.content, "html.parser") #parse request to BS object

        links_list = get_links_from_latest_updates_section(soup) #lauch function to get links

        for link in links_list: #run thru links
            whole_link = URL + link #combine full link
            try:
                title_text, article_text = scrape_bbc_title_and_article_text(whole_link) #lauch scraping function
            except Exception as e:
                print(e)

            if not commonFunctions.check_if_title_name_and_article_text_exist_in_file(title_text, article_text, "BBC_Data.csv", whole_link): #check for duplicates function
                commonFunctions.write_row_to_csv(title_text, article_text, "BBC_Data.csv", whole_link) #if no duplicates found, then write to csv file

    except Exception as e:
        print(e)

#run this part of program
def run_bbc_scrape():

    try:

        nav_site_list = get_nav_site_list() #get nav site list

        the_site = nav_site_list[1] #test

    #run thru  nav site list
        for site in nav_site_list:

            print("ALGORITHM WILL START HERE WITH THIS NAV SITE:") #test
            print(site) #test
            try: #try for connection error handling
                scrape_site_in_navigation_bar(site) #lauch srape site function
                #commonFunctions.write_row_to_csv("NAV BAR SITE FINISHED", "NEW ONE STARTING NOW", "BBC_Data.csv") #test
                #commonFunctions.write_row_to_csv(site, "", "BBC_Data.csv") #test
            except ConnectionError as e: #handle error
                print(e) #print error
    
    except Exception as e:
        print(e)
    
