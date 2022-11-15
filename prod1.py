# -*- coding: utf -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bs4
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from options import user_agent, thickness_prod1
from tqdm.auto import tqdm
import time

url = "http://23met.ru/"
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument(user_agent)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)


def prod_1(city):  # Сбор данных по продукту Лист/рулон г/к
    prod1 = "Лист/рулон г/к"
    driver.find_element(By.XPATH, f"//a[text()='{prod1}']").click()  ### Лист/рулон г/к
    # 4 6 8 10 12 16 18 20 28 32
    selected_prod1 = thickness_prod1
    for i in selected_prod1:
        time.sleep(3)
        driver.find_element(By.XPATH, f"//a[text()='{str(i)}']").click()
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table = soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data.to_excel(
            rf'C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\{city}\Лист_рулон_гк\prod1_thickness_{i}.xlsx',
            index=False)
        # print(f'prod1_thickness_{i}.xlsx -- ready')
    time.sleep(2)


def main_prod_1():
    driver.get(url)
    cities = {"Moscow": "Москва", 'Saint Petersburg': 'Санкт-Петербург', 'Yekaterinburg': 'Екатеринбург',
              'Nizhny Novgorod': 'Нижний Новгород', 'Novosibirsk': "Новосибирск", "Rostov-on-Don": "Ростов-на-Дону"}
    start_time = time.time()
    for i in tqdm(cities, desc=f"Выгрузка Лист_рулон_гк"):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//a[text()='{cities[i]}']").click()
        time.sleep(2)
        prod_1(i)
    print(f"Выгрузка Лист_рулон_гк занала {time.time() - start_time} секунд")



