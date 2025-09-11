# py -m pip install selenium
# py -m pip install bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Налаштування браузера
options = Options()
options.add_argument("--headless")  # без відкриття вікна браузера
service = Service()  # автоматично знайде ChromeDriver, якщо встановлений

URL_OSHADBANK = "https://www.oschadbank.ua/deposit/my-deposit"
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL_OSHADBANK)

# Очікуємо завантаження таблиці
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "table-rates__table"))
)

# Отримуємо HTML
html = driver.page_source
driver.quit()

print(f"URL →  {URL_OSHADBANK}")
# Парсимо таблицю
soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table", class_="table-rates__table")

for table in tables:
    rows = table.find_all("tr")[1:]  # пропускаємо заголовок

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            term = cells[0].get_text(strip=True)
            rate_UAH = cells[1].get_text(strip=True)
            rate_USD = cells[2].get_text(strip=True)
            rate_EUR = cells[2].get_text(strip=True)
            print(f"  Строк: {term} → Ставка: UAH {rate_UAH} ... USD {rate_USD} ... EUR {rate_EUR}")
