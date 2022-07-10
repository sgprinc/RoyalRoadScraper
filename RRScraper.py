import argparse
import requests
import os
import time
from bs4 import BeautifulSoup

# Global variables
baseURL = "https://www.royalroad.com"
outputBaseDir = "./Novels/"
overwriteExisting = False
useTemplate = True
scrapeDelay = 1


def useChapterTemplate(chapterData, chapterHTML):
    # Use a template to wrap the raw chapter content HTML
    with open("./Templates/ChapterHTML.html") as ct:
        soup = BeautifulSoup(ct, 'html.parser')
        soup.find("title").string = chapterData["name"]         # Set chapter title for browser-tab convenience
        content = soup.find("div", {"id":"chapter-content"})
        content.replace_with(chapterHTML)                       # Replace template placeholder with chapter content
        return soup

def fetchChapterList(novelName, novelURL):
    # Scrape the novel's index page to obtain a list of chapter 
    print(f"> Fetching chapter links for {novelName}...")
    if baseURL not in novelURL:                                 # Support both short-handed and full links
        novelURL = baseURL + novelURL   
    
    fictionPage = requests.get(novelURL)
    soup = BeautifulSoup(fictionPage.content, "html.parser")    
    chapterTable = soup.find("table",  {"id":"chapters"})
    
    startTime = time.time()
    chapterList = list()
    for row in chapterTable.findAll("tr")[1:]:                  # Iterate over the table rows and extract the data
        chapterData = {}        
        chapterData["name"] = row.find("td").find("a").contents[0].strip()        
        chapterData["link"] = row.find("td").find("a")["href"]
        chapterData["date"] = row.find("td", {"class":"text-right"}).find("a").contents[1]['title']
        chapterList.append(chapterData)    
    endTime = time.time()

    if args.verbose:
        print(f"> Fetched links for {len(chapterList)} chapters ({endTime-startTime}s)")
    return chapterList

def prepareOutputFolder():
    # Ensure there is an output folder to store the chapters to
    outputDir = outputBaseDir + (args.out or args.name)
    if not os.path.exists(outputDir):                    # Ensure the output directory exists
        os.makedirs(outputDir)
    
    if args.verbose:
        print(f" - Storing chapters in: {outputDir}")
    return outputDir

def scrapeChapter(chapterData, outputDir):
    # Scrape the contents of a given chapter

    filename = "".join(x for x in chapterData['name'] if (x.isalnum() or x in "- "))
    if not overwriteExisting and os.path.exists(f"{outputDir}{filename}.html"):
        if args.verbose:
            print(f" - Skipping chapter {filename} (already exists)")
        return

    chapterPage = requests.get(baseURL + chapterData["link"])
    soup = BeautifulSoup(chapterPage.content, "html.parser")
    chapterContent = soup.find("div", {"class":"chapter-content"})    
    if useTemplate: chapterContent = useChapterTemplate(chapterData, chapterContent)
    html = chapterContent.prettify("utf-8")
    
    filename = "".join( x for x in chapterData['name'] if (x.isalnum() or x in "._- "))
    with open(f"{outputDir}/{filename}.html", "wb") as file:
        file.write(html)
        if args.verbose:
            print(f" - Scraped chapter {filename}")
    
    time.sleep(scrapeDelay)                                     # Wait a certain amount of time inbetween chapters to be polite

if __name__ == "__main__":
    # Configure the scripts execution arguments
    parser = argparse.ArgumentParser(description="Scrape Novels from RoyalRoad.")
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')
    required.add_argument("-n", "--name", help="Novel's name", required=True)
    required.add_argument("-l", "--link", help="Link to the novel's index", required=True)
    optional.add_argument("-o", "--out", help="Output directory")
    optional.add_argument("-v", "--verbose", help="Execute in verbose mode", action="store_true")
    args = parser.parse_args()

    # Get the chapter list, prepare a folder and get those chapters!
    chapterList = fetchChapterList(args.name, args.link)
    outputDir = prepareOutputFolder()
    [scrapeChapter(chapter, outputDir) for chapter in chapterList]