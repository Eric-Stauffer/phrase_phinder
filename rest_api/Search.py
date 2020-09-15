import os
import re

def amountOfLinesInFile(episodeString):
    count = 0
    with open(episodeString, 'r') as file:
        for line in file:
            count += 1
        return count

def searchFunction(episodeString,searchString,season,episode):
    count = 0
    with open(episodeString) as fileInput:
        for line in fileInput:
            count += 1
            if searchString in line:
                episodeInMinutes = 22
                secondsInEpisode = episodeInMinutes*60
                percentInEpisode = (count/amountOfLinesInFile(episodeString))
                minutesIntoEpisode = (secondsInEpisode*percentInEpisode)//60
                secondsIntoEpisode = round((secondsInEpisode*percentInEpisode)%60)
                return {"season": season,"episode":episode,"minute":minutesIntoEpisode,"second":secondsIntoEpisode}
                # return ("Your search is around",minutesIntoEpisode,"minutes and", secondsIntoEpisode, "seconds into episode", str(episode),"season",season)

def findNumberOfEpisodes(seasonNumber):
    import os
    seasonPath = "/Users/user/Desktop/office_transcripts/season_0" + str(seasonNumber)

    list = os.listdir(seasonPath)
    number_files = len(list)
    return number_files
def stripSearchString(searchString):
    searchString.islower()
    searchString = re.sub(r'[^a-zA-Z0-9\s]',"",searchString)
    return searchString




def main(searchString):
    episode_list = []
    searchString = stripSearchString(searchString).lower()
    for episode in os.listdir(os.path.join(os.getcwd(),"The Office")):
        episodeNumber = ""
        seasonNumber = ""
        for i in range(len(episode)):
            if i < 2:
                seasonNumber += episode[i]
            elif i > 2:
                episodeNumber += episode[i]
        search_response = searchFunction(os.path.join(os.getcwd(),"The Office",(seasonNumber + "x" + episodeNumber)),searchString,seasonNumber,episodeNumber)
        if(search_response):
            episode_list.append(search_response)
    return {"episode_number":len(episode_list),"episodes":episode_list}







