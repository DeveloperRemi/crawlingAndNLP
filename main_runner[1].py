import bbcScrape
import time
import DailyMail
import guardianScrape
import mirrorScrape
import theSun

#THIS IS THE PART OF THE PROGRAM WHERE EVERY CRAWLER IS ACTIVATED


#running this class will start this loop that will start the process and it will run until stopped manually
counter = 0
while(True):

    bbcScrape.run_bbc_scrape()

    print(f"BBC DONE {counter} TIMES. SLEEPING")
    time.sleep(300)

    DailyMail.run_daily_mail()
    print(f"DAILY MAIL DONE {counter} TIMES. SLEEPING")

    time.sleep(300)

    guardianScrape.run_the_guardian()
    print(f"GUARDIAN DONE {counter} TIMES. SLEEPING")

    time.sleep(300)

    mirrorScrape.run_mirror_scrape()
    print(f"MIRROR DONE {counter} TIMES. SLEEPING")

    time.sleep(300)

    theSun.visit_site_bring_nav_list()
    print(f"THE SUN DONE {counter} TIMES. SLEEPING")

    time.sleep(300)

    counter += 1









