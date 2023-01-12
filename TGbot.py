from telebot import TeleBot
import sqlite3
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime
from pathlib import Path
import os



TOKEN_BOT = '5729656929:AAHSxglQG-DeuNCWOlENB91H8usjvoAzkps'
bot = TeleBot(TOKEN_BOT)
bot.set_webhook()

connection = sqlite3.connect("dbhack.db")
cursor = connection.cursor()

# cursor.execute("CREATE TABLE Hack (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `area` TEXT, `year` INTEGER, `season` TEXT, `month` TEXT, `description` TEXT, `feedback` TEXT, `mark` INTEGER, `date` TEXT, `userid` INTEGER, `src` TEXT);")
# connection.commit()

# cursor.execute("CREATE TABLE Moders (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `moder_id` INTEGER);")
# connection.commit()

# Запрос в дб
def main(sql):
    try:
        # Подключение к базе данных
        connection = sqlite3.connect("dbhack.db")
        cursor = connection.cursor()

        cursor.execute(sql)
        result = cursor.fetchall()


        connection.commit()
        
        # Не забываем закрыть соединение
        connection.close()
        return result

    except Exception as e:
        print(f'+++ {e}')

main(f"INSERT INTO Moders (`moder_id`) VALUES ('806902493')")
# main(f"INSERT INTO Moders (`moder_id`) VALUES ('735054458')")
# main(f"INSERT INTO Moders (`moder_id`) VALUES ('998781783')")



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '*Здравствуй, хочешь предложить свою достопримечательность/место в Ульяновске? Вперёд!\n\nУльяновск* — прекрасный город, который привлекает туристов историческими и архитектурными памятниками, а также природными достопримечательностями. Он известен не только как родина отца Октябрьской революции В. И. Ленина, но и как место, где появились на свет выдающиеся русские писатели Н. М. Карамзин и И. А. Гончаров.', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")


@bot.message_handler(commands=['new'])
def get_area(message):

    kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btns = [KeyboardButton("Засвияжский"), KeyboardButton("Заволжский"), KeyboardButton("Железнодорожный район"), KeyboardButton("Ленинский район")]
    for btn in btns:     
        kb.add(btn)
        
    bot.send_message(message.chat.id, '1️⃣ *В каком районе находится достопримечательность/место?*', reply_markup=kb, parse_mode="Markdown")

    bot.register_next_step_handler(message, get_year)


def get_year(message):
    ms_area = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btns = [KeyboardButton("2022"), KeyboardButton("2021"), KeyboardButton("2020"), KeyboardButton("2019"), KeyboardButton("2018")]
    for btn in btns:     
        kb.add(btn)
    bot.send_message(message.chat.id, '2️⃣ *В каком году Вы посещали достопримечательность/место?*', reply_markup=kb, parse_mode="Markdown")
    bot.register_next_step_handler(message, get_season, ms_area)


def get_season(message, ms_area):
    ms_year = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btns = [KeyboardButton("Зима"), KeyboardButton("Весна"), KeyboardButton("Лето"), KeyboardButton("Осень")]
    for btn in btns:     
        kb.add(btn)
    bot.send_message(message.chat.id, '3️⃣ *В каком сезоне Вы посещали её/его?*', reply_markup=kb, parse_mode="Markdown")
    bot.register_next_step_handler(message, get_month, ms_area, ms_year)
    

def get_month(message, ms_area, ms_year):
    ms_sesson = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if ms_sesson == "Зима":
        btns = [KeyboardButton("Декабрь"), KeyboardButton("Январь"), KeyboardButton("Февраль")]
        for btn in btns:     
            kb.add(btn)
    elif ms_sesson == "Весна":
        btns = [KeyboardButton("Март"), KeyboardButton("Апрель"), KeyboardButton("Май")]
        for btn in btns:     
            kb.add(btn)
    elif ms_sesson == "Лето":
        btns = [KeyboardButton("Июнь"), KeyboardButton("Июль"), KeyboardButton("Август")]
        for btn in btns:     
            kb.add(btn)
    elif ms_sesson == "Осень":
        btns = [KeyboardButton("Сентябрь"), KeyboardButton("Октябрь"), KeyboardButton("Ноябрь")]
        for btn in btns:     
            kb.add(btn)

    bot.send_message(message.chat.id, '4️⃣ *В каком месяце Вы посещали достопримечательность/место?*', reply_markup=kb, parse_mode="Markdown")
    bot.register_next_step_handler(message, get_description, ms_area, ms_year, ms_sesson)


def get_description(message, ms_area, ms_year, ms_sesson):
    ms_month = message.text
    bot.send_message(message.chat.id, '5️⃣ *Опишите данную достопримечательность/место: *', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
    bot.register_next_step_handler(message, get_feedback, ms_area, ms_year, ms_sesson, ms_month)


def get_feedback(message, ms_area, ms_year, ms_sesson, ms_month):
    ms_description = message.text
    bot.send_message(message.chat.id, '6️⃣ *Напишите отзыв о ней/нём: *', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
    bot.register_next_step_handler(message, get_mark, ms_area, ms_year, ms_sesson, ms_month, ms_description)


def get_mark(message, ms_area, ms_year, ms_sesson, ms_month, ms_description):
    ms_feedback = message.text
    bot.send_message(message.chat.id, '7️⃣ *Ваша субъективная оценка *\n_От 1 до 10:_', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
    bot.register_next_step_handler(message, choise_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback)


def choise_photo(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback):
    ms_mark = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btns = [KeyboardButton("Да"), KeyboardButton("Нет")]
    for btn in btns:     
        kb.add(btn) 
    bot.send_message(message.chat.id, '8️⃣ *У вас есть фотография этой достопримечательности/места?*', reply_markup=kb, parse_mode="Markdown")
    bot.register_next_step_handler(message, choise_moder, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark)


def choise_moder(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark):
    if message.text == "Да":
        bot.register_next_step_handler(message, get_photo, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark)
        bot.send_message(message.chat.id, '📸*Отправьте фотографию: *', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
    elif message.text == "Нет":
        kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btns = [KeyboardButton("Да"), KeyboardButton("Нет")]
        for btn in btns:     
            kb.add(btn) 
        bot.send_message(message.chat.id, '📥*Данные получены, отправить на модерацию?*', reply_markup=kb, parse_mode="Markdown")
        bot.register_next_step_handler(message, insert_and_send, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark)


@bot.message_handler(content_types=['photo', 'document'])
def get_photo(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark):
    try:
        kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        btns = [KeyboardButton("Да"), KeyboardButton("Нет")]
        for btn in btns:     
            kb.add(btn)

        # Создаем папочку, если ее нет
        Path(f'files/{message.chat.id}/').mkdir(parents = True, exist_ok = True)

        # Инфа о фото
        if bot.get_file(message.photo[len(message.photo) - 1].file_id):               # доработать, чтобы когда присылали НЕ сжатое изображение - обрабатывать это
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'files/{message.chat.id}/{datetime.datetime.now().strftime("%Y%m%d_%H%M")}{file_info.file_path.replace("photos/", "")}'
            print(f'---{src}')
            bot.send_message(message.chat.id, '📥*Данные получены, отправить на модерацию?*', reply_markup=kb, parse_mode="Markdown")
            # Сохраняем файл
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.register_next_step_handler(message, insert_and_send, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, src)

        else:
            bot.send_message(message.chat.id, '*Нужно отправлять сжатое изображение. Попробуйте снова*', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
            get_area(message)

    except Exception as e:
        print(print(f'!!!{e}'))



bot.message_handler(content_types=["text"])
def insert_and_send(message, ms_area, ms_year, ms_sesson, ms_month, ms_description, ms_feedback, ms_mark, src = False):

    if message.text == "Да":
        bot.send_message(message.chat.id, '🆗 *Спасибо за то, что внесли данные. Мы уведовим вас, если данные пройдут модерацию*', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")  
        date = datetime.datetime.now().strftime("%Y%m%d_%H%M")

        user_id = message.from_user.id

        if src:
            print(f'###{src}')
            main(f"INSERT INTO Hack (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `date`, `userid`, `src`) VALUES ('{ms_area}', '{ms_year}', '{ms_sesson}', '{ms_month}', '{ms_description}', '{ms_feedback}', '{ms_mark}', '{date}', '{user_id}', '{src}')")
            print(main(f"SELECT id FROM Hack WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND userid='{user_id}' AND `src`='{src}';"))
            dates_id = main(f"SELECT id FROM Hack WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND userid='{user_id}' AND `src`='{src}';")
            bot.send_photo(806902493, open(src,'rb'), caption=f"*Район:* {ms_area}\n\n*Год:* {ms_year}\n\n*Сезон:* {ms_sesson}\n\n*Месяц:* {ms_month}\n\n*Описание:* {ms_description}\n\n*Отзыв:* {ms_feedback}\n\n*Субъективная оценка пользователя:* {ms_mark}", reply_markup =  gen_markup(dates_id), parse_mode="Markdown")
            print(dates_id)
        else:
            main(f"INSERT INTO Hack (`area`, `year`, `season`, `month`, `description`, `feedback`, `mark`, `date`, `userid`, `src`) VALUES ('{ms_area}', '{ms_year}', '{ms_sesson}', '{ms_month}', '{ms_description}', '{ms_feedback}', '{ms_mark}', '{date}', '{user_id}', '0')")
            dates_id = main(f"SELECT id FROM Hack WHERE area='{ms_area}' AND year='{ms_year}' AND season='{ms_sesson}' AND month='{ms_month}' AND description='{ms_description}' AND feedback='{ms_feedback}' AND mark='{ms_mark}' AND userid='{user_id}' AND src='0';")
            bot.send_message(806902493, f"*Район:* {ms_area}\n\n*Год:* {ms_year}\n\n*Сезон:* {ms_sesson}\n\n*Месяц:* {ms_month}\n\n*Описание:* {ms_description}\n\n*Отзыв:* {ms_feedback}\n\n*Субъективная оценка пользователя:* {ms_mark}", reply_markup =  gen_markup(dates_id), parse_mode="Markdown")
            print(dates_id)
    else:
        bot.send_message(message.chat.id, '🔜 *Будем ждать вас снова!*', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
        start(message)
    

# Кнопки для модератора
def gen_markup(dates_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("✅Запостить", callback_data=f"{dates_id[0][0]} Yes"), InlineKeyboardButton("❌Проигноривовать", callback_data=f"{dates_id[0][0]} No")) # разобраться, как передать переменную в callback_data
    return markup


# обработчик call_back
@bot.callback_query_handler(func=lambda call: True)
def get_moder(call):
    moder_ids = main(f"SELECT moder_id FROM Moders;")

    call_data = call.data.split()
    data = main(f"SELECT * FROM Hack WHERE `id`={call_data[0]}") 
    area, year, season, month, description, feedback, mark, src = data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][10]

    if call_data[1] == "Yes":
        if src != '0':
            print(1)
            bot.send_photo(-1001701836271, open(src, 'rb'),
                           caption=f"<b>🏢Район: </b> {area}\n\n<b>⏳Год: </b> {year}\n\n<b>🏝️Сезон: </b> {season}\n\n<b>📅Месяц: </b> {month}\n\n<b>📝Описание: </b> {description}\n\n<b>📈Отзыв: </b> {feedback}\n\n<b>🌟Субъективная оценка пользователя: </b> {mark}",
                           parse_mode="html")
            bot.send_message(806902493, "*Пост опубликован*", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
            bot.send_message(data[0][9], '✅ *Спасибо, ваши данные успешно прошли модерацию и опубликованы на канал!*', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")


        else:
            print(2)
            bot.send_message(-1001701836271, f"<b>🏢Район: </b> {area}\n\n<b>⏳Год: </b> {year}\n\n<b>🏝️Сезон: </b> {season}\n\n<b>📅Месяц: </b> {month}\n\n<b>📝Описание: </b> {description}\n\n<b>📈Отзыв: </b> {feedback}\n\n<b>🌟Субъективная оценка пользователя: </b> {mark}", parse_mode="html")
            bot.send_message(806902493, "*Пост опубликован*", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
            bot.send_message(data[0][9], '✅ *Спасибо, ваши данные успешно прошли модерацию и опубликованы на канал!*', reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")

        bot.answer_callback_query(call.id, "OK, POST PUBLISHED")

    elif call_data[1] == "No":
        print(3)
        bot.answer_callback_query(call.id, "OK, POST IGNORED")
        bot.send_message(data[0][9], '❌ *Простите, данные не прошли модерацию. Повторите попытку.*', parse_mode="Markdown")
        bot.send_message(806902493, "*❌Пост проигнорирован*", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")


bot.polling(non_stop=True, interval = 0)