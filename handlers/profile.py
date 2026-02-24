from aiogram import Router
from aiogram.types import Message, CallbackQuery
from keyboars.inline import start_inline_keyboard
from databases.database import Database

router = Router()

@router.callback_query(lambda c: c.data == "profile")
async def profile_command_handler(call: CallbackQuery, db: Database):
    user_id = call.from_user.id
    user = await db.user_profile(user_id)

    if user:
        await call.message.answer(
            f"Profile ma'lumotlaringiz:\n"
            f"Ism: {user['full_name']}\n"
            f"Yosh: {user['age']}\n"
            f"Email: {user['email']}\n"
            f"Kontakt: {user['contact']}",
            reply_markup=start_inline_keyboard()
        )
    else:
        await call.message.answer("Sizning profilingiz topilmadi.")
    await call.answer()