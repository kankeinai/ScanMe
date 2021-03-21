from aiogram import types
from loader import dp, bot
from datetime import datetime
import os
from scan import scan_photos


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет! Я могу отсканировать почти что угодно и отправить тебе готовый .pdf Просто отправь мне столько фото сколько хочешь и напиши /scan")
    await message.answer_sticker(r'CAACAgEAAxkBAAEBG0tfHq7a9x7k7JLAcBVg0oeBetR3WQACwCIAAnj8xgWCnglbp1nzEhoE')


@ dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    text = "Я пока что не очень совершенный бот, но я стараюсь! Есть несколько ограничений:\n1. Постарайся чтобы фон не совпадал с цветом документа.\n2. Я могу сканировать только текст на белой бумаге (клетка не пойдет!).\nПросто отправь мне свои фото одним сообщением и посмотришь что выйдет)"
    await message.answer(text)


@ dp.message_handler(content_types=['photo'])
async def attach_photo(msg: types.Message):
    uname = msg['from']['username']+"_"+str(datetime.now())
    if not os.path.exists("data"):
        os.makedirs("data")
    print(msg.photo[-1])
    await msg.photo[-1].download("data/"+uname.lower()+'.jpg')


@ dp.message_handler(commands=['scan'])
async def process_help_command(message: types.Message):
    user_id = message.from_user.id
    file_name = message['from']['username']+"_"+str(datetime.now())+".pdf"
    err = scan_photos(message['from']['username'], file_name, 1280)
    if (err):
        await message.answer("У меня не получилось просканировать некоторые фото :(")
    try:
        await bot.send_document(user_id,  types.input_file.InputFile(file_name), caption='Я пытался!')
    except:
        await message.answer("Ты точно уверен что загрузил фото? А то у меня не вышло :(")
    os.remove(file_name)
