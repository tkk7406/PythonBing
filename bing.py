from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as beausoup
from datetime import datetime
import pytz
import os.path
import piexif


def main():
    imgPath = "C:/Users/Aristo/Downloads/BingWallpaper-" + getDate() + ".jpg"
    if os.path.isfile(imgPath) == False:
        urlretrieve(getImage(), imgPath)
        imgInfo = {270: getDescription(), 315: getAuthor()}
        imgData = piexif.dump({"0th":imgInfo})
        piexif.insert(imgData, imgPath)

def getImage():
    imgDiv = parsePage().select_one("div.img_cont")
    imgLink = "https://bing.com" + imgDiv['style'].split("url(")[1].split(")")[0]
    return imgLink

def getDescription():
    descDiv = parsePage().select_one("a.title")
    return descDiv.text

def getAuthor():
    authDiv = parsePage().select_one("div.copyright")
    return authDiv.text.split("© ")[1]

def parsePage():
    source = "https://www.bing.com/?cc=gb"
    client = urlopen(source)
    page = client.read()
    client.close()
    return beausoup(page, "html.parser")

def getDate():
    uk = pytz.timezone('Europe/London')
    return str(datetime.now(uk).date())

if __name__ == "__main__":
    main()