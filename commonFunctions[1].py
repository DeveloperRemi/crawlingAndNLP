import csv

#this file contains two functions that was reused by every scraping program in this project

#write article title, text, and link to specified file
def write_row_to_csv(title, article_text, file_name, link_of_article):


    #open csv file and write to rows
    with open(file_name, 'a', newline='') as file: #open csv in APPEND mode, so it does not overwrite
        writer = csv.writer(file) #initiate csv object
        writer.writerow([title, article_text, link_of_article]) #first row

#check if the article already exist in the dataset
def check_if_title_name_and_article_text_exist_in_file(title, article_text, file_name, link_of_article):


    #opne csv file to read and compare
    with open(file_name, 'r') as file: #open csv for reading
        csvreader = csv.reader(file) #initiate csv object

        

        
        for row in csvreader: #for every row in csv file
            if len(row) == 0: #check for len in case file is completely empty
                continue #continue loop

            for row in csvreader:
                if row[2] == link_of_article:
                    return True #return true for link

            else: 
                var = row[0] #set variable for title from row
                var1 = row[1] #set variable to article text from row

                if var == title: #compare title text with title text in row, return False in NOT True
                    print("TRUE FOR TITLE")

                    if var1 == article_text: #compare article text with article text in row, return False if NOT True
                        print("TRUE FOR ARTICLE TEXT")
                        print("THE COUNTER IS:")                       
                        return True #return True for function if TITLE and ARTICLE text both match respective texts in the row
    
            
                            
        return False