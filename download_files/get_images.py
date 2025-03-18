import requests
from bs4 import BeautifulSoup
import subprocess
import time

root_path = '/home/gcao/tmp/pics'
site = "https://chedongxi.com/p/337204.html"

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

cnt = 0
for img in img_tags:
    print("Currently downloaded: {}".format(img['src']))
    time.sleep(2)
    command = "cd "+ root_path +"; " +  "curl -o " + str(cnt).zfill(3) + '.jpg ' + img['src']
    cnt = cnt + 1
    subprocess.call(command, shell=True)
