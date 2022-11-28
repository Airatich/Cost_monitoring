# -*- coding: utf -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# from new_options import user_agent, path_to_project
from tqdm.auto import tqdm
import time
from datetime import datetime

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
path_to_project = r"C:\Users\ADMIN\OneDrive\Документы\pyProjects\Cost_monitoring"

url = "http://23met.ru/"
options = webdriver.ChromeOptions()
# options.add_argument('--start-maximized')
options.headless = True
options.add_argument("window-size=1800x900")
options.add_argument(user_agent)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)
now = datetime.now()


def prod(name_prod, city_ru, thinkness_prod):  # Сбор данных по продукту
    prod = name_prod
    driver.find_element(By.XPATH, f"//a[text()='{prod}']").click()
    selected_prod = thinkness_prod
    file = pd.DataFrame()
    for i in selected_prod:
        time.sleep(3)
        driver.find_element(By.XPATH, f"//div/a[text()='{str(i)}']").click()
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table = soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data["Дата выгрузки данных"] = now.strftime("%d.%m.%Y")
        data['Город'] = city_ru
        data["Продукт"] = prod
        data["Толщина"] = i
        file = pd.concat([file, data])
    file = file.drop(columns='Поставщик.1', axis=1)
    time.sleep(2)
    return file


def main_prod(name_prod, thinkness_prod, cities,count):
    driver.get(url)
    start_time = time.time()
    combined = pd.DataFrame()

    for city in tqdm(cities, desc=f"Выгрузка {name_prod}"):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//a[text()='{city}']").click()
        time.sleep(2)
        file = prod(name_prod, city, thinkness_prod)
        combined = pd.concat([combined, file])



    combined.to_excel(rf"{path_to_project}\Excel\ЦМ_{now.strftime('%Y-%m-%d')}_{count}.xlsx", index=False)

    print()
    print(
        f"Выгрузка Лист_рулон_гк заняла {int((time.time() - start_time) / 60)} минут {int((time.time() - start_time) / 60)} секунд")
