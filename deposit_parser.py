# py -m pip install selenium
# py -m pip install bs4
import os
import json
import pandas as pd

from datetime import datetime
from io import StringIO

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH_OUT = "OUT"

# =========================================================================================
def GetHTMLfromUrl(url: str, class_name_located: str) -> BeautifulSoup:
    # Налаштування браузера
    options = Options()
    options.add_argument("--headless")  # без відкриття вікна браузера
    service = Service()  # автоматично знайде ChromeDriver, якщо встановлений
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    # Очікуємо завантаження таблиці
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name_located))
    )
    # Отримуємо HTML
    html = driver.page_source
    driver.quit()
    # Підготувати HTML для парсингу
    return BeautifulSoup(html, "html.parser")

# =========================================================================================
def Oshadbank(bank_name: str, url: str, df: pd.DataFrame):
    # Отримати HTML для парсингу
    soup = GetHTMLfromUrl(url, "table-rates__table")
    # Обираємо таблицю "Процентні ставки"
    tables = soup.find_all("table", class_="table-rates__table")
    # Вибираємо першу таблицю (якщо вона містить дані)
    if tables:
        body = tables[0].find("tbody", class_="table-rates__table-body")
        # Перевірка результату
        if body:
            dt = datetime.now().date()
            rows = body.find_all("tr")
            for row in rows:
                # print(row.prettify())
                cells = row.find_all("td")
                term = cells[0].get_text(strip=True)
                # Витягуємо валюту з дужок
                start = term.find("(")
                end = term.find(")")
                curr = term[start+1:end] if start != -1 and end != -1 else None
                # Витягуємо термін до дужок
                term_clean = term[:start].strip() if start != -1 else term.strip()
                rate = cells[1].get_text(strip=True)
                new_row = {
                    'dt': dt,
                    'bank_name': bank_name,
                    'cur': curr,
                    'termin': term_clean,
                    'percent': rate,
                    'url': url
                }
                df.loc[len(df)] = new_row
        else:
            print("Тіло таблиці не знайдено.")
    else:
        print("Таблиці не знайдено.")

# =========================================================================================
def Sensbank(bank_name: str, url: str, df: pd.DataFrame):
    # Отримати HTML для парсингу
    soup = GetHTMLfromUrl(url, "deposit-list__items-item")
    # Обираємо таблицю "Процентні ставки"
    div_deposits = soup.find_all("div", class_="deposit-list__items-item")
    for deposit in div_deposits:
        flg_parser = False
        parameters = deposit.find_all("li", class_="deposit-card__list-item text--small")
        # Знайти ознаку депозиту - "виплата відсотків — у кінці терміну"
        for parameter in parameters:
            text = parameter.get_text(strip=True)
            if text == "виплата відсотків — у кінці терміну":
                flg_parser = True
            # Перевірка наявності слова "валюта"
            if "валюта" in text:
                # Витягуємо слово після "валюта —" або "валюта:"
                parts = text.split("—")  # або text.split(":") для іншого варіанту
                if len(parts) > 1:
                    curr = parts[1].strip()
                else:
                    print("У полі з валютою неочікуваний формат строки.")
        # Розпарсити депозит, якщо в нього "виплата відсотків — у кінці терміну"
        if flg_parser:
            dt = datetime.now().date()
            term_clean = deposit.find_all("div", class_="deposit-card__content text")[0].get_text(strip=True)
            rate = deposit.find_all("p", class_="deposit-card__interest-rate-value h5")[0].get_text(strip=True)
            new_row = {
                'dt': dt,
                'bank_name': bank_name,
                'cur': curr,
                'termin': term_clean,
                'percent': rate,
                'url': url
            }
            df.loc[len(df)] = new_row

# =========================================================================================
def RaiffeisenUAH(bank_name: str, url: str, df: pd.DataFrame):
    # Отримати HTML для парсингу
    soup = GetHTMLfromUrl(url, "container")
    # Обираємо таблицю "Процентні ставки"
    div_deposit = soup.find_all("div", class_="conditions__wrap js-collapse-wrap")[0]
    dls = div_deposit.find_all("dl")
    flgAdd = False
    flgNotPrematureWithdrawal = False
    curr = ""
    for dl in dls:
        dt_text = dl.find("dt").get_text(strip=True)
        dd_text = dl.find("dd").get_text(strip=True)
        match dt_text:
            case "Валюта вклад":
                curr = dd_text
            case "Поповнення":
                if dd_text == "Без поповнення":
                    flgAdd = True
            case "Дострокове зняття коштів":
                if dd_text == "Не передбачене":
                    flgNotPrematureWithdrawal = True
            case _:
                pass
    if flgAdd and flgNotPrematureWithdrawal:
        dt = datetime.now().date()
        tbl_interest_rate = soup.find_all("div", class_="main-title main-title_center")[0]
        # Знайти таблицю всередині div
        tbl = tbl_interest_rate.find("table")
        # Перетворити HTML-таблицю в DataFrame
        df_html = pd.read_html(StringIO(str(tbl)))[0]
        df_html = df_html.dropna(how="all")  # прибрати повністю порожні рядки
        df_html = df_html.loc[:, ~df_html.isna().all()]  # прибрати повністю порожні колонки
        # Транспонувати таблицю
        df_html = df_html.T.reset_index()
        # зробимо перший рядок заголовками
        df_html.columns = df_html.iloc[0]  
        df_html = df_html.drop(0).reset_index(drop=True)
        df_html = df_html.rename(columns={"Unnamed: 0": "Термін"})
        for idx, row in df_html.iterrows():
            term = row["Термін"]
            rate = row["Відкриття у відділенні:"]

            new_row = {
                'dt': dt,
                'bank_name': bank_name,
                'cur': curr,
                'termin': term,
                'percent': rate,
                'url': url
            }
            df.loc[len(df)] = new_row
    else:
        print(f"⚠️ Відсутні депозити у ГРН без докапіталізації і достроковим зняттям")

# =========================================================================================
def RaiffeisenUSD_EUR(bank_name: str, url: str, df: pd.DataFrame):
    # Отримати HTML для парсингу
    soup = GetHTMLfromUrl(url, "container")

# =========================================================================================
def run_script():
    path_name = os.path.dirname(__file__)
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    # -------------------------------------------------------------------------------------
    # Створити датафрейм для заповнення інформцією
    df_deposit = pd.DataFrame({
        'dt': pd.Series(dtype='datetime64[ns]'),      # дата
        'bank_name': pd.Series(dtype='string'),       # текст
        'cur': pd.Series(dtype='string'),             # текст
        'termin': pd.Series(dtype='string'),          # текст
        # 'percent': pd.Series(dtype='float'),          # число з плаваючою точкою
        'percent': pd.Series(dtype='string'),         # число з плаваючою точкою
        'url': pd.Series(dtype='string')              # текст
    })
    # -------------------------------------------------------------------------------------
    path_json = os.path.join(path_name, "config.json")
    if os.path.exists(path_json):
        # Відкриваємо файл config.json
        with open('config.json', 'r', encoding='utf-8') as f:
            banks = json.load(f)
        # Перебираємо елементи масиву
        for bank in banks:
            if not bank['valid_parse']:
                print(f"Банк: {bank['Bank']}")
                print(f" URL: {bank['Deposit_page_URL']}")
                print(f" MSG: ❓ На поточний момент сторінка не аналізується")
                print()
            else:
                print(f"Банк: {bank['Bank']}")
                print(f" URL: {bank['Deposit_page_URL']}")
                match bank['Bank']:
                    case "АТ \"Ощадбанк\"":
                        Oshadbank(bank['Bank'], bank['Deposit_page_URL'], df_deposit)
                        print(f" MSG: ✅ Інформацію додано в датафрейм")
                    case "АТ \"СЕНС БАНК\"":
                        Sensbank(bank['Bank'], bank['Deposit_page_URL'], df_deposit)
                        print(f" MSG: ✅ Інформацію додано в датафрейм")
                    case "АТ \"Райффайзен Банк\" - Вклад «Класичний Строковий» в гривні":
                        RaiffeisenUAH(bank['Bank'], bank['Deposit_page_URL'], df_deposit)
                        print(f" MSG: ✅ Інформацію додано в датафрейм")
                    case "АТ \"Райффайзен Банк\" - Вклад Класичний Строковий в доларах США, євро":
                        RaiffeisenUSD_EUR(bank['Bank'], bank['Deposit_page_URL'], df_deposit)
                    case _:
                        print(f" MSG: ⚠️  На поточний момент алгоритм для аналізу не готовий")
                print()
    # -------------------------------------------------------------------------------------
    if not os.path.exists(os.path.join(path_name, PATH_OUT)):
        os.makedirs(os.path.join(path_name, PATH_OUT))
    parh_xlsx = os.path.join(path_name, PATH_OUT, f"{dt}_deposit.xlsx")
    df_deposit.to_excel(parh_xlsx, index=False)
    # -------------------------------------------------------------------------------------
    return 1

# =========================================================================================
if __name__ == '__main__':
    run_script()
