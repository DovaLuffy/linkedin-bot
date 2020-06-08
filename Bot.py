#The needed libraries for this bot
import os, random, sys, time
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup

#finds the webdriver and reads your linkedin username and password
browser = webdriver.Chrome("Webdriver/chromedriver.exe")
browser.get("https://www.linkedin.com/login")
file = open("config.txt")
lines = file.readlines()
username = lines[0]
password = lines[1]

#inputs the given username and password inside of the website elements
elementID = browser.find_element_by_id("username")
elementID.send_keys(username)
elementID = browser.find_element_by_id("password")
elementID.send_keys(password)

#clicks the login button
elementID.submit()

#gets directed to the given username link and the full linkedin address
visitingProfileID = "/mynetwork/"
fullLink = "https://www.linkedin.com" + visitingProfileID
browser.get(fullLink)

#arrays to store the data of profiles that have been visited and the profiles that are in queue
visitedProfiles = []
profilesQueued = []

#function that goes to each user that viewed your linkedin account and takes their username
def getNewProfileIDS(soup, profilesQueued):
    profilesID = []
    pav = soup.find(
        "li",
        {
            "class": "mn-cohort-view ember-view"
        }
    )
    all_links = pav.findAll("a", {"class": "discover-entity-type-card__link ember-view"})

    for link in all_links:
        userID = link.get("href")
        if (userID not in profilesQueued) and (userID not in visitedProfiles):
            profilesID.append(userID)
    return profilesID

getNewProfileIDS(BeautifulSoup(browser.page_source), profilesQueued)



profilesQueued =getNewProfileIDS(BeautifulSoup(browser.page_source), profilesQueued)

#WHERE THE WHOLE PROCESS BEGINS 
#It checks the queued profiles by inspecting the page elements and using the previous function and then clicking connect and sending them a message 

while profilesQueued:
    try:
        visitingProfileID = profilesQueued.pop()
        visitedProfiles.append(visitingProfileID)
        fullLink = 'https://www.linkedin.com' + visitingProfileID
        browser.get(fullLink)

        browser.find_element_by_class_name('pv-s-profile-actions').click()

        browser.find_element_by_class_name('mr1').click()

        customMessage = "Hello, I would really appreciate it if you would accept my invitation, because I want to connect with more people in the industry. I hope in the future I can contact you for advice if possible"
        elementID = browser.find_element_by_id('custom-message')
        elementID.send_keys(customMessage)

        browser.find_element_by_class_name('ml1').click()

        # Add the ID to the visitedUsersFile
        with open('visitedUsers.txt', 'a') as visitedUsersFile:
            visitedUsersFile.write(str(visitingProfileID)+'\n')
        visitedUsersFile.close()

        # Get new profiles ID
        soup = BeautifulSoup(browser.page_source)
        try: 
            profilesQueued.extend(getNewProfileIDS(soup, profilesQueued))
        except:
            print('Continue')

        # Pause
        time.sleep(random.uniform(3, 7)) # Otherwise, sleep to make sure everything loads

        if(len(visitedProfiles)%50==0):
            print('Visited Profiles: ', len(visitedProfiles))

        if(len(profilesQueued)>100):
            with open('profilesQueued.txt', 'a') as visitedUsersFile:
                visitedUsersFile.write(str(visitingProfileID)+'\n')
            visitedUsersFile.close()
            print('100 Done!!!')
            break;
    except:
        print('error')


