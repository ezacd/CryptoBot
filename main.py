import telebot
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введи команду боту в следующем формате:\n <имя валюты> ' \
           '<в какую валюту перевести>\n ' \
           '<количество валюты>.\n' \
           'Например: биткоин доллар 1\n' \
           'Увидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Нераспознанная команда')

        quote, base, amount = value

        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду \n{e}')
    else:
        res = f'Курс {amount} {quote}/{base} составляет {total_base}'
        bot.send_message(message.chat.id, res)


bot.polling(none_stop=True)
