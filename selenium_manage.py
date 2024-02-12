import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import save_postanovy_data, search_attempts, get_until_not_vp_num


def perform_selenium_actions(vp_num_value, secret_num_value, driver: webdriver.Firefox):
    url = "https://asvpweb.minjust.gov.ua/#/search-debtors"
    vp_num = None
    while not vp_num:
        try:
            vp_num = get_until_not_vp_num(driver=driver, url=url)
        except:
            driver.refresh()
    if vp_num:
        print('waiting for visibility Секретний номер')
        secret_num = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[data-ng-model="vm.data.model.filterVPData.SecretNum"]'))
        )

        secret_num.clear()
        vp_num.clear()

        vp_num.send_keys(vp_num_value)
        secret_num.send_keys(secret_num_value)

        WebDriverWait(driver, 5).until(lambda driver: vp_num.get_attribute("value") != "")
        WebDriverWait(driver, 5).until(lambda driver: secret_num.get_attribute("value") != "")

        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='btn btn--color-info' and @data-ng-click='vm.events.searchSides()']"))
        )
        print('click Шукати')
        element.click()
        account_exist = search_attempts(driver, element)
        if account_exist:
            perelik_postanov_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Перелік постанов')]"))
            )
            perelik_postanov_btn.click()
            print('зберігаються файли')
            save_postanovy_data(driver, vp_num_value, secret_num_value)
            print('всі файли збережено')

        else:
            with open(os.path.abspath('Документи по ВП/error.txt'), 'a') as f:
                f.write(f"Сторінку з {vp_num_value} не завантажено\n")
            print(f'!!! АККАУНТ {vp_num_value} НЕ ЗНАЙДЕНО')
            print(f'!!! АККАУНТ {vp_num_value} НЕ ЗНАЙДЕНО')
    else:
        print('SITE DOES NOT RESPONSE')
