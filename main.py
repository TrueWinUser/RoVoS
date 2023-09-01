from bs4 import BeautifulSoup
import requests
import datetime
import json
import tkinter as tk
import time

def filter(s):
    s1 = ''
    for i in s:
        if i == ',':
            s1+='.'
            continue
        if 32 < ord(i) < 127:
            s1+=i
        
    return s1

def price_get(ticker):
    url = f'https://www.tinkoff.ru/invest/stocks/{ticker}/'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    price = soup.find('span', class_ = 'Money-module__money_p_VHJ').text
    print(price)
    return float(filter(price))

def create_report():
    #подгрузка файлов
    with open('D:\\code\\stock_report\\stocks.json') as f:
        info = json.load(f)

    tickers = open("D:\\code\\stock_report\\tickers.txt", "rt")
    tickers_list = (tickers.read().split())

    curr_date = str(datetime.datetime.now().date())+"_"+datetime.datetime.now().strftime("%H.%M.%S")
    print(curr_date)

    result = open(f"{curr_date}.txt", "w")

    #обработка и запись информации об акциях
    general_margin = 0
    for i in tickers_list:
        price = price_get(i)
        grow = (100*price)/info["start_prices"][i]-100
        margin = price*info["stocks_amount"][i]-info["start_prices"][i]*info["stocks_amount"][i]
        result.write(f"{str(i)} {str(price)} {str(grow)} % {str(margin)} rub\n")
        print(i, price, grow)
        general_margin += margin
    result.write(f"General margin: {general_margin} rub")
    result.close()

def add_stock():
    with open('D:\\code\\stock_report\\stocks.json') as f:
        info = json.load(f)
    
    tickers = open("D:\\code\\stock_report\\tickers.txt", "a")
    new_ticker = entr1.get()
    new_price = entr2.get()
    new_amunt = entr3.get()
    tickers.write(f" {new_ticker}")
    tickers.close()
    info["start_prices"][new_ticker] = int(new_price)
    info["stocks_amount"][new_ticker] = int(new_amunt)

    with open('D:\\code\\stock_report\\stocks.json', 'w') as f:
        json.dump(info, f)

def remove_stock():
    with open('D:\\code\\stock_report\\stocks.json') as f:
        info = json.load(f)
    
    tickers = open("D:\\code\\stock_report\\tickers.txt", "r")
    t = tickers.read().split()
    tickers.close()

    tickers = open("tickers.txt", "w")
    remove_ticker = entr4.get()
    t.remove(remove_ticker)
    for i in t:
        tickers.write(f"{i} ")

    info["start_prices"].pop(remove_ticker)
    info["stocks_amount"].pop(remove_ticker)
    with open('stocks.json', 'w') as f:
        json.dump(info, f)
    tickers.close()



#создание интерфейса
win = tk.Tk()
win.title("RoVoS")
win.geometry("500x200")

create_report_btn = tk.Button(win, text="Create report", command=create_report, width=20)
create_report_btn.grid(column=1, row=0)

add_stock_btn = tk.Button(win, text="Add ticker", command=add_stock, width=20)
add_stock_btn.grid(column=2, row=0)

lbl1 = tk.Label(win, text="Name of the ticker:", width=20)
lbl1.grid(column=2, row=1)
entr1 = tk.Entry(win, width=20)
entr1.grid(column=2, row=2) 
lbl2 = tk.Label(win, text="Purchase price:", width=20)
lbl2.grid(column=2, row=3)
entr2 = tk.Entry(win, width=20)
entr2.grid(column=2, row=4) 
lbl3 = tk.Label(win, text="Amount of shares:", width=20)
lbl3.grid(column=2, row=5)
entr3 = tk.Entry(win, width=20)
entr3.grid(column=2, row=6) 

remove_stock_btn = tk.Button(win, text="Remove ticker", command=remove_stock, width=20)
remove_stock_btn.grid(column=3, row=0)

lbl4 = tk.Label(win, text="Name of the ticker:", width=20)
lbl4.grid(column=3, row=1)
entr4 = tk.Entry(win, width=20)
entr4.grid(column=3, row=2)

win.mainloop()




    
