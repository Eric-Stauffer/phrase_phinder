from bs4 import BeautifulSoup
import requests
import os
import fileinput
import re
import time
episodeLinks = []

def createEpisodeList(seriesPath):
    aList = []
    source = requests.get(seriesPath).text
    # open soup and find correct section of episodes
    soup = BeautifulSoup(source,'html.parser')
    episodesSection = soup.table

    episodes = episodesSection.find_all("tr")
    # create list of seasons
    for episode in episodes:
        aList.append(episode.find("a"))
    # add this pages hrefs and and titles to episodeLinks
    for item in aList:
        if(item != None):
            text = item.text.split()
            text[0] = text[0].replace("/","-")
            href = item.get('href')
            # href[1:] removes first character in string for some reason was returning with period at start of string
            nameAndRef = [text[0], href[1:]]
            if(text[0][0] == "0" or text[0][0] == "1" or text[0][0] == "2" or text[0][0] == "3" or text[0][0] == "4" or text[0][0] == "5"):
                episodeLinks.append(nameAndRef)

    if (nextPageLink(soup) != None):
        createEpisodeList("https://transcripts.foreverdreaming.org/" +nextPageLink(soup))
    else:
        makeFolderAndFile(episodeLinks,setShowName(soup))

def setShowName(soup):
    breadCrumbsHeader = soup.find("p", class_="breadcrumbs")
    aTags = breadCrumbsHeader.find_all("a")

    showName = aTags[len(aTags)-1].text
    return showName

def nextPageLink(soup):
    pageHeader = soup.find("div",class_="boxbody clearfix")
    aTags = pageHeader.find_all("a")
    for tag in aTags:
        if (tag.text == "»"):
            href = tag.get("href")
            return href[1:]


def makeFolderAndFile(episodeLinks,showName):
    os.mkdir(os.path.join(os.getcwd(),showName))
    for nameAndHref in episodeLinks:
        episodePath = os.path.join(os.getcwd(),showName,str(nameAndHref[0]))

        file = open(episodePath,"w")
        file.write(scanEpisode(nameAndHref[1]))
        file.close()
        makeFileMultipleLines(episodePath)
        makeFileLowerCase(episodePath)
        stripFile(episodePath)




def scanEpisode(episodePath):
    try:
        source = requests.get("https://transcripts.foreverdreaming.org"+str(episodePath)).text
    except:
        return ""
    returnString = ""
    soup = BeautifulSoup(source,'html.parser')
    postBody = soup.find("div",class_="postbody")
    pTags = postBody.find_all('p')
    for line in pTags:

        returnString += (line.text + " ")

    return returnString

def makeFileLowerCase(episodeString):
    file = open(episodeString, "rt")
    data = file.read()
    data = data.replace(data, data.lower())
    file.close()

    fin = open(episodeString, "wt")
    fin.write(data)
    fin.close()

def makeFileMultipleLines(episodeString):
    with fileinput.FileInput(episodeString, inplace=True,) as file:
        for line in file:
            print(re.sub(r'( )(?=[a-zA-Z]*(: ))',"\n",line),end = '')

def stripFile(episodeString):
    with fileinput.FileInput(episodeString, inplace=True,) as file:
        for line in file:
            print(re.sub(r'(\[)[,\'\"_\-a-zA-Z0-9\s!()$#@/]*(])',"",line),end = '')
    with fileinput.FileInput(episodeString, inplace=True, ) as file:
        for line in file:
            print(re.sub(r'[^:a-zA-Z0-9\s]',"",line),end = '')


startTime = time.time()
createEpisodeList("https://transcripts.foreverdreaming.org/viewforum.php?f=194&sid=0a5a963468b3692bfecee741602f507b")
endTime = time.time()
print("this took " + str(endTime-startTime)+"seconds")


