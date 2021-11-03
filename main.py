import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import sleep
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import kb
import album as ab

#252114764

class Form(StatesGroup):
    song = State()
    name_of_song = State()
    name_of_artists = State()
    author_of_song = State()  # Задаем состояние
    author_of_text = State()
    text_of_song = State()
    picture_of_song = State()
    is_ready = State()


API_TOKEN = 'TOKEN'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(ab.AlbumMiddleware())


@dp.message_handler(commands=['start'])
async def starting(message: types.Message):
    await message.answer('Привет, Бот создан для отправки песен на прослушивание.\n'
                         'Для этого нажми на соответсвующую кнопку. Также стоит прочитать требования.',
                         reply_markup=kb.bt12)


@dp.message_handler(lambda message: message.text == "Узнать требования")
async def txt_trebovaniya(message: types.Message):
    await message.answer("Требование такие бла бла бла", reply_markup=kb.bt2)


@dp.message_handler(lambda message: message.text == "Отправить трек на прослушивание")
async def txt_trebovaniya(message: types.Message, state: FSMContext):
    await message.answer("Отправьте песню в формате MP3 или WAV или пришлите ссылку на него:",
                         reply_markup=kb.bt_remove)
    await Form.song.set()


@dp.message_handler(state=Form.song, is_media_group=False,
                    content_types=types.ContentTypes.AUDIO)  # Принимаем состояние
async def start1(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['song'] = message.audio
        print(message.audio.file_id)
        await message.answer("Файл загружен успешно!")
    await state.update_data(song=message.audio.file_id)
    await Form.next()  # Переключаем состояние
    await message.answer("Введите название песни:")


@dp.message_handler(state=Form.song, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start1(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['song'] = message.text
        # print(message.audio.file_id)
        await message.answer("Ссылка получена!")
    await state.update_data(song=message.text.title())
    await Form.next()  # Переключаем состояние
    await message.answer("Введите название песни:")


@dp.message_handler(state=Form.name_of_song, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['name_of_song'] = message.text
        print(message.text)
        await message.answer("Введите имена артистов:")
        await state.update_data(name_of_song=message.text.title())
        await Form.next()


@dp.message_handler(state=Form.name_of_artists, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['name_of_artists'] = message.text
        await message.answer("Введите имена авторов песни:")
        print(message.text)
        await state.update_data(name_of_artists=message.text.title())
        await Form.next()


@dp.message_handler(state=Form.author_of_song, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['author_of_song'] = message.text
        await message.answer("Введите имена авторов текста:")
        print(message.text)
        await state.update_data(author_of_song=message.text.title())
        await Form.next()


@dp.message_handler(state=Form.author_of_text, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['author_of_text'] = message.text
        await message.answer("Введите текст песни")
        print(message.text)
        await state.update_data(author_of_text=message.text.title())
        await Form.next()


@dp.message_handler(state=Form.text_of_song, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['text_of_song'] = message.text
        await message.answer("Отправьте изображение обложки или ссылку на множество изображений")
        print(message.text)
        await state.update_data(text_of_song=message.text.title())
        await Form.next()


@dp.message_handler(state=Form.picture_of_song, is_media_group=False,
                    content_types=types.ContentTypes.PHOTO)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['picture_of_song'] = message.photo[0]
        print(message.photo[0].file_id)
        await state.update_data(picture_of_song=message.photo[0].file_id)
        user_data = await state.get_data()
        await message.answer("Фото успешно загружено!")
        #await state.finish()
    await message.answer(
        'Название песни: ' + user_data['name_of_song'] + '\n' + 'Имена артистов: ' + user_data['name_of_artists']
        + '\n' + 'Автор песни: ' + user_data['author_of_song'] + '\n' + 'Автор текста: '
        + user_data['author_of_text'] + '\n' + 'Текст песни: ' + user_data['text_of_song'])
    await message.answer("Фото обложки:")
    await bot.send_photo(photo=user_data['picture_of_song'], chat_id=message.from_user.id)
    await message.answer("Песня:")
    try:
        await bot.send_audio(audio=user_data['song'], chat_id=message.from_user.id)
    except:
        await message.answer(user_data['song'])
    await message.answer("Если все правильно нажмите кнопку 'Готово'\nМожете также начать 'Заново', нажав "
                         "соответствующую кнопку", reply_markup=kb.bt6)
    await Form.next()
    print(message.from_user.id)


# state=Form.picture_of_song,

@dp.message_handler(state=Form.picture_of_song, content_types=types.ContentTypes.TEXT)  # Принимаем состояние
async def start2(message: types.Message, state: FSMContext):
    async with state.proxy() as a:  # Устанавливаем состояние ожидания
        a['picture_of_song'] = message.text
        await state.update_data(picture_of_song=message.text.title())
        user_data = await state.get_data()
        await message.answer("Ссылка на фотографии успешно получена!")
    await message.answer(
        'Название песни: ' + user_data['name_of_song'] + '\n' + 'Имена артистов: ' + user_data['name_of_artists']
        + '\n' + 'Автор песни: ' + user_data['author_of_song'] + '\n' + 'Автор текста: '
        + user_data['author_of_text'] + '\n' + 'Текст песни: ' + user_data['text_of_song'])
    await message.answer("Фото обложки:")
    await message.answer(user_data['picture_of_song'])
    await message.answer("Песня:")
    try:
        await bot.send_audio(audio=user_data['song'], chat_id=message.from_user.id)
    except:
        await message.answer(user_data['song'])
    await message.answer("Если все правильно нажмите кнопку 'Готово'\nМожете также начать 'Заново', нажав "
                         "соответствующую кнопку", reply_markup=kb.bt6)
    await Form.next()

    print(message.from_user.id)


@dp.message_handler(state=Form.picture_of_song, is_media_group=True, content_types=types.ContentType.ANY)
async def start2(message: types.Message, state: FSMContext):
    """This handler will receive a complete album of any type."""
    async with state.proxy() as a:
        await message.answer("Отправьте только 1 файл или ссылку на множество файлов")


@dp.message_handler(state=Form.song, is_media_group=True, content_types=types.ContentType.ANY)
async def start2(message: types.Message, state: FSMContext):
    """This handler will receive a complete album of any type."""
    async with state.proxy() as a:
        await message.answer("Отправьте только 1 файл или ссылку на множество файлов")


@dp.message_handler(state=Form.is_ready, content_types=types.ContentTypes.TEXT)
async def txt_trebovaniya(message: types.Message, state: FSMContext):
    if message.text == "Я передумал, не отправлять":
        await state.finish()
        await message.answer("Хорошо! можете попробовать заново: ", reply_markup=kb.bt2)  # Отправить код владельцу
    elif message.text == "Готово!":
        user_data = await state.get_data()
        await bot.send_message(252114764,'Отправитель: @' + message.from_user.username +
                               '\n' 'Название песни: ' + user_data['name_of_song'] + '\n' + 'Имена артистов: ' + user_data['name_of_artists']
            + '\n' + 'Автор песни: ' + user_data['author_of_song'] + '\n' + 'Автор текста: '
            + user_data['author_of_text'] + '\n' + 'Текст песни: ' + user_data['text_of_song'])
        await bot.send_message(252114764,'Прикрепленное аудио:')
        try:
            await bot.send_audio(audio=user_data['song'], chat_id=252114764)
        except:
            await bot.send_message(252114764, user_data['song'])
        await bot.send_message(252114764, 'Прикрепленное фото:')
        try:
            await bot.send_photo(photo=user_data['picture_of_song'], chat_id=252114764)
        except:
            await bot.send_message(252114764, user_data['picture_of_song'])
        await state.finish()
        await message.answer("Отлично! Ваша заявка успешно отправлена!", reply_markup=kb.bt2)  # Отправить код владельцу


@dp.message_handler(state='*')
async def opisanie_fila(message: types.Message):
    await message.answer("Упс. Я получил не то, что ожидал!")


if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as e:
            sleep(3)
            print(e)
