import telebot
from telebot import types
from database_connect import database_connect
from src.database_connect.util import utils



token = "6020285970:AAFocXdquKUhduTBCekTmcNp1xHBDvmFljY"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/help")
    keyboard.row("Расписание", "/mtuci")
    bot.send_message(message.chat.id, 'Привет! Хотите узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def start_message(message):
    week = database_connect.check_data_week(0)
    bot.send_message(message.chat.id, utils.typeOfWeek(week))

@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею: \n /week - узнать какая сейчас неделя \n /start - меню бота \n /mtuci - ссылка на сайт МТУСИ \n "расписание" - расписание на выбранный день')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда - https://mtuci.ru/')
    elif message.text.lower() == "расписание":
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.row("Сегодня", "Завтра")
        keyboard.row("Понедельник", "Вторник")
        keyboard.row("Среда", "Четверг")
        keyboard.row("Пятница", "Суббота")
        keyboard.row("На эту неделю", "На след. неделю")
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=keyboard)
    elif message.text.lower() == "сегодня":
        day = database_connect.check_data(0)
        arrTimeTable = database_connect.timeTableOfDay(0)
        bot.send_message(message.chat.id, str(day) + utils.create_timetable(arrTimeTable))
    elif message.text.lower() == "завтра":
        day = database_connect.check_data(1)
        arrTimeTable = database_connect.timeTableOfDay(1)
        bot.send_message(message.chat.id, str(day) + utils.create_timetable(arrTimeTable))
    elif message.text.lower() == "понедельник":
        sendDayTimeTable(bot, message, 1)
    elif message.text.lower() == "вторник":
        sendDayTimeTable(bot, message, 2)
    elif message.text.lower() == "среда":
        sendDayTimeTable(bot, message, 3)
    elif message.text.lower() == "четверг":
        sendDayTimeTable(bot, message, 4)
    elif message.text.lower() == "пятница":
        sendDayTimeTable(bot, message, 5)
    elif message.text.lower() == "суббота":
        sendDayTimeTable(bot, message, 6)
    elif message.text.lower() == "на эту неделю":
        sendWeekTimeTable(bot, message, 0)
    elif message.text.lower() == "на след. неделю":
        sendWeekTimeTable(bot, message, 1)
    else:
        print(message.text)
        bot.send_message(message.chat.id, 'Я вас не понимаю( \nВоспользуйтесь командой /help')

def sendDayTimeTable(bot, message, numbOfDay):
    day = utils.dowTransform(numbOfDay)
    arrTimeTable = database_connect.timeTableOfDayWeek(numbOfDay)
    text = utils.create_timetable(arrTimeTable)
    bot.send_message(message.chat.id, day + text)


def sendWeekTimeTable(bot, message, shift):
    arrTimeTable = database_connect.timeTableOfWeek(shift)
    text = utils.create_timetable_of_week(arrTimeTable)
    bot.send_message(message.chat.id, text)


bot.infinity_polling()