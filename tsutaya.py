from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

# driver_path = 'chromedriver.exe'

# グローバル変数
item_id = '005570850'
item_type = 'rental_cd'
prefecture_id = '13'
csv_save_dir = './csv/'
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(executable_path=driver_path)

token_private = 'LNRxo0CLxzUteJNndzwhrQwS5LLEFtIubtM2QRi46A2'
token_000 = 'CDE9b5U3qVBNqnRhpH9q8PhbBiLCO7epp1eFdExk5dV'

url_list = [
    {'title': 'かぐや様は告らせたい18', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103616950.html?storeId=7630'},
    {'title': 'かぐや様は告らせたい17', 'url': 'https://store-tsutaya.tsite.jp/item/rental_comic/103587429.html?storeId=7630'}
]


def get_zaiko_info(url):
    driver.get(url)
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    zaiko = soup.find('div', class_='state').find('span').string
    if '－' in zaiko:
        message = '取扱していません'
        state = -1
    else:
        load_date = soup.find('div', class_='stateDate').string
        if '○' in zaiko:
            message = f'在庫があります{load_date}'
            state = 1
        else:
            return_date = soup.find('div', class_='state').find('div').string
            message = f'現在在庫がありません{load_date} {return_date}'
            state = 0
    return state, message


def main():
    message_list = []
    for url_dict in url_list:
        state, message = get_zaiko_info(url_dict['url'])
        message_list.append(f'{url_dict["title"]}\n{message}')
        if state == 1:
            headers = {"Authorization": "Bearer " + token_000}
            payload = {"message": f'{url_dict["title"]}\n{message}'}
            requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)

    driver.quit()  # ブラウザを閉じる

    headers = {"Authorization": "Bearer " + token_private}
    payload = {"message": '\n\n'.join(message_list)}
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)


if __name__ == '__main__':
    main()
