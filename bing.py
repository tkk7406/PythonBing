from urllib.request import urlopen
from bs4 import BeautifulSoup as beausoup

source = "https://www.bing.com/?cc=gb"
client = urlopen(source)
page = client.read()
client.close()
parsed = beausoup(page, "html.parser")
#print(parsed)
imageDiv = parsed.findAll("div", {"class":"img_cont"})
temp = imageDiv[0]
imageLink = "https://bing.com/" + imageDiv[0]['url']
#print(len(imageCont))
print(temp)
#print(imageLink)