# -- coding: utf-8 --
import requests
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent


def gethtml(url):
    headers = {
        "user-agent": 'Mozilla/5.0',
    }
    r = requests.get(url, headers=headers, timeout=25)
    r.encoding = 'utf-8'
    return str(r.content)


def get_list_html(url, page):
    headers = {
        "user-agent": 'Mozilla/5.0',
    }
    kv = {
        "page": page
    }
    r = requests.get(url, headers=headers, params=kv, timeout=25)
    r.encoding = 'utf-8'
    return str(r.content)


def get_url(page_content):
    temp_list = []
    soup = BeautifulSoup(page_content, 'html5lib')
    url_div = soup.find('div', attrs={'id': 'questions', 'class': 'flush-left'})
    questions = url_div.find_all('div', attrs={'class': 'question-summary'})
    for i in questions:
        accept_tag = i.find('div', attrs={'class': 'status answered-accepted'})
        if accept_tag==None:
            continue
        url = i.find('a', attrs={'class': 'question-hyperlink'}).attrs['href']
        temp_list.append('https://stackoverflow.com'+url)
    return temp_list


def get_url_list(number):
    url_list = []
    page_number = int(number/50)+1
    for i in range(1, page_number):
        page_content = get_list_html(
            'https://stackoverflow.com/questions/tagged/android?tab=votes&pagesize=50',
            str(i)
        )
        url_list.extend(get_url(page_content))
        print('列表获取成功')
    return url_list


def get_QandA(url_list, path):
    docname = 1
    for i in url_list:
        try:
            soup = BeautifulSoup(gethtml(i), 'html5lib')

           #清除所有图片标签
            img_list = soup.find_all('img')
            for p in img_list:
                p.decompose()

            QandA = soup.find_all('div', attrs={'class': 'post-text'}, limit=2)
            dianzan = soup.find_all('div', attrs={
                'class': 'js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center'
            }, limit=2)
            Qpart = QandA[0].text
            Apart = QandA[1].text
            Qzan = dianzan[0].text
            Azan = dianzan[1].text

            #转义字符修正
            Apart = Apart.replace('\\r\\n', '\n')
            Apart = Apart.replace('\\n', '\n')
            Apart = Apart.replace(r'\'', '\'')
            Qpart = Qpart.replace('\\r\\n', '\n')
            Qpart = Qpart.replace('\\n', '\n')
            Qpart = Qpart.replace(r'\'', '\'')

            #去除Q或A内容前端的换行符
            Qpart = Qpart.lstrip()
            Apart = Apart.lstrip()

            #保存文件
            with open(path+str(docname)+'.txt', 'w', encoding='utf-8') as f:
                f.write(Qzan+'\n')
                f.write('Q:'+Qpart)
                f.write('\n')
                f.write('===============================================================================================\n')
                f.write(Azan+'\n')
                f.write('A:'+Apart)

            docname += 1
        except:
            print('获取失败')
            continue


url_list = get_url_list(13000)
path = ''
get_QandA(url_list, path)
