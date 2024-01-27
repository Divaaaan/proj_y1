from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from contextlib import suppress

from typing import Optional

from FCM import where_user

from read_numers_of_members import push_data, push_balance, get_names_of_exact_actions

router = Router()

user_data = {}


class APLCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[str] = None


@router.message(where_user.have_access, Command("make_application"))
async def cmd_start_application(message: Message, state: FSMContext):
    await go_to_start(message)


async def go_to_start(message: types.Message):
    user_data[message.from_user.id] = ['', '', '', '', '']
    await message.answer(
        text=f'Выбирать пункты можно в любом порядке,\nкнопка отмены стирает все поля,\n'
             f'поменять поле можно введя его еще раз\n'
             f'Тип: \n'
             f'Сумма: \n'
             f'Описание: \n', reply_markup=make_apl(False))


@router.callback_query(APLCallbackFactory.filter(F.action == "change"))
async def callbacks_change(callback: types.CallbackQuery, callback_data: APLCallbackFactory, state: FSMContext):
    if callback_data.value == 'категория':
        await update_type_text(callback.message)
    elif callback_data.value == 'сумма':
        await update_sum_text(callback.message, state)
    elif callback_data.value == 'описание':
        await update_extra_text(callback.message, state)
    elif callback_data.value == 'тип':
        await update_category_text(callback.message)
    await callback.answer()


@router.callback_query(APLCallbackFactory.filter(F.action == "choice"))
async def callbacks_change(callback: types.CallbackQuery, callback_data: APLCallbackFactory):
    if callback_data.value == 'Поступление':
        user_data[callback.message.chat.id][0] = callback_data.value
        await update_text(callback.message)
    elif callback_data.value == 'Выбытие':
        user_data[callback.message.chat.id][0] = callback_data.value
        await update_text(callback.message)
    await callback.answer(None)


@router.callback_query(APLCallbackFactory.filter(F.action == "type"))
async def callbacks_change(callback: types.CallbackQuery, callback_data: APLCallbackFactory):
    list = get_names_of_exact_actions(user_data[callback.message.chat.id][0])
    user_data[callback.message.chat.id][3] = list[int(callback_data.value)]
    await update_text(callback.message)
    await callback.answer(None)


@router.callback_query(APLCallbackFactory.filter(F.action == "cancel"))
async def callbacks_change(callback: types.CallbackQuery, callback_data: APLCallbackFactory):
    user_data[callback.message.chat.id] = ['', '', '', '', '']
    await update_text(callback.message)
    await callback.answer(text='Запрос отменен, вы можете заполнить поля еще раз', show_alert=True)


@router.callback_query(APLCallbackFactory.filter(F.action == "done"))
async def callbacks_change(callback: types.CallbackQuery, callback_data: APLCallbackFactory):
    if user_data[callback.message.chat.id][0] == '' or user_data[callback.message.chat.id][1] == '':
        await update_text(callback.message, f=True)
        await callback.answer(None)
    print(user_data)
    ans = push_data(user_data[callback.message.chat.id])
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f'Транзакция записана \n'
                                         f'Расчетный остаток {ans}')
    await callback.answer(None)


async def update_category_text(message: types.Message):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Выберите тип: ",
            reply_markup=make_choice())


async def update_type_text(message: types.Message):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Категория: ", reply_markup=make_type(message.chat.id))


async def update_sum_text(message: types.Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Введите сумму :")
        await state.set_state(where_user.take_sum)


@router.message(where_user.take_sum, F.text)
async def sum(message: types.Message, state: FSMContext):
    await state.set_state(where_user.have_access)
    user_data[message.from_user.id][1] = float(message.text.replace(',', '.'))
    await make_text(message)


async def update_extra_text(message: types.Message, state: FSMContext):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Введите описание:")
        await state.set_state(where_user.take_extra)


@router.message(F.text, where_user.take_extra)
async def extra(message: types.Message, state: FSMContext):
    user_data[message.from_user.id][2] = message.text
    await make_text(message)
    await state.set_state(where_user.have_access)


async def make_text(message: types.Message):
    await message.answer(
        f"Выбирать пункты можно в любом порядке,\nкнопка отмены стирает все поля,\n"
        f"Изменить содержание поля можно введя данные еще раз\n"
        f"Тип: {user_data[message.chat.id][0]} \n"
        f"Категория: {user_data[message.chat.id][3]} \n"
        f"Сумма: {user_data[message.chat.id][1]} \n"
        f"Описание: {user_data[message.chat.id][2]} \n",
        reply_markup=make_apl(False if user_data[message.chat.id][0] == '' else True))


async def update_text(message: types.Message, f=False):
    print(user_data[message.chat.id])
    if f:
        with suppress(TelegramBadRequest):
            await message.edit_text(
                f"Вы не ввели поле суммы или категории, без них отправка невозможна\n"
                f"Выбирать пункты можно в любом порядке,\nкнопка отмены стирает все поля,\n"
                f"Изменить содержание поля можно введя данные еще раз\n"
                f"Тип: {user_data[message.chat.id][0]} \n"
                f"Категория: {user_data[message.chat.id][3]} \n"
                f"Сумма: {user_data[message.chat.id][1]} \n"
                f"Описание: {user_data[message.chat.id][2]} \n",
                reply_markup=make_apl(False if user_data[message.chat.id][0] == '' else True))
    else:
        with suppress(TelegramBadRequest):
            await message.edit_text(
                f"Выбирать пункты можно в любом порядке,\nкнопка отмены стирает все поля,\n"
                f"Изменить содержание поля можно введя данные еще раз\n"
                f"Тип: {user_data[message.chat.id][0]} \n"
                f"Категория: {user_data[message.chat.id][3]} \n"
                f"Сумма: {user_data[message.chat.id][1]} \n"
                f"Описание: {user_data[message.chat.id][2]} \n",
                reply_markup=make_apl(False if user_data[message.chat.id][0] == '' else True))


def make_apl(flag):
    builder = InlineKeyboardBuilder()
    builder.button(text="Тип", callback_data=APLCallbackFactory(action="change", value='тип'))
    if flag:
        builder.button(text="Категория", callback_data=APLCallbackFactory(action="change", value='категория'))
    builder.button(text="Ввести сумму", callback_data=APLCallbackFactory(action="change", value='сумма'))
    builder.button(text="Добавить описание", callback_data=APLCallbackFactory(action="change", value='описание'))
    builder.button(text="Отменить ❌", callback_data=APLCallbackFactory(action="cancel"))
    builder.button(text="Отправить ✅", callback_data=APLCallbackFactory(action="done"))
    builder.adjust(1)
    return builder.as_markup()


def make_choice():
    builder = InlineKeyboardBuilder()
    builder.button(text="Поступление", callback_data=APLCallbackFactory(action="choice", value='Поступление'))
    builder.button(text="Выбытие", callback_data=APLCallbackFactory(action="choice", value='Выбытие'))
    builder.adjust(2)
    return builder.as_markup()


def make_type(id):
    builder = InlineKeyboardBuilder()
    list = get_names_of_exact_actions(user_data[id][0])
    for i in range(len(list)):
        builder.button(text=f'{list[i]}', callback_data=APLCallbackFactory(action='type', value=f'{i}'))
    builder.adjust(1)
    return builder.as_markup()


@router.callback_query(APLCallbackFactory.filter(F.action == "action"))
async def have_action(callback: types.CallbackQuery, callback_data: APLCallbackFactory):
    user_data[callback.message.chat.id][4] = callback_data.value
    await update_type_text(callback.message)
    await callback.answer(None)


# ---------------------------------------------------------------------------------------------

@router.message(where_user.have_access, Command("add_actual_balance"))
async def add_actual_balance(message: Message):
    user_data[message.chat.id] = ['', '']
    await message.answer(
        f"Дата: {user_data[message.chat.id][1]} \n"
        f"Фактический остаток: {user_data[message.chat.id][0]} \n",
        reply_markup=balance())


async def update_balance(message: types.Message, f=False):
    if f:
        with suppress(TelegramBadRequest):
            await message.answer(
                f"Вы не ввели поле суммы или категории, без них отправка невозможна"
                f"Дата: {user_data[message.chat.id][1]} \n"
                f"Фактический остаток: {user_data[message.chat.id][0]} \n",
                reply_markup=balance())
    else:
        with suppress(TelegramBadRequest):
            await message.answer(
                f"Дата: {user_data[message.chat.id][1]} \n"
                f"Фактический остаток: {user_data[message.chat.id][0]} \n",
                reply_markup=balance())


def balance():
    builder = InlineKeyboardBuilder()
    builder.button(text="Дата", callback_data=APLCallbackFactory(action="add", value='date'))
    builder.button(text="Сумма", callback_data=APLCallbackFactory(action="add", value='sum'))
    builder.button(text="Отправить", callback_data=APLCallbackFactory(action="add", value='done'))
    builder.adjust(2)
    return builder.as_markup()


@router.callback_query(APLCallbackFactory.filter(F.action == "add"))
async def get_sum(callback: types.CallbackQuery, callback_data: APLCallbackFactory, state: FSMContext):
    if callback_data.value == 'date':
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f"Введите дату сумму в формте ДД.ММ.ГГГГ:")
            await state.set_state(where_user.add_date)
    elif callback_data.value == 'sum':
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f"Введите остаток по расчетному счету:")
            await state.set_state(where_user.add_sum)
    elif callback_data.value == 'done':
        if user_data[callback.message.chat.id][0] == '' or user_data[callback.message.chat.id][1] == '':
            await update_balance(callback.message, f=True)
            await callback.answer(None)
            return
        ans = push_balance(user_data[callback.message.chat.id][1], user_data[callback.message.chat.id][0])
        if ans:
            await callback.message.edit_text(
                f"Отправлено")
        else:
            await callback.message.edit_text(
                f"Данной даты нет таблице, отправьте запрос еще раз")
    await callback.answer(None)


@router.message(F.text, where_user.add_date)
async def extra(message: types.Message, state: FSMContext):
    user_data[message.from_user.id][1] = message.text
    await state.set_state(where_user.have_access)
    await update_balance(message)


@router.message(F.text, where_user.add_sum)
async def extra(message: types.Message, state: FSMContext):
    user_data[message.from_user.id][0] = message.text
    await state.set_state(where_user.have_access)
    await update_balance(message)
