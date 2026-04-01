from aiogram import Router, F
from aiogram.types import LabeledPrice

from config import PROVIDER_TOKEN
from db import add_vote

router = Router()


@router.callback_query(F.data.startswith("pay:"))
async def pay(callback):
    _, r, g, user = callback.data.split(":")

    prices = [LabeledPrice(label="Голос", amount=10)]

    await callback.message.answer_invoice(
        title="Платный голос",
        description="1 голос",
        provider_token=PROVIDER_TOKEN,
        currency="XTR",
        prices=prices,
        payload=f"{r}:{g}:{user}"
    )


@router.pre_checkout_query()
async def checkout(pre):
    await pre.answer(ok=True)


@router.message(F.successful_payment)
async def success(message):
    r, g, user = message.successful_payment.invoice_payload.split(":")
    add_vote(message.from_user.id, user, int(r), int(g), "paid")
    await message.answer("✅ Платный голос засчитан")