from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
import aiosqlite

router = Router()

@router.callback_query(F.data.startswith("vote_paid"))
async def paid(call: CallbackQuery):
    _, gid, user = call.data.split(":")

    await call.bot.send_invoice(
        call.from_user.id,
        title="💸 Голос",
        description="Платный голос",
        payload=f"{gid}:{user}",
        provider_token="",
        currency="XTR",
        prices=[{"label": "Голос", "amount": 10}]
    )

@router.message(F.successful_payment)
async def success(msg: Message):
    gid, user = msg.successful_payment.invoice_payload.split(":")

    async with aiosqlite.connect("battle.db") as db:
        await db.execute(
            "INSERT INTO votes VALUES (?, ?, ?, ?, 'paid')",
            (msg.from_user.id, msg.from_user.username, gid, user)
        )
        await db.commit()

    await msg.answer("💸 Голос засчитан")