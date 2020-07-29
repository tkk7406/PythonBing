from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as beausoup
from datetime import datetime
import pytz


def main():    
    urlretrieve(getImage(), "C:/Users/Aristo/Desktop/Coding Projects/Python Web Scraping/" + getDate() + ".jpg")
    print("main")

def getImage():
    source = "https://www.bing.com/?cc=gb"
    client = urlopen(source)
    print("client")
    page = client.read()
    print("read")
    client.close()
    parsed = beausoup(page, "html.parser")
    print("parsed")
    imageDiv = parsed.select_one("div.img_cont")
    imageLink = "https://bing.com" + imageDiv['style'].split("url(")[1].split(")")[0]
    print("saved")
    return imageLink

def getDate():
    uk = pytz.timezone('Europe/London')
    date = str(datetime.now(uk).year()) + "-" + str(datetime.now(uk).month()) + "-" + str(datetime.now(uk).day())
    print(datetime.now(uk).date())
    return date

if __name__ == "__main__":
    print("start")
    main()