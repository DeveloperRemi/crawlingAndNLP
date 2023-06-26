import requests
from bs4 import BeautifulSoup
import commonFunctions

#scrape article title and text of a given link
def single_site_data_to_csv(single_link):

    try:

        page  = requests.get(single_link) #send request of site
        soup = BeautifulSoup(page.content, "html.parser") #parse the content
        title = soup.find("h1")
        title = title.text
        print("THIS IS TITLE") #test
        print(title) #test
        content = soup.find("div", class_ = "article__content") #find main page section
        article_str = ""
        all_ps = content.find_all("p")
        for i in all_ps:
            article_str += i.text
            article_str += " "

        print("THIS IS ARTICLE") #test
        print(article_str) #test

        if not commonFunctions.check_if_title_name_and_article_text_exist_in_file(title, article_str, "theSun_Data.csv", single_link): #check for duplicates function
            commonFunctions.write_row_to_csv(title, article_str, "theSun_Data.csv", single_link) #if no duplicates found, then write to csv file

    except Exception as e:
        print(e)

#get links to articles in a given subsection site
def visit_sub_nav_site_get_all_titles_and_links(sub_nav_site_link):

    try:

        URL = "https://www.thesun.co.uk"

        page  = requests.get(sub_nav_site_link) #send request of site
        soup = BeautifulSoup(page.content, "html.parser") #parse the content
        section = soup.find("section", class_ = "sun-container__home-section") #find main page section

        containers = section.find_all("div", class_ = "teaser__copy-container")

        #find_titles = containers.find_all("a", href = True)

        for i in containers:
            link = i.find("a")['href'] #get link to site
            link = URL + link
            print(link) #test
            single_site_data_to_csv(link)

    except Exception as e:
        print(e)
   
#get link options from the main site option panel
def visit_nav_site(link):

    try:
        #all these variables contain sub nav site relative to project
        News_tab = ["UK News", "World News", "Politics", "Health News", "Science"]
        Money_tab = ["Money News", "Property", "Business"]
        Health_tab = ["News"]
        Tech_tab = ["News"]

        page  = requests.get(link) #send request of site
        soup = BeautifulSoup(page.content, "html.parser") #parse the content
        sub_nav = soup.find("ul", {"id" : "sun-sub-menu"})
        sub_nav_links = sub_nav.find_all("a", href = True)

        for i in sub_nav_links:

            if "/news/" in link and i.text in News_tab: #check if link is from news tab
                sub_nav_site = i['href'] #variable for comfort
                print(i['href']) #test
                visit_sub_nav_site_get_all_titles_and_links(sub_nav_site) #call function to scrape titles and links
            elif "/money/" in link and i.text in Money_tab: #check if link is from money tab
                sub_nav_site = i['href'] #variable for comfort
                print(i['href']) #test
                visit_sub_nav_site_get_all_titles_and_links(sub_nav_site) #call function to scrape titles and links
            elif "/heath/" in link and i.text in Health_tab: #check if link is from health tab
                sub_nav_site = i['href'] #variable for comfort
                print(i['href']) #test
                visit_sub_nav_site_get_all_titles_and_links(sub_nav_site) #call function to scrape titles and links
            elif "/tech/" in link and i.text in Tech_tab: #check if link is from tech tab
                sub_nav_site = i['href'] #variable for comfort
                print(i['href']) #test
                visit_sub_nav_site_get_all_titles_and_links(sub_nav_site) #call function to scrape titles and links

    except Exception as e:
        print(e)

#run this program
def visit_site_bring_nav_list():

    try:

        list_of_main_nav_strings = ["News", "Money", "Health", "Tech"] #nav sites needed
        URL = "https://www.thesun.co.uk" #main site URL

        page  = requests.get(URL) #send request of site 

        soup = BeautifulSoup(page.content, "html.parser") #parse the content

        results = soup.find("ul", {"id" : "sun-menu"}) #navigation bar ul

        nav_links = results.find_all("a", href = True) #find all <a> elements

        for i in nav_links: #loop thru all <a> elements
            if i.text in list_of_main_nav_strings: #extract needed sites
                needed_site_link = i['href'] #needed site variable
                visit_nav_site(needed_site_link)
                print(needed_site_link) #test

    except Exception as e:
        print(e)

            





