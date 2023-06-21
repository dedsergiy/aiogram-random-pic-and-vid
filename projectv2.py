import telegram_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
import urlscrap, urlphoto
from aiogram.dispatcher.filters import Text

bot = Bot(telegram_token.TOKEN_API)
dp = Dispatcher(bot)

ikbp = InlineKeyboardMarkup(row_width=2)
ibp1 = InlineKeyboardButton(text='Некст пикча',
                            callback_data='nextp')
ibp2 = InlineKeyboardButton(text='Мейн меню',
                            callback_data='menu')
ikbp.add(ibp1, ibp2)

ikbv = InlineKeyboardMarkup(row_width=2)
ibv1 = InlineKeyboardButton(text='Некст видик',
                            callback_data='nextv')
ikbv.add(ibv1, ibp2)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/randpic')
b2 = KeyboardButton(text='/contacts')
b3 = KeyboardButton(text='/randvid')
b4 = KeyboardButton(text='TY<3')
kb.add(b1).insert(b3).add(b4, b2)


@dp.message_handler(commands=['randpic'])
async def get_picture(message: types.Message):
    url = urlphoto.take_purl()
    await bot.send_message(text='Все пикчи взяты с сервиса Unsplash, посредством API',
                           chat_id=message.chat.id,
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=message.chat.id,
                         photo=url['url'],
                         caption=f"Автор:{url['autor']}, Описание:{url['caption']}",
                         reply_markup=ikbp)


@dp.message_handler(Text(equals='TY<3'))
async def textcmd(message: types.Message):
    await message.answer(text='❤️')


@dp.message_handler(commands=['contacts'])
async def getcont(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='По поводу сотрудничества и всего прочего - @ded_sergiy')


@dp.message_handler(commands=['randvid'])
async def get_video(message: types.Message):
    vidurl = urlscrap.take_url()
    await bot.send_message(chat_id=message.chat.id,
                           text='Возможна жестямба, би карефулл пожалуйста',
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_video(chat_id=message.chat.id,
                         video=vidurl,
                         caption='Разработчик бота не несёт ответсвенность за контент, который найден ботом в открытом доступе',
                         reply_markup=ikbv)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Готов работать как ишак',
                           reply_markup=kb)


@dp.callback_query_handler()
async def callback_photo(callback: types.CallbackQuery):
    if callback.data == 'nextp':
        url = urlphoto.take_purl()
        await callback.message.edit_media(types.InputMedia(media=url['url'],
                                                           type='photo',
                                                           caption=f'Автор: {url["autor"]}, Описание: {url["caption"]}'),
                                          reply_markup=ikbp)
        await callback.answer('Загрузка может занять некоторое время...')
    elif callback.data == 'nextv':
        vidurl = urlscrap.take_url()
        await callback.message.edit_media(types.InputMedia(media=vidurl,
                                                           type='video',
                                                           caption='Разработчик бота не несёт ответсвенность за контент, который найден ботом в открытом доступе'),
                                          reply_markup=ikbv)
    elif callback.data == 'menu':
        await bot.send_message(chat_id=callback.message.chat.id,
                               reply_markup=kb,
                               text='Добро пожаловать в мейн меню')
        await callback.message.delete()
        await callback.answer(text='Успешный переход')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
