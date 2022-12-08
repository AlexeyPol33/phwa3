import re
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def get_html (url):
    result = requests.get(url=url,headers=get_headers()).text
    return result

def get_vacancys(html):
    soup = BeautifulSoup(html,features='html.parser')
    vacancys = soup.find(id="a11y-main-content").findAll('div',attrs={'data-qa':"vacancy-serp__vacancy vacancy-serp__vacancy_premium"})
    return vacancys
    
def desired_tags(text,pattern_):
    pattern = re.compile(pattern_)
    return not(pattern.search(str(text)) == None)

def get_pattern(text,pattern):
    pattern = re.compile(pattern)
    return pattern.findall(text)

def get_data (soup):
    ref = soup.find(class_="serp-item__title",href=True)
    paycheck =  '-'.join(get_pattern(str(soup.find('span',class_="bloko-header-section-3")),r'(\d+\s*\d+)'))
    company = ''.join(get_pattern(str(soup.find('a',class_="bloko-link bloko-link_kind-tertiary")), r'>(.+)<'))
    city = ''.join(get_pattern(str(soup.find('div',attrs={'data-qa':'vacancy-serp__vacancy-address'})),r'Москва|Санкт-Петербург'))
    return {'ссылка':str(ref['href']),'вилка зп':str(paycheck),'название компании':str(company),'город':str(city)}

def get_sorted_vacancys_list(vacancys,pattern_):
    sorted_vacancy = []
    for i in vacancys:
        if desired_tags(i,pattern_):
            sorted_vacancy.append(i)
    return sorted_vacancy

def to_json(dict):
    with open('test.json','w',encoding='utf-8') as f:
        json.dump(dict,f,ensure_ascii=False)

def currency_check(vacancy,currency):
    soup = vacancy.find('span',attrs={'data-qa':"vacancy-serp__vacancy-compensation"} )
    result = str(soup)[-10:-7]
    return result == currency

def get_sorted_vacancys_list_currency(vacancys,currency):
    sorted_vacancy = []
    for i in vacancys:
        if currency_check(i,currency):
            sorted_vacancy.append(i)
    return sorted_vacancy

if __name__ == '__main__':
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    skill_tags = r'[d,D]jango|[F,f]lask'
    USD_tag = 'USD'
    vac = []
    for i in get_sorted_vacancys_list(get_vacancys(get_html(url)),skill_tags):
        vac.append(get_data(i))
    for i in get_sorted_vacancys_list_currency(get_vacancys(get_html(url)),USD_tag):
        print(i)
        vac.append(get_data(i))
    to_json(str(vac))
    print(str(vac))
