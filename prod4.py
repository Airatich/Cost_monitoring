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
from options import user_agent,thickness_prod4
from tqdm.auto import tqdm
import time
url = "http://23met.ru/"
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--start-maximized')
options.add_argument(user_agent)

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)


def prod_4(city):  # Сбор данных по продукту Лист/рулон окраш.
    time.sleep(2)
    prod4="Лист/рулон окраш."
    driver.find_element(By.XPATH,f"//a[text()='{prod4}']").click()  ### Лист/рулон окраш.
    time.sleep(2)
    # 0, 4
    # 0, 45
    # 0, 5
    # 0, 55
    # 0, 7
    # 1

    selected_prod1 =thickness_prod4

    for i in selected_prod1:
        time.sleep(3)

        driver.find_element(By.XPATH, f"//div/a[text()='{str(i)}']").click()
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, "lxml")
        table = soup.select_one(".tablesorter")
        data = pd.read_html(str(table))
        data = data[0]
        data.to_excel(
            rf'C:\Users\Админ\Documents\PyProjects\Cost_monitoring\chromedriver\{city}\Лист_рулон_окраш\prod3_thickness_{i}.xlsx',
            index=False)
    driver.find_element(By.XPATH, "/html/body").click()



def main_prod_4():
    driver.get(url)
    cities = {"Moscow": "Москва", 'Saint Petersburg': 'Санкт-Петербург', 'Yekaterinburg': 'Екатеринбург',
              'Nizhny Novgorod': 'Нижний Новгород', 'Novosibirsk': "Новосибирск", "Rostov-on-Don": "Ростов-на-Дону"}
    start_time = time.time()
    for i in tqdm(cities, desc=f"Лист/рулон окраш."):
        driver.find_element(By.XPATH, f"//div[text()='Изменить/выбрать несколько']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[text()='Сбросить все']").click()
        time.sleep(2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                    f"//a[text()='{cities[i]}' and @class='citychooser-city-link']"))).click()
        time.sleep(2)
        prod_4(i)
    print(f"Выгрузка Лист/рулон окраш. занала {time.time() - start_time} секунд")

