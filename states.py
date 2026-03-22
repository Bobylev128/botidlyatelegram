from aiogram.fsm.state import StatesGroup, State

class CreateBattle(StatesGroup):
    max_users = State()
    rounds = State()
    prizes = State()