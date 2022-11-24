# -*- coding: utf -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bs4
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.service import Service
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from options import user_agent,thickness_prod3
from tqdm.auto import tqdm
import time
url = "http://23met.ru/"
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument(user_agent)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)




def prod_3(city):  # Сбор данных по продукту Лист/рулон оцинк.
    time.sleep(3)
    prod3="Лист/рулон оцинк."
    driver.find_element(By.XPATH,f"//a[text()='{prod3}']").click()  ### Лист/рулон оцинк.
    # 0, 4
    # 0, 5
    # 0, 55
    # 0, 7
    # 1
    time.sleep(2)
    selected_prod1 =thickness_prod3

    for i in selected_prod1:
        time.sleep(3)

        driver.find_element(By.XPATH, f"//div/a[text()='{str(i)}']").click()
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table = soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data.to_excel(
            rf'C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\{city}\Лист_рулон_оцинк\prod3_thickness_{i}.xlsx',
            index=False)
    driver.find_element(By.XPATH, "/html/body").click()


def main_prod_3():
    driver.get(url)
    cities = {"Moscow": "Москва", 'Saint Petersburg': 'Санкт-Петербург', 'Yekaterinburg': 'Екатеринбург',
              'Nizhny Novgorod': 'Нижний Новгород', 'Novosibirsk': "Новосибирск", "Rostov-on-Don": "Ростов-на-Дону"}
    start_time = time.time()
    for i in tqdm(cities, desc=f"Выгрузка Лист/рулон оцинк."):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//a[text()='{cities[i]}']").click()
        time.sleep(2)
        prod_3(i)
    print(f"Выгрузка Лист/рулон оцинк. занала {time.time() - start_time} секунд")

# -*- coding: utf -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bs4
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.service import Service
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from options import user_agent,thickness_prod3,path_to_project,cities_start
from tqdm.auto import tqdm
import time
from datetime import datetime
import random


url = "http://23met.ru/"
options = webdriver.ChromeOptions()
# options.add_argument('--start-maximized')
options.headless=True
options.add_argument("window-size=1800x900")
num=random.randrange(9)
options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')


s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

now = datetime.now()


def prod_3(city_ru):  # Сбор данных по продукту Лист/рулон оцинк.
    time.sleep(3)
    prod3="Лист/рулон оцинк."
    driver.find_element(By.XPATH,f"//a[text()='{prod3}']").click()  ### Лист/рулон оцинк.
    time.sleep(2)
    selected_prod1 =thickness_prod3
    file = pd.DataFrame()
    for i in selected_prod1:
        time.sleep(3)
        driver.find_element(By.XPATH, f"//div/a[text()='{str(i)}']").click()
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table = soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data["Дата выгрузки данных"] = now.strftime("%d.%m.%Y")
        data['Город'] = city_ru
        data["Продукт"] = prod3
        data["Толщина"] = i
        file = pd.concat([file, data])
    file = file.drop(columns='Поставщик.1', axis=1)
    time.sleep(2)
    return file


def main_prod_3():
    driver.get(url)
    cities = cities_start
    start_time = time.time()
    combined = pd.DataFrame()
    for i in tqdm(cities, desc=f"Выгрузка Лист_рулон_оцинк"):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//a[text()='{i}']").click()
        time.sleep(2)
        file = prod_3(i)
        combined = pd.concat([combined, file])

    combined.to_excel(rf"{path_to_project}/Excel/ЦМ_{now.strftime('%Y-%m-%d')}_03_Лист_рулон_оц.xlsx",index=False)
    print()
    print(f"Выгрузка Лист_рулон_оцинк заняла {int((time.time()-start_time)/60)} минут {int((time.time()-start_time)/60)} секунд")

