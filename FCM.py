from aiogram.fsm.state import StatesGroup, State
class where_user(StatesGroup):
    make_access = State()
    have_access = State()
    take_sum = State()
    take_balance = State()
    add_date = State()
    add_text = State()
    add_sum = State()
    take_extra = State()
