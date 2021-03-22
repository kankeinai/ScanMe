from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp, bot
from datetime import datetime
import os
from converter import convert_to_jpeg
from scan import scan_photos
import keybords


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет! Я могу отсканировать почти что угодно и отправить тебе готовый .pdf Просто отправь мне столько фото сколько хочешь и напиши /scan", reply_markup=keybords.main_kb)
    await message.answer_sticker(r'CAACAgEAAxkBAAEBG0tfHq7a9x7k7JLAcBVg0oeBetR3WQACwCIAAnj8xgWCnglbp1nzEhoE')


@dp.message_handler(text="Помощь")
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message, ):
    text = "Я пока что не очень совершенный бот, но я стараюсь! Есть несколько ограничений:\n1. Постарайся чтобы фон не совпадал с цветом документа.\n2. Я могу сканировать только текст на белой бумаге (клетка не пойдет!).\nПросто отправь мне свои фото одним сообщением и посмотришь что выйдет)"
    await message.answer(text, reply_markup=keybords.main_kb)


@dp.message_handler(content_types=['photo'])
async def send_photo(msg: types.Message):
    uname = msg['from']['username']+"_"+str(datetime.now())
    if not os.path.exists("data"):
        os.makedirs("data")
    print(msg.photo[-1])
    await msg.photo[-1].download("data/"+uname.lower()+'.jpg')


@dp.message_handler(content_types=['document'])
async def send_document(msg: types.Message):
    uname = msg['from']['username']
    file_name = msg.document.file_name.lower()
    if not os.path.exists("data"):
        os.makedirs("data")
    src = 'data/' + uname+"_" + file_name
    await msg.document.download(src)
    text = convert_to_jpeg(uname, src)
    await msg.answer(text, reply_markup=keybords.main_kb)


@dp.message_handler(text="Сканировать")
@dp.message_handler(commands=['scan'])
async def process_scan_command(message: types.Message):
    user_id = message.from_user.id
    file_name = message['from']['username']+"_"+str(datetime.now())+".pdf"
    err = scan_photos(message['from']['username'], file_name, 2000)
    if (err):
        await message.answer("У меня не получилось просканировать некоторые фото :(", reply_markup=keybords.main_kb)
    try:
        await bot.send_document(user_id,  types.input_file.InputFile(file_name), caption='Я пытался! Если тебе не нравится качество попробуй отправить фото как документы :з После отправки документа нужно дождаться, чтобы бот сказал "Готово" ')
    except:
        await message.answer("Ты точно уверен что загрузил фото? А то у меня не вышло :(", reply_markup=keybords.main_kb)
    os.remove(file_name)


@dp.message_handler(text="Отменить")
@dp.message_handler(commands=['cancel'])
async def process_cancel_command(message: types.Message):
    my_dir = "data"
    uname = message['from']['username']
    for pictures in os.listdir(my_dir):
        if pictures.split("_")[0] == uname:
            os.remove(my_dir+"/"+pictures)
    await message.answer("Я все удалил, можешь отправлять сначала", reply_markup=keybords.main_kb)
