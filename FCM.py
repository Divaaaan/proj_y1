from aiogram.fsm.state import StatesGroup, State
class where_user(StatesGroup):
    make_access = State()
    have_access = State()
    take_sum = State()
