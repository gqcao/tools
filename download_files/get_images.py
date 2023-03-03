import re
import requests
from bs4 import BeautifulSoup
from pdb import set_trace
import subprocess

root_path = '/home/gcao/tmp/slides'
site = "https://auto.gasgoo.com/news/202205/23I70301923C601.shtml"

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = []
for img in img_tags:
    if img.has_attr('data-src'):
        urls.append(img['data-src'])
cnt = 0
set_trace()
for url in urls:
    # sleep(5) #throttle so you dont hammer the site
    # downloadlink(l)
    command = "cd "+ root_path +"; " +  "wget " + url + ' -O ' + str(cnt).zfill(5) + '.jpg'
    #command = "cd "+ root_path +"; " +  "wget " + base_url + l.attrs['href']
    cnt = cnt + 1
    subprocess.call(command, shell=True)
