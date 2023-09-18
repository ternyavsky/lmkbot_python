from bs4 import BeautifulSoup as bs
import requests
import time

url = 'http://lmk-lipetsk.ru/main_razdel/shedule/index.php'
res = requests.get(url)
soup = bs(res.content, 'html.parser')
def get_shedule():
    start = time.time()
    tags =soup.find_all('a', target='_blank')
    result = None
    name = None
    for i in tags:
        if '2023' in i.text:
            result = i['href']
            name = i.text
    print(result)

    sec_url = 'http://lmk-lipetsk.ru{}'.format(result)
    get_pdf = requests.get(sec_url)
    with open ('shedule.pdf', 'wb') as f:
        f.write(get_pdf.content)
    print(time.time() - start)
    return name

def get_color():
    tags = soup.find_all('h3')
    result = None
    for i in tags:

        if 'неделя' in i.text:
            result = i.text 
    return result

