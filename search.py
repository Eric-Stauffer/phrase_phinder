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

                print("Your search is around",minutesIntoEpisode,"minutes and", secondsIntoEpisode, "seconds into episode", str(episode),"season",season)
                return True
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




def main():
    searchString = input("Enter what you want to search for: ").lower()
    searchString = stripSearchString(searchString)

    for episode in os.listdir(os.path.join(os.getcwd(),"The Office")):
        episodeNumber = ""
        seasonNumber = ""
        for i in range(len(episode)):
            if i < 2:
                seasonNumber += episode[i]
            elif i > 2:
                episodeNumber += episode[i]

        searchFunction(os.path.join(os.getcwd(),"The Office",(seasonNumber + "x" + episodeNumber)),searchString,seasonNumber,episodeNumber)



    # for season in range(1,len(os.listdir(os.path.join(os.getcwd(),"seasons"))) + 1):
    #     for episode in range(1,len(os.listdir(os.path.join(os.getcwd(),"seasons","season_"+str(season)))) + 1):
    #         searchFunction(os.path.join(os.getcwd(),"seasons","season_"+ str(season),"episode_"+str(episode)+".txt"),searchString,season,episode)




main()