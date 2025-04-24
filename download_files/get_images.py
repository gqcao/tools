import requests
from bs4 import BeautifulSoup
import subprocess
import time

root_path = '/home/gcao/tmp/pics'
url = ""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers = headers)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

cnt = 0
for img in img_tags:
    if 'src' in img.attrs:
        key = 'src'
    elif 'data-src' in img.attrs:
        key = 'data-src'
    else:
        continue
    print("Currently downloaded: {}".format(img[key]))
    time.sleep(2)
    command = "cd "+ root_path +"; " +  "curl -o " + str(cnt).zfill(3) + '.jpg ' + img[key]
    cnt = cnt + 1
    subprocess.call(command, shell=True)
