import re
import requests
from bs4 import BeautifulSoup
from pdb import set_trace
import subprocess

root_path = '/home/gcao/tmp/'
site = 'https://mp.weixin.qq.com/s/oOYGa4Mti6KpkpI4TtpitQ'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = []
for img in img_tags:
    if img.has_attr('data-src'):
        urls.append(img['data-src'])
cnt = 0
for url in urls:
    # sleep(5) #throttle so you dont hammer the site
    # downloadlink(l)
    command = "cd "+ root_path +"; " +  "wget " + url + ' -O ' + str(cnt).zfill(5) + '.jpg'
    #command = "cd "+ root_path +"; " +  "wget " + base_url + l.attrs['href']
    cnt = cnt + 1
    subprocess.call(command, shell=True)
