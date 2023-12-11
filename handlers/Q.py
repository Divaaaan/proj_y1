from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State


from keyboards.for_questions import login

from FCM import where_user

from read_numers_of_members import get_number, add_id, get_name_from_file

router = Router()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Пж авторизируйся",
        reply_markup=login()
    )
    await state.set_state(where_user.make_access)


@router.message(where_user.have_access, Command("start"))
async def cmd_alrd_start(message: Message):
    await message.answer('Вы уже авторизировались')


@router.message(F.contact, where_user.make_access)
async def on_user_shared(message: types.contact, state: FSMContext):
    list_of_good_num = get_number()
    if message.contact.user_id == message.from_user.id and (
            message.contact.phone_number in list_of_good_num or str(message.contact.phone_number)[
                                                                1:] in list_of_good_num):
        await message.answer(
            f"Привет, {message.from_user.first_name}!",
            reply_markup=ReplyKeyboardRemove())
        await state.set_state(where_user.have_access)
        if message.contact.phone_number[0] == '+':
            add_id(message.contact.phone_number[1:], message.from_user.id)
        else:
            add_id(message.contact.phone_number, message.from_user.id)
        # sub_user.add(user_data(message.from_user.id, get_name_from_file(message.from_user.id)))
        # при использовании доп массива данных
    else:
        await message.answer(
            f"Нет доступа, обратитесь к разработчику")
