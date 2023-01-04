from bot_config import token
from keyboa import Keyboa
from telebot import TeleBot
from parse_cfg import URL, HEADERS, URL_for_evenodd
from parse import groups_name_array, get_group_url, get_schedule, get_depart_names, even_odd_check
from datetime import datetime

bot = TeleBot(token)

lesson_time ={
    1: '8:30-10:05',
    2: '10:15-11:50',
    3: '12:00-13:35',
    4: '13:50-15:25',
    5: '15:40-17:15',
    6: '17:15-19:00',
    7: '19:10-20:45'
}

@bot.message_handler(commands=['start'])
def start(message):
    global uid
    uid = message.chat.id
    menu = ['АК', 'БМТ', 'ИБМ', 'ИСОТ', 'ИУ', 'Л', 'МТ', 'ОЭ', 'ПС', 'РК',
            'РКТ', 'РЛ', 'РТ', 'СГН', 'СМ', 'ФН', 'Э', 'ЮР', 'ИУК', 'МК', 'К', 'ЛТ']
    keyboard = Keyboa(items=menu, items_in_row=4, copy_text_to_callback=True, back_marker='$')
    text = 'Choose your faculty:'
    bot.send_message(chat_id = message.chat.id, text=text, reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    received_callback = call.data
    if received_callback[-1] == '$':
        menu1 = get_depart_names(URL, HEADERS, received_callback[:-1])
        keyboard = Keyboa(items=menu1, copy_text_to_callback=True, back_marker='#',
                          items_in_row=4)
        bot.send_message(chat_id=call.message.chat.id, text='Choose your department: ', reply_markup=keyboard())

    elif received_callback[-1] == '#':
        dep_name = received_callback.replace('#', '')

        menu2 = groups_name_array(URL, HEADERS, dep_name)
        keyboard = Keyboa(items=menu2, copy_text_to_callback=True,
                          back_marker='%', alignment=True)
        bot.send_message(chat_id=call.message.chat.id, text='Choose your group:', reply_markup=keyboard())

    elif received_callback[-1] == '%':
        group_name = received_callback.replace('%', '')
        url = get_group_url(URL, HEADERS, group_name)
        schedule = get_schedule(url, HEADERS)
        day_of_week = datetime.weekday(datetime.now())
        text = f'<b>{schedule[day_of_week][0]}</b>, {group_name}'
        bot.send_message(chat_id=call.message.chat.id, text=text, parse_mode='html')
        count = 0
        if len(schedule[day_of_week]) == 1:
            bot.send_message(chat_id=call.message.chat.id, text='No lessons today. Go drink some beer!🍻', parse_mode='Markdown')
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
                bot.send_message(chat_id=call.message.chat.id, text='No lessons today. Go drink some beer!🍻', parse_mode='Markdown')



bot.infinity_polling()