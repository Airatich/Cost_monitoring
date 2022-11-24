# -*- coding: utf -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import bs4
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.service import Service
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from options import user_agent,thickness_prod4,path_to_project,cities_start
from tqdm.auto import tqdm
import time
from datetime import datetime
import random



url = "http://23met.ru/"
options = webdriver.ChromeOptions()
# options.add_argument('--start-maximized')
options.headless=True
options.add_argument("window-size=1800x900")
options.add_argument('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')


s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

now = datetime.now()

def prod_4(city_ru):  # Сбор данных по продукту Лист/рулон окраш.
    time.sleep(2)
    prod4="Лист/рулон окраш."
    driver.find_element(By.XPATH,f"//a[text()='{prod4}']").click()  ### Лист/рулон окраш.
    time.sleep(2)
    selected_prod1 =thickness_prod4
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
        data["Продукт"] = prod4
        data["Толщина"] = i
        file = pd.concat([file, data])
    file = file.drop(columns='Поставщик.1', axis=1)
    time.sleep(2)
    return file



def main_prod_4():
    driver.get(url)
    cities = cities_start
    start_time = time.time()
    combined = pd.DataFrame()
    for i in tqdm(cities, desc=f"Лист/рулон окраш."):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,f"//a[text()='{i}' and @class='citychooser-city-link']"))).click()
        time.sleep(2)
        file = prod_4(i)
        combined = pd.concat([combined, file])

    combined.to_excel(rf"{path_to_project}/Excel/ЦМ_{now.strftime('%Y-%m-%d')}_04_Лист_рулон_пп.xlsx", index=False)
    print()
    print(f"Выгрузка Лист/рулон окраш. занала {int((time.time()-start_time)/60)} минут {int((time.time()-start_time)/60)} секунд")



