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
from webdriver_manager.chrome import ChromeDriverManager



def main():
    x = 6
    while x > 0:
        if os.path.isfile(getPrevPath(x)) == False:
            page = parsePrevPage(x)
            print(getPrevPath(x) + " doesn't exist")
            urlretrieve(getPrevImage(page), getPrevPath(x))
            print(getPrevDescription(page) + " by " + getPrevAuthor(page))
            imgInfo = {270: getPrevDescription(page), 315: getPrevAuthor(page)}
            imgData = piexif.dump({"0th":imgInfo})
            piexif.insert(imgData, getPrevPath(x))
        x -= 1
    currentImgPath = "C:/Users/Aristo/Downloads/BingWallpaper-" + str(getCurrentDate()) + ".jpg"
    if os.path.isfile(currentImgPath) == False:
        page = parseCurrentPage()
        print(currentImgPath + " doesn't exist")
        urlretrieve(getCurrentImage(page), currentImgPath)
        print(getCurrentDescription(page) + " by " + getCurrentAuthor(page))
        imgInfo = {270: getCurrentDescription(page), 315: getCurrentAuthor(page)}
        imgData = piexif.dump({"0th":imgInfo})
        piexif.insert(imgData, currentImgPath)

def getCurrentDate():
    uk = pytz.timezone('Europe/London')
    return datetime.now(uk).date()

def getCurrentImage(source):
    imgLink = "https://bing.com" + source.split('"Image":{"Url":"')[1].split("\\")[0]
    return imgLink

def getCurrentDescription(source):
    descDiv = source.split('"Title":"')[1].split('","')[0]
    return descDiv

def getCurrentAuthor(source):
    authDiv = source.split('"Copyright":"© ')[1].split('","')[0]
    return authDiv

def parseCurrentPage():
    arg = webdriver.ChromeOptions()
    arg.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.maximize_window()
    browser.get("https://www.bing.com/?cc=gb")
    #img = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Want to see the Bing daily image?")))
    #browser.implicitly_wait(1)
    #img.click()
    source = browser.page_source
    browser.close()
    return source

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
    desc = source.split('Image of the day: ')[1].split('"')[0]
    return desc

def getPrevAuthor(source):
    auth = source.split('copyright">© ')[1].split('</div>')[0]
    return auth

def parsePrevPage(day):
    arg = webdriver.ChromeOptions()
    arg.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.maximize_window()
    browser.get("https://www.bing.com/?cc=gb")
    cookie_reject = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "bnp_btn_reject")))
    browser.implicitly_wait(3)
    cookie_reject.click()
    #img = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Want to see the Bing daily image?")))
    #browser.implicitly_wait(1)
    #img.click()
    x = 0
    while x < day:
        back = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, "leftNav")))
        browser.implicitly_wait(3)
        back.click()
        x += 1
    source = browser.page_source
    browser.close()
    return source


if __name__ == "__main__":
    main()