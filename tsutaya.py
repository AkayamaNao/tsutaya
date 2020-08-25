# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# driver_path = 'chromedriver.exe'
# driver = webdriver.Chrome(executable_path=driver_path)

token_private = 'LNRxo0CLxzUteJNndzwhrQwS5LLEFtIubtM2QRi46A2'
token_000 = 'CDE9b5U3qVBNqnRhpH9q8PhbBiLCO7epp1eFdExk5dV'

url_list = [
    {'title': 'ようこそ実力至上主義の教室へ２', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103249727.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ３', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103276750.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ４', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103306934.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ５', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103349773.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ６', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103381645.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ７', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103463433.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ８', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103528200.html?storeId=7630'},
    {'title': 'ようこそ実力至上主義の教室へ９', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103593729.html?storeId=7630'},
]


def get_zaiko_info(url):
    for i in range(5):
        driver.get(url)
        driver.implicitly_wait(30)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            zaiko = soup.find('div', class_='state').find('span').string
            break
        except:
            continue
    if i == 4:
        return 0, '情報を取得できませんでした'
    if '－' in zaiko:
        message = '取扱していません'
        state = -1
    else:
        load_date = soup.find('div', class_='stateDate').string
        if '○' in zaiko:
            message = '在庫があります\n' + load_date
            state = 1
        else:
            return_date = soup.find('div', class_='state').find('div').string
            message = '現在在庫がありません\n' + load_date + '\n' + return_date
            state = 0
    return state, message


def main():
    message_list = []
    for url_dict in url_list:
        state, message = get_zaiko_info(url_dict['url'])
        message_list.append(url_dict["title"] + '\n' + message)
        if state == 1:
            headers = {"Authorization": "Bearer " + token_000}
            payload = {"message": '\n' + url_dict["title"] + '\n' + message}
            requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)

    driver.quit()  # ブラウザを閉じる
    message = '\n' + '\n\n'.join(message_list)

    headers = {"Authorization": "Bearer " + token_private}
    payload = {"message": message}
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)

    # with open('last_message.txt', 'r', encoding='utf-8') as f:
    #     last_message = f.read()
    #
    # if message != last_message:
    #     headers = {"Authorization": "Bearer " + token_private}
    #     payload = {"message": message}
    #     requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    #
    #     with open('last_message.txt', 'w', encoding='utf-8') as f:
    #         f.write(message)


if __name__ == '__main__':
    main()
