from selenium import webdriver
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import accessibility_events.database as db

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options)


def main():
    db.EMailContent.delete().execute()

    browser.get("https://www.zuerichunbezahlbar.ch/events/")

    for _ in range(7):
        browser_events = browser.find_elements(By.CSS_SELECTOR, ".poster__title-span.poster__title-span-text")
        for event in browser_events:
            event.click()

            title = get_element(By.CSS_SELECTOR, ".reveal-modal.open .poster__title-span.poster__title-span-text").text
            time = get_element(By.CSS_SELECTOR, ".detailpost__date time").text
            info = get_element(By.CSS_SELECTOR, "div.detailpost__info").text
            address = get_element(By.CSS_SELECTOR, "address.detailpost__address").text
            description = get_element(By.CSS_SELECTOR, "div.detailpost__description").text
            link = get_element(By.CSS_SELECTOR, "a.detailpost__link").get_attribute("href")

            print(title)
            db.EMailContent.create(subject=uuid4(),
                                   content=f"title: {title}\ntime: {time}\n info: {info}\naddress: {address}\ndescription: {description}\nlink: {link}")

            get_element(By.CSS_SELECTOR, ".close-reveal-modal").click()

        get_element(By.CSS_SELECTOR, "span.step-links a").click()

    browser.quit()


def get_element(selector_type, selector: str):
    return WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((selector_type, selector)))


if __name__ == '__main__':
    main()
