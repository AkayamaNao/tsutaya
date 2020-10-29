# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import datetime

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# driver_path = 'chromedriver.exe'
# driver = webdriver.Chrome(executable_path=driver_path)

token_private = 'LNRxo0CLxzUteJNndzwhrQwS5LLEFtIubtM2QRi46A2'
token_000 = 'CDE9b5U3qVBNqnRhpH9q8PhbBiLCO7epp1eFdExk5dV'

url_list = [
    {'title': 'かぐや様は告らせたい8', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103361867.html?storeId=7630'},
    {'title': 'かぐや様は告らせたい9', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103390533.html?storeId=7630'},
    {'title': 'かぐや様は告らせたい10', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103407857.html?storeId=7630'},
    {'title': 'かぐや様は告らせたい11', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103437478.html?storeId=7630'},
    {'title': 'かぐや様は告らせたい18', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103616950.html?storeId=7630'},
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


# def main():
#     message_list = []
#     for url_dict in url_list:
#         state, message = get_zaiko_info(url_dict['url'])
#         message_list.append(url_dict["title"] + '\n' + message)
#         if state == 1:
#             headers = {"Authorization": "Bearer " + token_000}
#             payload = {"message": '\n' + url_dict["title"] + '\n' + message}
#             requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
#
#     driver.quit()  # ブラウザを閉じる
#     message = '\n' + '\n\n'.join(message_list)
#
#     headers = {"Authorization": "Bearer " + token_private}
#     payload = {"message": message}
#     requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
#
#     # with open('last_message.txt', 'r', encoding='utf-8') as f:
#     #     last_message = f.read()
#     #
#     # if message != last_message:
#     #     headers = {"Authorization": "Bearer " + token_private}
#     #     payload = {"message": message}
#     #     requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
#     #
#     #     with open('last_message.txt', 'w', encoding='utf-8') as f:
#     #         f.write(message)


def main():
    today=datetime.datetime.now().strftime('%Y%m%d')
    url = f'https://hotel.travel.rakuten.co.jp/hotelinfo/plan/?f_no=84814&f_campaign=&f_flg=PLAN&f_kin=&f_kin2=&f_heya_su=1&f_hak=&f_tel=&f_tscm_flg=&f_p_no=&f_custom_code=&send=&f_clip_flg=&f_static=&f_service=&f_teikei=&f_camp_id=4246007&f_syu=1&f_hizuke={today}&f_otona_su=1&f_thick=1&TB_iframe=true&height=768&width=1024'
    for i in range(5):
        driver.get(url)
        driver.implicitly_wait(30)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            vacant = soup.find_all('span', class_='vacant')
            break
        except:
            continue

    if len(vacant) != 0:
        message=f'{len(vacant)} 日候補があります。\n{url}'
        headers = {"Authorization": "Bearer " + token_000}
        payload = {"message": message}
        requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)


if __name__ == '__main__':
    main()
