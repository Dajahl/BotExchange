import telebot

from config import cur_list, TOKEN
from extensions import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])

def greet(message: telebot.types.Message):
    text = f"Здравствуйте, {message.chat.username}!\nЧтобы начать работу с конвертером валют, введите запрос через пробел:" \
           f"\n" \
           f"\n<имя валюты> <в какую валюту перевести> <сумма валюты>" \
           f"\n" \
           f"\nСписок доступных валют: /currency" \
           f"\n" \
           f"\nЕсть вопрросы? Жмиите /help"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def hlp(message: telebot.types.Message):
    text = "Для просмотра всего списка валют выберете: /currency \n пример ввода запроса: доллар евро 100"
    bot.reply_to(message, text)

@bot.message_handler(commands=['currency'])
def value(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in cur_list.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Слишком много параметров.")

        quote, base, amount = values
        total_base = CurrencyConverter.errors_check(quote, base, amount)

    except ConvertionException as f:
        bot.reply_to(message, f"Ошибка пользователя\n {f}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n {e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()