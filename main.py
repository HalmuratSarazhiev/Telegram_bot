import csv
import requests
from bs4 import BeautifulSoup as bs
from mytoken import token
from telebot import types
import telebot 

bot = telebot.TeleBot(token)

inline_keyboard = types.InlineKeyboardMarkup()
btn = types.InlineKeyboardButton('QUIT', callback_data='exit_')
inline_keyboard.add(btn)

@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['start'])
def start_message(message):
    adress = 'https://kaktus.media/?lable=8&date=2022-05-03&order=time'
    listt=main(adress)
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Начинаю парсить новостной потрал Kaktus.kg', reply_markup=inline_keyboard)
        for value in listt[0:20]:
            bot.send_message(message.chat.id, f'ID:{value[0]}, {value[1]["news"]}')
    else:
        number = int(message.text)
        for new in listt:
            if new[0] == number:
                news = new[1]["news"]
                href = new[1]["href"]
                r_in = requests.get(href)
                d_soup = bs(r_in.text, "lxml")
                news_description = d_soup.find("div", class_="BbCode").find_all("p")
                update_new = [i.text for i in news_description]
                new_desc = "".join(update_new)
                bot.send_message(message.chat.id, f"{news}.\n\n{new_desc}")
                
@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    bot.send_message(c.message.chat.id, 'До свидания!') 

def get_html(url):
    resp = requests.get(url)
    return resp.text

def get_content(html):
    list_ = []
    soup = bs(html, "lxml")
    all_news = soup.find_all('div', class_ ='Tag--article')
    for i in all_news:
        news = i.find('a', class_ = 'ArticleItem--name').text.strip()
        href = i.find('a', class_ = 'ArticleItem--name').get("href")
        list_.append({"news":news, "href":href})
    a = list(enumerate(list_, 1))
    return a

def main(url):
    html = get_html(url)
    a=get_content(html)
    return a

bot.polling()