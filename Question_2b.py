# packages needed are selenium, BeautifulSoup4, xlsxwriter, pandas
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import xlsxwriter

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

stocks = []
while stocks == []:
    service = ChromeService()
    driver = Chrome(service=service,options=options)
    driver.get('https://www.nseindia.com/market-data/live-equity-market')
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stocks = soup.find_all("a", class_="symbol-word-break")

index = 0
for stock in stocks:
    stocks[index] = stock.text
    index += 1

indivisual_HTML_unaltered = soup.find_all("tr", class_="")
indivisual_HTML = []
for index in range(0, len(indivisual_HTML_unaltered)):
    if index % 4 == 0:
        indivisual_HTML.append(indivisual_HTML_unaltered[index])
indivisual_HTML.pop(0)

all_info_dictionary = {}


def info_list(index):
    indivisual_info_list = indivisual_HTML[index].find_all("td", class_="text-right")
    index_2 = 0
    for value in indivisual_info_list:
        indivisual_info_list[index_2] = value.text
        index_2 += 1
    return indivisual_info_list

for index in range(0, 50):
    all_info_dictionary[stocks[index]] = info_list(index)
print(all_info_dictionary)


# Now showing the data in a database
df = pd.DataFrame()
for i in range(50):
    Stocks = stocks[i]
    open = all_info_dictionary[stocks[i]][0]
    high = all_info_dictionary[stocks[i]][1]
    low= all_info_dictionary[stocks[i]][2]
    prev_close= all_info_dictionary[stocks[i]][3]
    ltp= all_info_dictionary[stocks[i]][4]
    change= all_info_dictionary[stocks[i]][5]
    per_change= all_info_dictionary[stocks[i]][6]
    volume= all_info_dictionary[stocks[i]][7]
    value= all_info_dictionary[stocks[i]][8]
    high52= all_info_dictionary[stocks[i]][9]
    low52= all_info_dictionary[stocks[i]][10]

    df = df._append(
        pd.DataFrame({"STOCKS": Stocks, "OPEN": open, "HIGH": high, "LOW": low, "PREV. CLOSE": prev_close, "LTP": ltp, "CHANGE": change, "%CHANGE": per_change, "VOLUME": volume, "VALUE": value, "52W HIGH": high52, "52W LOW": low52},
                     index=[0]), ignore_index=True)
df.index += 1
df.index.name = "S.No."
print(df)

df.to_excel("NSE-NIFTY50.xlsx", engine="xlsxwriter")
