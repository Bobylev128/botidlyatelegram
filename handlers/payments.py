from aiogram import Router
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message
from db import add_vote

router = Router()


async def send_invoice(bot, user_id, r, g, user):
    await bot.send_invoice(
        chat_id=user_id,
        title="Голос",
        description=f"Голос за {user}",
        payload=f"{r}:{g}:{user}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Голос", amount=10)]
    )


@router.pre_checkout_query()
async def pre_checkout(q: PreCheckoutQuery):
    await q.answer(ok=True)


@router.message(lambda m: m.successful_payment)
async def success(message: Message):
    r, g, user = message.successful_payment.invoice_payload.split(":")
    add_vote(message.from_user.id, user, int(r), int(g), "paid")
    await message.answer("✅ Оплачено")