import logging
from datetime import date

import telebot
from telebot import types
from database_funcs_369 import create_connection, insert_id, insert_name, insert_age, insert_weight, insert_height, \
    del_data, get_user_data, check_user_data, get_weight, get_height, create_connection_w, insert_weight_w, \
    del_data_w, get_weight_data, get_user, insert_id_w

'''from database_w import get_by_key_word, get_recipe, translate_text, translate_text_eng, insert_id_r_num_word, \
    insert_id_r_num_in, get_user_r, get_num_word, insert_rec, get_rec, filter_recipes'''

token = ''
bot = telebot.TeleBot(token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

cursor, conn = create_connection('users.db')
cursor_w, conn_w = create_connection_w('weight_history.db')
cursor_r, conn_r = create_connection_w('recipe.db')

start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_fill_data = types.KeyboardButton('Заполнить данные 🗒')
start_kb.add(btn_fill_data)

# Главное меню
main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_ak_data = types.KeyboardButton('Аккаунт 👤')
o_p_i_s = types.KeyboardButton('О питании и спорте 🥗🧘‍')
main_kb.add(btn_ak_data, o_p_i_s)

data_main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_fill_data = types.KeyboardButton('Заполнить данные 🗒')
btn_del_data = types.KeyboardButton('Удалить данные о себе 🗑️')
btn_weight = types.KeyboardButton('Динамика веса ⚖️')
btn_back = types.KeyboardButton('Назад🔙')
data_main_kb.add(btn_fill_data, btn_del_data, btn_weight, btn_back)

# Меню для заполнения данных
data_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_name = types.KeyboardButton('Имя')
btn_age = types.KeyboardButton('Возраст')
btn_height = types.KeyboardButton('Рост')
btn_weight = types.KeyboardButton('Вес')
btn_ok = types.KeyboardButton('Просмотреть все данные 👓')
btn_back = types.KeyboardButton('Назад (Аккаунт)🔙')
btn_ok2 = types.KeyboardButton('Я ввел(а) все данные ✅')
data_kb.add(btn_name, btn_age, btn_height, btn_weight, btn_ok, btn_ok2, btn_back)

weight_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_add_w = types.KeyboardButton('Добавить вес ➕')
btn_all_w = types.KeyboardButton('Посмтореть историю 📊')
btn_del_w = types.KeyboardButton('Удалить все изменения веса 🗑️')
btn_back = types.KeyboardButton('Назад (Аккаунт)🔙')
weight_kb.add(btn_add_w, btn_all_w, btn_del_w, btn_back)

function_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_res = types.KeyboardButton('Посик рецептов 🔎')
btn_funct = types.KeyboardButton('Статьи о питании и спорте 🌐')
btn_data = types.KeyboardButton('Расчитать ИМТ 🧮')
btn_back = types.KeyboardButton('Назад (О питании и спорте)🔙')
function_kb.add(btn_res, btn_funct, btn_data, btn_back)

r_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_word = types.KeyboardButton('Поиск по ключевому слову в названии блюда 🥗')#новый поиск еще не написан
btn_in = types.KeyboardButton('Поиск по ингридиентам 🍅') #новый поиск еще не написан
btn_back = types.KeyboardButton('Назад (Поиск рецептов)🔙')
r_kb.add(btn_word, btn_in, btn_back)

info_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_sport = types.KeyboardButton('О спорте 🏃')
btn_eat = types.KeyboardButton('О питании 🍽️')
btn_back = types.KeyboardButton('Назад (Статьи о питании и спорте)🔙')
info_kb.add(btn_sport, btn_eat, btn_back)

'''eng_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_en = types.KeyboardButton('Перевести рецепт на русский язык')
eng_kb.add(btn_en)'''

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я Рататуй — ваш персональный помощник в вопросах здоровья, питания и контроля веса.\n\n "
        "Мои функции:\n🍽 Подбор рецептов – помогу найти вкусные и полезные блюда\n"
        "📊 Расчет ИМТ – определю индекс массы тела и дам рекомендации\n"
        "📈 Контроль веса – сохраню историю изменений и покажу прогресс\n"
        "💡 Советы по питанию и спорту – поделюсь полезной информацией\n\n"
        "Просто скажите, с чего начать! 😊",
        reply_markup=start_kb
    )
    if check_user_data(cursor, message.chat.id) == "Пользователь не найден":
        bot.send_message(
            message.chat.id,
            "Перед началом работы давайте сохраним ваши данные в нашей базе. Не волнуйтесь - эта информация будет доступна только нам.",
        )
        chat_id = message.chat.id
        insert_id(cursor, chat_id)
    else:
        if check_user_data(cursor, message.chat.id) == "Все поля заполнены":
            bot.send_message(
                message.chat.id,
                "Ваши данные уже есть в нашей базе 😊", reply_markup=main_kb
            )
        else:
            message_data = check_user_data(cursor, message.chat.id)
            bot.send_message(message.chat.id, f'Вы уже есть в нашей базе.\n😞 Увы, Рататуй нашел не все ваши данные. {message_data}',
                             reply_markup=start_kb)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Я Рататуй — твой умный помощник для здорового образа жизни! 🌿\n\n'
                                      'Что я умею:\n• 🍴 Подбирать идеальные рецепты — вкусные, полезные и подходящие именно тебе\n'
                                      '• 📏 Автоматически рассчитывать ИМТ + давать персональные рекомендации\n'
                                      '• 📉 Вести дневник веса — наглядно покажу твой прогресс\n'
                                      '• 🏋️‍♂️ Делиться лайфхаками по питанию и тренировкам\n\n'
                                      'Готов помочь прямо сейчас! Просто напиши, что тебя интересует 😉')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Аккаунт 👤':
        bot.send_message(
            message.chat.id,
            'Рататуй ищет Вас',
            reply_markup=data_main_kb)

    if message.text == 'Заполнить данные 🗒':
        bot.send_message(
            message.chat.id,
            'Пожалуйста, заполните данные о себе. Вам необходимо:\n1️⃣ Выбрать тип данных, который хотите ввести.\n'
            '2️⃣ Нажать на кнопку с этим типом данных.\n'
            '3️⃣ Следовать дальнейшим инструкциям.\n'
            'После того, как заполните все данные, нажмите на кнопку "Я ввел(а) все данные ✅"',
            reply_markup=data_kb)

    elif message.text == 'Имя':
        msg = bot.send_message(message.chat.id, 'Введите пожалуйста свое имя:')
        bot.register_next_step_handler(msg, process_name_step)
    elif message.text == 'Возраст':
        msg = bot.send_message(message.chat.id, 'Введите пожалуйста свой возраст:')
        bot.register_next_step_handler(msg, process_age_step)
    elif message.text == 'Рост':
        msg = bot.send_message(message.chat.id, 'Введите пожалуйста свой рост (в см):')
        bot.register_next_step_handler(msg, process_height_step)
    elif message.text == 'Вес':
        msg = bot.send_message(message.chat.id, 'Введите пожалуйста свой вес (в кг):')
        bot.register_next_step_handler(msg, process_weight_step)

    elif message.text == ('Просмотреть все данные 👓'):
        if check_user_data(cursor, message.chat.id) == "Все поля заполнены":
            message_data = get_user_data(cursor, message.chat.id)
            bot.send_message(message.chat.id, message_data, reply_markup=data_kb)
        elif check_user_data(cursor, message.chat.id) == "Пользователь не найден":
            bot.send_message(message.chat.id, '😞 Увы, Рататуй потерял ваши данные', reply_markup=start_kb)
        else:
            message_data = check_user_data(cursor, message.chat.id)
            bot.send_message(message.chat.id, f'😞 Увы, Рататуй нашел не все ваши данные. {message_data}',
                             reply_markup=data_kb)

    elif message.text == 'Я ввел(а) все данные ✅':
        if check_user_data(cursor, message.chat.id) == "Все поля заполнены":
            message_data = get_user_data(cursor, message.chat.id)
            bot.send_message(message.chat.id, message_data, reply_markup=main_kb)
            bot.send_message(message.chat.id, "Спасибо! 🥰")
        elif check_user_data(cursor, message.chat.id) == "Пользователь не найден":
            bot.send_message(message.chat.id, '😞 Увы, Рататуй потерял ваши данные. Заполните их пожалуйста еще раз',
                             reply_markup=start_kb)
        else:
            message_data = check_user_data(cursor, message.chat.id)
            bot.send_message(message.chat.id, f'😞 Увы, Рататуй нашел не все ваши данные. {message_data}',
                             reply_markup=data_kb)

    elif message.text == 'Назад🔙':
        bot.send_message(
            message.chat.id,
            'Вы вернулись в главное меню',
            reply_markup=main_kb
        )
    elif message.text == 'Удалить все изменения веса 🗑️':
        bot.send_message(message.chat.id,
                         'Вы точно хотите удалить данные? После удаления: - Я не смогу предоставить вам расчеты.\n'
                         '- История изменений веса будет утеряна.\nДля возобновления работы потребуется ввести данные занаво.',
                         reply_markup=weight_kb)
        answer = types.InlineKeyboardMarkup()
        btn_w_yes = types.InlineKeyboardButton('Да', callback_data='del_data_w_yes', m_t=message.text,
                                               user_id=message.chat.id)
        btn_w_no = types.InlineKeyboardButton('Нет', callback_data='no_data_del')
        answer.add(btn_w_yes, btn_w_no)
        bot.send_message(message.chat.id, 'Удалить ваши данные?', reply_markup=answer)

    elif message.text == 'Удалить данные о себе 🗑️':
        bot.send_message(message.chat.id,
                         'Вы точно хотите удалить данные? После удаления: - Я не смогу предоставить вам расчеты.\n'
                         '- История изменений веса будет утеряна.\nДля возобновления работы потребуется ввести данные занаво.',
                         reply_markup=data_main_kb)
        answer = types.InlineKeyboardMarkup()
        btn_yes = types.InlineKeyboardButton('Да', callback_data='del_data_yes', m_t=message.text,
                                             user_id=message.chat.id)
        btn_no = types.InlineKeyboardButton('Нет', callback_data='no_data_del')
        answer.add(btn_yes, btn_no)
        bot.send_message(message.chat.id, 'Удалить ваши данные?', reply_markup=answer)

    elif message.text == 'Динамика веса ⚖️':
        bot.send_message(message.chat.id, 'В данном разделе можно остлеживать изменения вашего веса',
                         reply_markup=weight_kb)

    elif message.text == 'Добавить вес ➕':
        msg = bot.send_message(message.chat.id, 'Введите пожалуйста свой вес (в кг):')
        bot.register_next_step_handler(msg, process_weight_step_w)

    elif message.text == 'Посмтореть историю 📊':
        msg = get_weight_data(cursor_w, message.chat.id)
        bot.send_message(message.chat.id, msg)

    elif message.text == 'Назад (Аккаунт)🔙':
        bot.send_message(
            message.chat.id,
            'Вы вернулись в главное меню',
            reply_markup=data_main_kb)
    elif message.text == 'Назад🔙':
        bot.send_message(
            message.chat.id,
            'Вы вернулись в главное меню',
            reply_markup=main_kb)

    elif message.text == 'О питании и спорте 🥗🧘‍':
        bot.send_message(
            message.chat.id,
            'Рататуй все расскажет',
            reply_markup=function_kb)
    elif message.text == 'Расчитать ИМТ 🧮':
        if check_user_data(cursor, message.chat.id) == "Все поля заполнены":
            bot.send_message(
                message.chat.id,
                '‼️ ️Учтите, что состояние вашего здоровья можно пределить по ИМТ только, если вы старше 18 лет')
            imt = int(get_weight(cursor, message.chat.id)) / (int(get_height(cursor, message.chat.id)) / 100) ** 2
            bot.send_message(
                message.chat.id,
                f'Индек массы вашего тела равен {round(imt, 1)}')
            bot.send_photo(message.chat.id,
                           "https://avatars.mds.yandex.net/i?id=14d88f3102c262c9d346b50f89ba06cc_l-3939094-images-thumbs&n=13")
        elif check_user_data(cursor, message.chat.id) == "Пользователь не найден":
            bot.send_message(message.chat.id, '😞 Увы, Рататуй потерял ваши данные, заполните пожалуйства данные занво',
                             reply_markup=start_kb)
        else:
            message_data = check_user_data(cursor, message.chat.id)
            bot.send_message(message.chat.id, f'😞 Увы, Рататуй нашел не все ваши данные. {message_data}',
                             reply_markup=data_kb)

    elif message.text == 'Статьи о питании и спорте 🌐':
        bot.send_message(message.chat.id, 'Для того, чтобы получить информацию вам необходимо выбрать нужную тему.',
                         reply_markup=info_kb)

    elif message.text == 'О питании 🍽️':
        bot.send_message(message.chat.id,
                         '1. ФИЦ питания и биотехнологии (Россия, официальный сайт)\n🔹https://ion.ru\n'
                         '✅ Государственный институт, разрабатывающий нормы питания для РФ. Есть таблицы БЖУ, витаминов и минералов.\n\n '
                         '2. Роспотребнадзор – «Здоровое питание»\n🔹https://здоровое-питание.рф\n'
                         '✅ Официальный проект с рекомендациями, калькуляторами калорий и статьями от врачей.\n\n'
                         '3. ПостНаука (раздел «Биология» и «Медицина»)\n🔹https://postnauka.ru'
                         '\n✅ Лекции и статьи учёных о биохимии пищи, метаболизме и микронутриентах.\n\n'
                         '4. «КиберЛенинка» (научные статьи)\n🔹https://cyberleninka.ru\n'
                         '✅ Бесплатные исследования российских учёных по диетологии (ищите по ключевым словам).\n\n'
                         '5. «Биомолекула» (научно-популярный сайт)\n🔹https://biomolecula.ru\n'
                         '✅ Подробные материалы о нутриентах.\n\n'
                         '6. «Министерство здравоохранения РФ» (раздел о питании)\n🔹https://minzdrav.gov.ru\n'
                         '✅ Официальные рекомендации, включая нормы для детей и взрослых.\n\n'
                         '7. «Здоровье Mail.ru» (раздел «Диетология»)\n🔹https://cgon.rospotrebnadzor.ru/naseleniyu/zdorovyy-obraz-zhizni/chto-takoe-zdorovoe-pitanie/\n'
                         '✅ Советы от экспертов для здорового образа жизни.\n\n'
                         '8. «ТАСС Наука» (раздел «Медицина»)\n🔹https://nauka.tass.ru/medicina\n'
                         '✅ Новости о исследованиях в области питания (например, о роли цинка или омега-3).\n\n'
                         '9. «Элементы» (научпоп от РАН)\n🔹https://elementy.ru\n'
                         '✅ Объяснения биохимических процессов.\n\n'
                         '10. «FoodNews» (о составе продуктов)\n🔹https://foodnews-press.ru\n'
                         '✅ Анализ пищевой ценности продуктов по данным Роспотребнадзора.',
                         reply_markup=info_kb)

    elif message.text == 'О спорте 🏃':
        bot.send_message(message.chat.id, '1. Спорт - Экспресс(раздел «Наука и спорт»)\n🔹https: // www.sport-express.ru \n'
                                          '✅ Новости, интервью с тренерами и врачами, аналитика влияния спорта на организм.\n\n'
                                          '2.Управление Федеральной службы по надзору в сфере защиты прав потребителей и благополучия человека\n'
                                          '✅ О пользе занятий спортом.\n\n'
                                          '3.«РЖД-Медицина»\n🔹https://67.rospotrebnadzor.ru/content/104/125346/\n'
                                          '✅ Спорт - как основа здорового образа жизни.\n\n'
                                        '4.«Спортмастер»\n🔹https://www.sportmaster.ru/media/articles/11675246/?utm_referrer=https://yandex.ru/\n'
                                          '✅ Планирование и организация тренировок.\n\n'
                                          '5.«Skillbox»\n🔹https://skillbox.ru/media/health/strength-training/\n'
                                          '✅ Силовые тренировки: что это такое, в чём их польза и вред, как заниматься правильно. Фитнес-тренер о том, почему штанга и гантели подходят не только брутальным мужчинам.\n\n'
                                          '6.«Дзен»\n🔹https://dzen.ru/a/ZGFf5FI3ImYrEIZM\n'
                                          '✅ Как эффективно нагружать мышцы, не впадая в перетренированность.\n\n'
                                          '7.«FitStars media»\n🔹https://fitstars.ru/blog/healthy-lifestyle/shest-rabotayushchih-sposobov-prevratit-trenirovki-v-obraz-zhizni\n'
                                          '✅ 6 работающих способов превратить тренировки в образ жизни.\n\n'
                                          '8.«Will food»\n🔹https://blog.willfood.pro/post/iskusstvo-garmonii-pravilnoe-pitanie-i-sport-dlya-optimalnyh-rezultatov\n'
                                          '✅ Искусство гармонии: Правильное питание и спорт для оптимальных результатов.\n\n'
                                          '9.«Дзен»\n🔹https://dzen.ru/a/Z67yB08Fo2azPYfj\n'
                                          '✅ Объясняю на пальцах, как составить себе программу тренировок\n\n'
                                          '10.«Спортмастер»\n🔹https://www.sportmaster.ru/media/articles/11562722/?utm_referrer=https://yandex.ru/\n'
                                          '✅5 программ домашних тренировок для начинающих\n\n',
                         reply_markup=info_kb)


    elif message.text == 'Назад (Статьи о питании и спорте)🔙':
        bot.send_message(
            message.chat.id,
            'Вы вернулись в главное меню',
            reply_markup=function_kb)

    elif message.text == 'Посик рецептов 🔎':
        #s, b = get_user_r(cursor_r, message.chat.id)
        #if not s or s == 'Пользователь не найден':
            #print("Пользователь не найден - рецепты")
            #insert_id_r_num_word(cursor, message.chat.id, 0)
            #insert_id_r_num_in(cursor, message.chat.id, 0)
        bot.send_message(message.chat.id,
                         'В данном разделе вы можете найти нужные рецепты.\n\nПоиск рецептов возможен двумя способами:\n1️⃣ По ключевому слову в названии блюда.\n'
                         '2️⃣По ингредиентам которые должны быть в блюде.',
                         reply_markup=r_kb)

    elif message.text == 'Поиск по ингрeдиентам 🍅':
        msg = bot.send_message(message.chat.id,
                               'Введите пожалуйста ингредиенты, которое должны быть в бдюде через точку с запятой и пробел.\n'
                               'Например: Курица; молоко')
        #bot.register_next_step_handler(msg, process_rec_in)

    elif message.text == 'Поиск по ключевому слову в названии блюда 🥗':
        msg = bot.send_message(message.chat.id,
                               'Введите пожалуйста слово, которое должно быть в названии рецептов, которые я найду.\n'
                               'Например: Курица')
        #bot.register_next_step_handler(msg, process_rec_s)

    elif message.text == 'Назад (Поиск рецептов)🔙':
        bot.send_message(
            message.chat.id,
            'Вы вернулись в главное меню',
            reply_markup=function_kb
        )

    elif message.text == 'Назад (О питании и спорте)🔙':
        bot.send_message(
            message.chat.id,
            'Вы вернулись в главное меню',
            reply_markup=main_kb
        )

    """elif message.text == 'Перевести рецепт на русский язык':
        rec_get = get_rec(cursor_r, message.chat.id)
        t = translate_text(rec_get)
        bot.send_message(message.chat.id, t, reply_markup=r_kb)"""

"""def process_rec_s(message):
    bot.send_message(message.chat.id, 'Поиск рецепта займет около одной минуты. Прошу прощения за такое долгое ожидание. \n'
                                      'После того, как я найду нужный рецепт, я пришлю его в этот чат в двух экземплярах: на английском и на русском языках. '
                                      'К сожалению, перевод на русский язык может быть не полностью корректен, прошу прощения, если такое произойдет', reply_markup=r_kb)
    t1 = message.text.split(', ')
    if t1[1] == 0:
        num = 0
    else:
        num = int(t1[1]) + 1
    t = translate_text_eng(t1[0])
    m_t = get_by_key_word(t, num)
    #insert_rec(cursor_r, message.chat.id, m_t)
    bot.send_message(message.chat.id, "\n".join(m_t), reply_markup=r_kb)
    bot.send_message(message.chat.id, translate_text("\n".join(m_t)), reply_markup=r_kb)

'''def process_rec_s(message):
    bot.send_message(message.chat.id, 'Поиск рецепта займет около одной минуты. Прошу прощения за такое долгое ожидание. \n'
                                      'После того, как я найду нужный рецепт, я пришлю его в этот чат в двух экземплярах: на английском и на русском языках. '
                                      'К сожалению, перевод на русский язык может быть не полностью корректен, прошу прощения, если такое произойдет', reply_markup=r_kb)
    t1 = message.text.split(', ')
    print(t1[0])
    if t1[1] == 0:
        num = 0
    else:
        num = int(t1[1]) + 1
    t = translate_text_eng(t1[0])
    m_t = get_by_key_word(t, num)
    print(m_t)
    #insert_rec(cursor_r, message.chat.id, m_t)
    bot.send_message(message.chat.id, "\n".join(m_t), reply_markup=r_kb)
    bot.send_message(message.chat.id, translate_text("\n".join(m_t)), reply_markup=r_kb)'''


def process_rec_in(message):
    bot.send_message(message.chat.id, 'Поиск рецепта займет около одной минуты. Прошу прощения за такое долгое ожидание. \n'
                                      'После того, как я найду нужный рецепт, я пришлю его в этот чат в двух экземплярах: на английском и на русском языках. '
                                      'К сожалению, перевод на русский язык может быть не полностью корректен, прошу прощения, если такое произойдет', reply_markup=r_kb)
    ing = message.text.split('; ')
    t1 = message.text.split(', ')
    if t1[1] == 0:
        num = 0
    else:
        num = int(t1[1]) + 1
    #if not ing
    with_ing = ing[0]
    without_ing = ing[1]
    t_with = translate_text_eng(with_ing)
    t_without = translate_text_eng(without_ing)
    m_t = filter_recipes(t_with, t_without, num)
    #insert_rec(cursor_r, message.chat.id, m_t)
    bot.send_message(message.chat.id, "\n".join(m_t), reply_markup=r_kb)
    bot.send_message(message.chat.id, translate_text("\n".join(m_t)), reply_markup=r_kb)""" #старый поиск рецептов в дб

def process_name_step(message):
    # Здесь можно сохранить имя
    answer = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='name_yes')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='name_no')
    answer.add(btn_yes, btn_no)
    bot.send_message(
        message.chat.id,
        f'Вы ввели имя: {message.text}. Всё верно?',
        reply_markup=answer
    )


def process_age_step(message):
    # Здесь можно сохранить возраст
    answer = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='age_yes')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='age_no')
    answer.add(btn_yes, btn_no)
    if message.text.isdigit() and 120 > int(message.text) > 0:
        bot.send_message(
            message.chat.id,
            f'Вы ввели возраст: {message.text}. Всё верно?',
            reply_markup=answer
        )
    else:
        bot.send_message(
            message.chat.id,
            f'😞Вы ввели неверный тип данных.\nЧтобы исправить ввод, вам нужно:\n1️⃣Выбрать нужный тип данных.\n2️⃣Ввести данные занаво.\n3️⃣Следовать дальнейшим инструкциям.',
            reply_markup=data_kb)


def process_height_step(message):
    # Здесь можно сохранить рост
    answer = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='height_yes')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='height_no')
    answer.add(btn_yes, btn_no)
    if message.text.isdigit() and 300 > int(message.text) > 0:
        bot.send_message(
            message.chat.id,
            f'Вы ввели рост: {message.text} см. Всё верно?',
            reply_markup=answer
        )
    else:
        bot.send_message(
            message.chat.id,
            f'😞Вы ввели неверный тип данных.\nЧтобы исправить ввод, вам нужно:\n1️⃣Выбрать нужный тип данных.\n2️⃣Ввести данные занаво.\n3️⃣Следовать дальнейшим инструкциям.',
            reply_markup=data_kb)


def process_weight_step(message):
    # Здесь можно сохранить вес
    answer = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='weight_yes')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='weight_no')
    answer.add(btn_yes, btn_no)
    tt = message.text.replace(',', '.')
    print(tt)
    t = tt.replace('.', '')
    if t.isdigit() and 30000 > int(t) > 0:
        bot.send_message(
            message.chat.id,
            f'Вы ввели вес: {tt} кг. Всё верно?',
            reply_markup=answer
        )
    else:
        bot.send_message(
            message.chat.id,
            f'😞Вы ввели неверный тип данных.\nЧтобы исправить ввод, вам нужно:\n1️⃣Выбрать нужный тип данных.\n2️⃣Ввести данные занаво.\n3️⃣Следовать дальнейшим инструкциям.',
            reply_markup=data_kb)


def process_weight_step_w(message):
    answer = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='weight_w_yes')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='weight_no_w')
    answer.add(btn_yes, btn_no)
    tt = message.text.replace(',', '.')
    t = tt.replace('.', '')
    if t.isdigit() and 30000 > int(t) > 0:
        bot.send_message(
            message.chat.id,
            f'Вы ввели вес: {tt} кг. Всё верно?',
            reply_markup=answer
        )
    else:
        bot.send_message(
            message.chat.id,
            f'😞Вы ввели неверный тип данных.\nЧтобы исправить ввод, вам нужно:\n1️⃣Выбрать нужный тип данных.\n2️⃣Ввести данные занаво.\n3️⃣Следовать дальнейшим инструкциям.',
            reply_markup=weight_kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    m_t = call.message.text
    if call.data.endswith('_yes'):
        print('имя да')
        if call.data == 'name_yes':
            print(1)
            name = m_t.split(': ')[1].split('.')[0]
            insert_name(cursor, chat_id, name)
            bot.send_message(call.message.chat.id, 'Данные сохранены! ✅', reply_markup=data_kb)

        if call.data == 'age_yes':
            age = m_t.split(': ')[1].split('.')[0]
            insert_age(cursor, chat_id, age)
            bot.send_message(call.message.chat.id, 'Данные сохранены! ✅', reply_markup=data_kb)

        if call.data == 'height_yes':
            height = m_t.split(': ')[1].split(' см.')[0]
            insert_height(cursor, chat_id, height)
            bot.send_message(call.message.chat.id, 'Данные сохранены! ✅', reply_markup=data_kb)

        if call.data == 'weight_yes':
            weight = float(m_t.split(': ')[1].split(' кг')[0])
            insert_weight(cursor, chat_id, weight)
            insert_weight_w(cursor_w, weight, chat_id, date.today().strftime("%d-%m-%Y"))
            bot.send_message(call.message.chat.id, 'Данные сохранены! ✅', reply_markup=data_kb)

        if call.data == 'del_data_yes':
            del_data(cursor, chat_id)
            del_data_w(cursor_w, chat_id)
            insert_id(cursor, chat_id)
            bot.send_message(call.message.chat.id, 'Ваши данные удалены ✅',
                             reply_markup=start_kb)
        if call.data == 'del_data_w_yes':
            del_data_w(cursor_w, chat_id)
            insert_weight_w(cursor_w, int(get_weight(cursor, chat_id)), chat_id, date.today().strftime("%d-%m-%Y"))
            bot.send_message(call.message.chat.id, 'Ваша история веса удалена ✅',
                             reply_markup=weight_kb)

        if call.data == 'weight_w_yes':
            weight = float(m_t.split(': ')[1].split(' кг')[0])
            insert_weight(cursor, chat_id, weight)
            insert_weight_w(cursor_w, weight, chat_id, date.today().strftime("%d-%m-%Y"))
            bot.send_message(call.message.chat.id, 'Именение вашего веса сохранено!', reply_markup=weight_kb)

    elif call.data == 'no_data_del':
        bot.send_message(call.message.chat.id, 'Рататуй сохранил ваши данные в порядкке', reply_markup=data_main_kb)

    if call.data == 'weight_no_w':
        bot.send_message(call.message.chat.id, 'Изменения не сохранены', reply_markup=weight_kb)

    elif call.data.endswith('_no'):
        bot.send_message(call.message.chat.id, 'Пожалуйста, выберите нужный тип данных и введите данные заново',
                         reply_markup=data_kb)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
