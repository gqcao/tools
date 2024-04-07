import re
import requests
from bs4 import BeautifulSoup
import subprocess

root_path = '/home/gcao/tmp/pics'
site = "https://yle.fi/a/74-20082473"

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = []
yle_base_url = "https://images.cdn.yle.fi/image/upload/"
for img in img_tags:
    if img.has_attr('src'):
        urls.append(yle_base_url + img['src'].split("/")[-1])
cnt = 0
for url in urls:
    # sleep(5) #throttle so you dont hammer the site
    # downloadlink(l)
    command = "cd "+ root_path +"; " +  "wget " + url + ' -O ' + str(cnt).zfill(5) + '.jpg'
    #command = "cd "+ root_path +"; " +  "wget " + base_url + l.attrs['href']
    cnt = cnt + 1
    subprocess.call(command, shell=True)
