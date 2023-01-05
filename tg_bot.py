from bot_config import token
from keyboa import Keyboa
from telebot import TeleBot
from telebot import types
from parse_cfg import URL, HEADERS, URL_for_evenodd
from parse import groups_name_array, get_group_url, get_schedule, get_depart_names, even_odd_check
from datetime import datetime

bot = TeleBot(token)

lesson_time = {
    1: '8:30-10:05',
    2: '10:15-11:50',
    3: '12:00-13:35',
    4: '13:50-15:25',
    5: '15:40-17:15',
    6: '17:15-19:00',
    7: '19:10-20:45'
}

week_day_num = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5
}


@bot.message_handler(commands=['start'])
def start(message):
    start_message = f"Hi, <u>{message.from_user.first_name}</u>!\nI'm your personal study assistant. " \
                    f"At the moment I can only show your schedule for today or for selected day.\nIf you have any problems with the bot" \
                    f", please contact <b>@turrrrrrboUl</b>"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton('Schedule for today')
    button2 = types.KeyboardButton('Schedule for selected day')
    markup.add(button1, button2)
    bot.send_message(chat_id=message.chat.id, text=start_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_buttons(message):
    faculties_menu = ['АК', 'БМТ', 'ИБМ', 'ИСОТ', 'ИУ', 'Л', 'МТ', 'ОЭ', 'ПС', 'РК',
                      'РКТ', 'РЛ', 'РТ', 'СГН', 'СМ', 'ФН', 'Э', 'ЮР', 'ИУК', 'МК', 'К', 'ЛТ']
    keyboard_fac = Keyboa(items=faculties_menu, items_in_row=4, copy_text_to_callback=True, back_marker='$')
    week_day_menu = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    keyboard_days = Keyboa(items=week_day_menu, items_in_row=1, copy_text_to_callback=True, back_marker='*')
    if message.text == 'Schedule for today':
        bot.send_message(chat_id=message.chat.id, text='Select your faculty:', reply_markup=keyboard_fac())
    elif message.text == 'Schedule for selected day':
        bot.send_message(chat_id=message.chat.id, text='Select day:', reply_markup=keyboard_days())
    else:
        bot.send_message(chat_id=message.chat.id, text="Sorry, I don't understand you. "
                                                       "Please use buttons to communicate with me")


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    received_callback = call.data
    marker = received_callback[-1]
    pure_callback = received_callback[:-1]
    selected_day = False

    if marker == '*':
        selected_day = week_day_num[pure_callback]
        faculties_menu = ['АК', 'БМТ', 'ИБМ', 'ИСОТ', 'ИУ', 'Л', 'МТ', 'ОЭ', 'ПС', 'РК',
                          'РКТ', 'РЛ', 'РТ', 'СГН', 'СМ', 'ФН', 'Э', 'ЮР', 'ИУК', 'МК', 'К', 'ЛТ']
        keyboard_fac = Keyboa(items=faculties_menu, items_in_row=4, copy_text_to_callback=True, back_marker='$')
        bot.send_message(chat_id=call.message.chat.id, text='Select your faculty:', reply_markup=keyboard_fac())
    elif marker == '$':
        menu1 = get_depart_names(URL, HEADERS, received_callback[:-1])
        keyboard = Keyboa(items=menu1, copy_text_to_callback=True, back_marker='#',
                          items_in_row=4)
        bot.send_message(chat_id=call.message.chat.id, text='Select your department: ', reply_markup=keyboard())

    elif marker == '#':
        dep_name = received_callback.replace('#', '')

        menu2 = groups_name_array(URL, HEADERS, dep_name)
        if menu2:
            keyboard = Keyboa(items=menu2, copy_text_to_callback=True,
                              back_marker='%', items_in_row=3)
            bot.send_message(chat_id=call.message.chat.id, text='Select your group:', reply_markup=keyboard())
        else:
            bot.send_message(chat_id=call.message.chat.id, text='There are no active groups in selected department. '
                                                                'Please choose another department')


    elif marker == '%':
        group_name = received_callback.replace('%', '')
        url = get_group_url(URL, HEADERS, group_name)
        schedule = get_schedule(url, HEADERS)
        day_of_week = datetime.weekday(datetime.now())
        text = f'<b>{schedule[day_of_week][0]}</b>, {group_name}'
        bot.send_message(chat_id=call.message.chat.id, text=text, parse_mode='html')
        count = 0
        if len(schedule[day_of_week]) == 1:
            bot.send_message(chat_id=call.message.chat.id, text='No lessons today. Go drink some beer!🍻',
                             parse_mode='Markdown')
        else:
            even_odd_week_offset = even_odd_check(URL_for_evenodd, HEADERS)
            empty_flag = True
            for i in range(1 + even_odd_week_offset, len(schedule[day_of_week]), 2):
                count += 1
                message = f'<b><u>{lesson_time[count]}</u></b> - {schedule[day_of_week][i]}'
                if schedule[day_of_week][i] != ' ':
                    bot.send_message(chat_id=call.message.chat.id, text=message, parse_mode='html')
                    empty_flag = False
            if empty_flag:
                bot.send_message(chat_id=call.message.chat.id, text='No lessons today. Go drink some beer!🍻',
                                 parse_mode='Markdown')


bot.infinity_polling()
