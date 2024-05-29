import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from paths import cards, input_field, cookies, count, next_page


URL: str = "https://2gis.ru"


def make_list_cities() -> list:
    url: str = (
        "https://catalog.api.2gis.com/2.0/region/list?fields=items.country_code,items.code&key=028765df-ee43-429d-b281-099f973e3e87"
    )
    response = requests.get(url=url).json()["result"]["items"]
    cities: list = [
        (city["name"], city["code"])
        for city in response
        if city["country_code"] == "ru"
    ]
    return cities


def open_page(driver: webdriver, url: str) -> webdriver:
    driver.get(url=url)
    return driver


def click_on_cookies(driver: webdriver) -> webdriver:
    try:
        driver.find_element(by=By.XPATH, value=cookies).click()
        return driver
    except NoSuchElementException:
        return driver


def find_quantity(wait: WebDriverWait) -> int:
    try:
        quantity = wait.until(EC.presence_of_element_located((By.XPATH, count)))
        quantity = int(quantity.text)
        return quantity
    except TimeoutException:
        return 0


def main():
    cities = make_list_cities()
    category: str = "строительный магазин"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)
    driver.maximize_window()
    for counter, city in enumerate(cities, start=1):
        link: str = f"{URL}/{city[1]}/search/{category}"
        open_page(driver=driver, url=link)
        if counter == 1:
            click_on_cookies(driver=driver)
        quantity = find_quantity(wait=wait)
        pages = round(quantity / 12 + 0.5)
        for page in range(1, pages + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(EC.presence_of_element_located((By.XPATH, next_page))).click()
    driver.quit()


if __name__ == "__main__":
    main()
