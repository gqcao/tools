import re
import requests
from bs4 import BeautifulSoup as BS
from pdb import set_trace
import subprocess

file_path = '/home/gcao/tmp/xlsx/'
site = ''
base_url = ''
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
page = requests.get(site, headers=agent)
soup = BS(page.text, 'html.parser')
img_tags = soup.find_all('a')
#urls = []
names = []

for i, link in enumerate(soup.findAll('a')):
    full_url = site + link.get('href')
    if full_url.endswith('.xlsx'):
        #urls.append(full_url)
        names.append(soup.select('a')[i].attrs['href'])
for name in names:
    # sleep(5) #throttle so you dont hammer the site
    # downloadlink(l)
    command = "cd "+ file_path +"; " +  "wget " + base_url + name
    subprocess.call(command, shell=True)
