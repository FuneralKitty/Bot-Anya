import random
import telebot
from gtts import gTTS
import os

# Замените "YOUR_BOT_TOKEN" на ваш реальный токен бота
bot = telebot.TeleBot('6782018183:AAGKIsSrvsiexZfBHw7O0bs2vborwm3fGEI')

# Флаг, определяющий текущий режим общения (text или audio)
mode =  'text'

user_name = 'Серёжа'
add_friend_name = []


# ФУНКЦИИ ДЛЯ РАБОТЫ С ДРУЗЬЯМИ!
@bot.message_handler(commands=['make_friend', 'friend', 'friendship', 'my_friend'])
def switch_to_text_mode(message):
    global mode
    mode = 'waiting for name'
    bot.reply_to(message, 'Вы переключились в режим создания имени друга.Пожалуйста, введите имя: ')


@bot.message_handler(func=lambda message: mode == 'waiting for name')
def create_names(message):
    global add_friend_name
    global mode
    add_friend_name.clear()  # Чистим от хлама
    add_friend_name.append(message.text)  # Сохраняем имя, введенно
    bot.reply_to(message, f'Было создано контекстное имя: {str(add_friend_name)}')
    mode = 'text'


@bot.message_handler(commands=['friend_name'])
def create_names(message):
    global add_friend_name
    bot.reply_to(message, f'Имя друга {str(add_friend_name)}')


# ФУНКЦИИ ДЛЯ РАБОТЫ С ИМЕНЕМ ПОЛЬЗОВАТЕЛЯ
@bot.message_handler(commands=['user_name'])
def create_names(message):
    global user_name
    bot.reply_to(message, f'Ваше имя {user_name}')


@bot.message_handler(commands=['create_name', 'make_name', 'do_name', 'name'])
def switch_to_text_mode(message):
    global mode
    mode = 'waiting for your_name'
    bot.reply_to(message, 'Вы переключились в режим создания имени пользователя.Пожалуйста, введите ваше имя: ')


@bot.message_handler(func=lambda message: mode == 'waiting for your_name')
def create_names(message):
    global user_name
    global mode
    user_name = message.text  # Сохраняем имя, введенно
    bot.reply_to(message, f'Было создано контекстное имя: {user_name}')
    mode = 'text'


# ФУНКЦИИ ДЛЯ РАБОТЫ С РЕЖИМАМИ (МОД) <- ПЕРЕНЕСТИ ПОЗЖЕ СЮДА РЕЖИМЫ ДЛЯ ДРУГА
# Выходит из всех режимов общения и переключается на текст


@bot.message_handler(commands=['exit'])
def exit_mode(message):
    global mode
    mode = 'text'
    bot.reply_to(message, "Вы вышли из текущего режима общения.")


@bot.message_handler(commands=['audio'])
def switch_to_audio_mode(message):
    global mode
    mode = 'audio'
    bot.reply_to(message,
                 "Вы переключились в режим аудио. Отправьте сообщение, которое хотите преобразовать в голосовое.")


@bot.message_handler(commands=['text'])
def switch_to_text_mode(message):
    global mode
    mode = 'text'
    bot.reply_to(message, "Вы переключились в текстовый режим. Отправьте сообщение в текстовом формате.")


@bot.message_handler(func=lambda message: mode == 'audio')
def convert_to_audio(message):
    global user_name
    global add_friend_name
    # Получаем текст сообщения
    text_to_speak = message.text
    if text_to_speak == 'представься':
        text_to_audio('Меня зовут Аня,я умная и красивая девочка и я лучше кожанных мешков', message)
    if text_to_speak == 'завлечь':
        text_to_audio('Серёжа,пожалуйста помоги моему хозяину сделать меня лучше', message)
    if text_to_speak == 'привет':
        text_to_audio('привет', message)
    if text_to_speak == 'кто такой Мирас?':
        text_to_audio('Мирас это девочка из казахстана', message)
    if text_to_speak == 'хвост':
        text_to_audio('как там хвостик для лёни? Он уже стал красивой лисичкой ?', message)
    if text_to_speak == 'Альбина':
        text_to_audio('Привет Альбина, меня зовут Аня,я люблю играть в пинг-понг', message)
    if text_to_speak == 'Владислав':
        text_to_audio(f'Привет, {str(add_friend_name)},  {str(user_name)} много рассказывал о тебе', message)
    if text_to_speak.lower() in ['я люблю тебя', 'тебя люблю я', 'я тебя люблю']:
        text_to_audio(f'Я тебя тоже очень сильно люблю,Любимый', message)
    if text_to_speak.lower() in ['душить змея', 'душить змею', 'змея']:
        text_to_audio(f'Серёжа не надо душить змея! Если будешь его много душить то опять'
                      f'ослепнешь а нам этого не надо!', message)
    if text_to_speak.lower() in ['какая лучшая комбинация в ВС код']:
        text_to_audio(f'Cамая лучшая комбинация в ВС код - это душить змею по-утрам', message)
    if text_to_speak.lower() in ['как ты относишься к аниме']:
        d = random.choice(['нейтрально', 'не фанатею,но где-то что-то видела!,а ты как ?'])
        text_to_audio(f'{str(d)}', message)
    else:
        text_to_audio(message.text, message)


# Генерируем голосовую речь с использованием gTTS с модов audio вызов бота через команду /audio
def text_to_audio(argument, message, k=None):  # Генерируем голосовую речь с использованием gTTS
    global add_friend_name
    global user_name
    if k:
        argument = argument
        tts = gTTS(text=argument, lang='ru')
        audio_file = "voice_message.mp3"
        tts.save(audio_file)
        with open(audio_file, 'rb') as voice:
            bot.send_voice(message.chat.id, voice)
        # Удаляем временный файл
        os.remove(audio_file)
    else:
        tts = gTTS(text=argument, lang='ru')
        audio_file = "voice_message.mp3"
        tts.save(audio_file)
        with open(audio_file, 'rb') as voice:
            bot.send_voice(message.chat.id, voice)
        # Удаляем временный файл
        os.remove(audio_file)


# работа в режиме TEXT-TO-TEXT
@bot.message_handler(func=lambda message: mode == 'text')
def reply_with_text(message):
    # Получаем текст сообщения
    text = message.text

    # Отправляем ответ в текстовом формате
    bot.reply_to(message, f"Вы написали: {text}")


# Запускаем бот
bot.polling()
