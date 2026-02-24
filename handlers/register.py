from email import message
from aiogram.types import Message,CallbackQuery
from aiogram import Bot,F,Router
from config import config
from aiogram.fsm.context import FSMContext
from states.register import RegisterState
from keyboars.inline import  confirm_inline_keyboard
from keyboars.reply import contact_keyboard 
from databases.database import Database

db= Database()
bot = Bot(token=config.BOT_TOKEN)
ADMIN_ID=7602386575
router = Router()

@router.message(RegisterState.full_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(RegisterState.age)

@router.message(RegisterState.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Yosh raqam bo'lishi kerak!")
    elif int(message.text) <= 15:
        await message.answer("Siz 15 yoshdan katta bo'lishingiz kerak!")
        return

    await state.update_data(age=message.text)
    await message.answer("Gmail manzilingizni kiriting:")
    await state.set_state(RegisterState.email)

@router.message(RegisterState.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(
        "Kontaktni tugma orqali yuboring:",
        reply_markup=contact_keyboard()
    )
    await state.set_state(RegisterState.phone)

@router.message(RegisterState.phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Kontaktni faqat tugma orqali yuboring!")
        return

    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()

    text = (
        "Ma'lumotlaringizni tekshiring:\n\n"
        f"Ism: {data['full_name']}\n"
        f"Yosh: {data['age']}\n"
        f"Gmail: {data['email']}\n"
        f"Telefon: {data['phone']}"
    )

    await message.answer(text, reply_markup=confirm_inline_keyboard())
    await state.set_state(RegisterState.confim)

@router.callback_query(RegisterState.confim, F.data)
async def confirm_handler(call: CallbackQuery, state: FSMContext,db):
    data = await state.get_data()

    if call.data == "confirm":
        data = await state.get_data()
        await bot.send_message(chat_id=ADMIN_ID,text=(f"""Yangi foydalanuvchi ro'yxatdan o'tdi:
        Ism: {data['full_name']}
        Yosh: {data['age']}
        Gmail: {data['email']}
        Telefon: {data['phone']}"""))

        user_id = call.from_user.id
        full_name = data['full_name']
        age = data['age']
        email = data['email']
        contact = data['phone']
        await db.add_user(user_id, full_name, age, email, contact)
        await call.message.answer("Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! Endi siz bizning botimizdan foydalanishingiz mumkin.")

    elif call.data == "edit":
        await call.message.answer("Qayta kiriting.\nIsm familiyangizni yozing:")
        await state.set_state(RegisterState.full_name)

    else:
        await message.answer("Tugmalardan foydalaning")
