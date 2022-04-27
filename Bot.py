import telebot
import requests
import json
from config import keys, token
from extension import ConversionException



bot = telebot.TeleBot(token)


@bot.message_handler(commands= ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Увидеть список всех доступных валют: /values '
    bot.reply_to(message, text)

@bot.message_handler(commands= ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types= ['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConversionException("Ошибка ввода параметров.")

    quote, base, amount = values #в сообщении передаем параметры (биткоин, доллар и тп, количество) и разделяем их методом split через пробел

    if quote == base:
        raise ConversionException ('f Невозможно конвертировать одинаковые валюты {base}.')


    quote_ticker, base_ticker = keys[quote], keys[base]
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = float (json.loads(r.content)[keys[base]])
    c = float (amount)
    text = f'{amount} {quote} в {base} = {total_base * c}'
    bot.send_message(message.chat.id, text)

bot.polling()