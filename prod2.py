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
from options import user_agent,thickness_prod2
from tqdm.auto import tqdm
import time
url = "http://23met.ru/"
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument(user_agent)

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)



def prod_2(city): # Сбор данных по продукту Лист/рулон х/к
    time.sleep(2)
    prod2="Лист/рулон х/к"
    driver.find_element(By.XPATH,f"//a[text()='{prod2}']").click() ### Лист/рулон х/к
    # 0,5
    # 0,7
    # 0,8
    # 1
    # 1,2
    # 1,5
    # 2
    time.sleep(2)
    selected_prod1=thickness_prod2
    for i in selected_prod1:
        time.sleep(3)
        driver.find_element(By.XPATH,f"//a[text()='{str(i)}']").click()
        page_source=driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table=soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data.to_excel(rf'C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\{city}\Лист_рулон_хк\prod2_thickness_{i}.xlsx', index=False)



def main_prod_2():
    driver.get(url)
    cities = {"Moscow": "Москва", 'Saint Petersburg': 'Санкт-Петербург', 'Yekaterinburg': 'Екатеринбург',
              'Nizhny Novgorod': 'Нижний Новгород', 'Novosibirsk': "Новосибирск", "Rostov-on-Don": "Ростов-на-Дону"}
    start_time = time.time()
    for i in tqdm(cities, desc=f"Выгрузка Лист/рулон х/к"):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//a[text()='{cities[i]}']").click()
        time.sleep(2)
        prod_2(i)
    print(f"Выгрузка Лист/рулон х/к занала {time.time() - start_time} секунд")

