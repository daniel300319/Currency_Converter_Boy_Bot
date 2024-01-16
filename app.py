import telebot
from config import TOKEN, exchanges
from extensions import APIException, Convertor

bot = telebot.TeleBot(TOKEN)

help_text = '''CurrencyСonverterBoy — конвертер валют.

Для начала работы, введите сообщение в следующем формате:
<Имя валюты> <Количество переводимой валюты> <В какую валюту перевести>
Например, если Вы хотите перевести 100 долларов в рубли, запрос должен выглядеть как "доллар 100 рубль".

Для просмотра доступных валют введите: /values'''
valid_input = '\nКорректный ввод: \n<Имя валюты> <Количество переводимой валюты> <В какую валюту перевести>'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}!\n\n{help_text}')

@bot.message_handler(commands=['help'])
def help(message):
        bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['values'])
def values(message):
    values_text = 'Доступные валюты:'
    for currency, value in exchanges.items():
        values_text = '\n'.join((values_text, f'{currency} {value[1]}',))
    bot.send_message(message.chat.id, values_text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.title().split()
        print(values)
        if len(values) > 3:
            raise APIException(f'Слишком много параметров! {valid_input}')
        if len(values) < 3:
            raise APIException(f'Вы ввели менее 3-х параметров! {valid_input}')

        curr1, amount, curr2 = values
        base = Convertor.get_price(curr1, amount, curr2)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        convert_text = f'{amount} {exchanges[curr1][0]} = {base * float(amount)} {exchanges[curr2][0]}'
        bot.send_message(message.chat.id, convert_text)


bot.polling(none_stop=True)





