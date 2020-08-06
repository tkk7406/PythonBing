from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as beausoup
from datetime import datetime, timedelta
import pytz
import os.path
import piexif
import html
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    x = 6
    while x > 0:
        if os.path.isfile(getPrevPath(x)) == False:
            page = parsePrevPage(x)
            print(getPrevPath(x) + " doesn't exist")
            urlretrieve(getPrevImage(page), getPrevPath(x))
            imgInfo = {270: getPrevDescription(page), 315: getPrevAuthor(page)}
            imgData = piexif.dump({"0th":imgInfo})
            piexif.insert(imgData, getPrevPath(x))
        x -= 1
    #currentImgPath = "C:/Users/Aristo/Downloads/BingWallpaper-" + str(getCurrentDate()) + ".jpg"
    currentImgPath = "C:/Users/Aristo/Downloads/BingWallpaper-" + str(getCurrentDate()) + ".jpg"
    if os.path.isfile(currentImgPath) == False:
        urlretrieve(getCurrentImage(), currentImgPath)
        imgInfo = {270: getCurrentDescription(), 315: getCurrentAuthor()}
        imgData = piexif.dump({"0th":imgInfo})
        piexif.insert(imgData, currentImgPath)

def getCurrentDate():
    uk = pytz.timezone('Europe/London')
    return datetime.now(uk).date()

def getCurrentImage():
    imgDiv = parseCurrentPage().select_one("div.img_cont")
    imgLink = "https://bing.com" + imgDiv['style'].split("url(")[1].split(")")[0]
    return imgLink

def getCurrentDescription():
    descDiv = parseCurrentPage().select_one("a.title")
    return descDiv.text

def getCurrentAuthor():
    authDiv = parseCurrentPage().select_one("div.copyright")
    return authDiv.text.split("© ")[1]

def parseCurrentPage():
    source = "https://www.bing.com/?cc=gb"
    client = urlopen(source)
    page = client.read()
    client.close()
    return beausoup(page, "html.parser")

def getPrevPath(day):
    date = str(getCurrentDate() - timedelta(days=day))
    return ("C:/Users/Aristo/Downloads/BingWallpaper-" + date + ".jpg")

def getPrevImage(source):
    imgExt = source.split("background-image: url(")[1].split("rf=")[0]
    imgExt = html.unescape(imgExt)
    if '"' in imgExt:
        imgExt = imgExt[1:]
    if "&" in imgExt:
        imgExt = imgExt[:-1]        
    imgLink = "https://bing.com" + imgExt
    return imgLink

def getPrevDescription(source):
    desc = source.split('"title">')[1].split("</a>")[0]
    print(desc)
    return desc

def getPrevAuthor(source):
    auth = source.split('"copyright">© ')[1].split("</div>")[0]
    return auth

def parsePrevPage(day):
    arg = webdriver.ChromeOptions()
    arg.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(options=arg)
    browser.get("https://www.bing.com/?cc=gb")
    x = 0
    while x < day:
        back = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "leftNav")))
        browser.implicitly_wait(2)
        back.click()
        #browser.execute_script("arguments[0].click();", back)
        x += 1
    source = browser.page_source
    browser.close()
    return source


if __name__ == "__main__":
    main()