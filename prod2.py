# -*- coding: utf -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.service import Service
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from options import user_agent,thickness_prod2,path_to_project,cities_start
from tqdm.auto import tqdm
import time
from datetime import datetime
import random

url = "http://23met.ru/"
options = webdriver.ChromeOptions()
# options.add_argument('--start-maximized')
options.headless=True
options.add_argument("window-size=1800x900")
options.add_argument(user_agent)



s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

now = datetime.now()

def prod_2(city_ru): # Сбор данных по продукту Лист/рулон х/к
    time.sleep(2)
    prod2="Лист/рулон х/к"
    driver.find_element(By.XPATH,f"//a[text()='{prod2}']").click() ### Лист/рулон х/к
    time.sleep(2)
    selected_prod1=thickness_prod2
    file = pd.DataFrame()
    for i in selected_prod1:
        time.sleep(3)
        driver.find_element(By.XPATH,f"//a[text()='{str(i)}']").click()
        page_source=driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table=soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data["Дата выгрузки данных"] = now.strftime("%d.%m.%Y")
        data['Город']=city_ru
        data["Продукт"] = prod2
        data["Толщина"] = i
        file=pd.concat([file,data])
    file = file.drop(columns='Поставщик.1', axis=1)
    time.sleep(2)
    return file

def main_prod_2():
    driver.get(url)
    cities = cities_start
    start_time = time.time()
    combined = pd.DataFrame()
    for i in tqdm(cities, desc=f"Выгрузка Лист/рулон х/к"):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//a[text()='{i}']").click()
        time.sleep(2)
        file = prod_2(i)
        combined = pd.concat([combined, file])

    combined.to_excel(rf"{path_to_project}/Excel/ЦМ_{now.strftime('%Y-%m-%d')}_02_Лист_рулон_xк.xlsx", index=False)
    print()
    print(f"Выгрузка Лист_рулон_хк заняла {int((time.time()-start_time)/60)} минут {int((time.time()-start_time)/60)} секунд")

