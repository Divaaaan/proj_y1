from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from keyboards.for_questions import login

from FCM import where_user

router = Router()


@router.message(where_user.have_access, Command("make_application"))
async def cmd_start_application(message: Message, state: FSMContext):
    await message.answer('hi')
