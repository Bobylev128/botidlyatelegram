from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import CreateBattle
from keyboards.admin_kb import admin_kb
from config import ADMIN_ID

router = Router()

@router.message(F.text == "/admin")
async def admin(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer("Админ панель", reply_markup=admin_kb())

@router.callback_query(F.data == "create")
async def create(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите лимит:")
    await state.set_state(CreateBattle.max_users)

@router.message(CreateBattle.max_users)
async def max_users(msg: Message, state: FSMContext):
    await state.update_data(max=int(msg.text))
    await msg.answer("Введите раунды (например 334):")
    await state.set_state(CreateBattle.rounds)