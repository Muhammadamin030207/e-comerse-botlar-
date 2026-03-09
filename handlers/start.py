from aiogram import Router,F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from filters.filter import RoleFilter
from keyboars.inline import start_inline_keyboard,register_inline_keyboard,admin_start_inline_keyboard
from aiogram.fsm.context import FSMContext
from states.register import RegisterState
from databases.database import Database
router = Router()

@router.message(CommandStart(),RoleFilter("admin"))
async def admin_start(msg: Message):
    await msg.answer("Admin panelga xush kelibsiz!",reply_markup=admin_start_inline_keyboard())

@router.message(CommandStart())
async def start_command_handler(msg: Message, db: Database):
    user_id = msg.from_user.id
    user = await db.check_user(user_id)

    if not user:
        await msg.answer(
            f"Assalomu alaykum!\n"
            f"{msg.from_user.full_name}!\n"
            f"Smart Shop botiga xush kelibsiz! 😊"
            f"Botimizdan foydalanish uchun ro'yxatdan o'ting:",
            reply_markup=register_inline_keyboard()
        )
    else:
        await msg.answer(
            f"Assalomu Alaykum {msg.from_user.full_name}, "
            f"Smart Shop botiga xush kelibsiz! 😊"
            f"Botimizdan foydalanishingiz mumkin!",
            reply_markup=start_inline_keyboard()
        )
@router.callback_query(lambda c: c.data == "register")
async def start_register_callback(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ism va familiyangizni kiriting:")
    await state.set_state(RegisterState.full_name)
    await call.answer()


@router.callback_query(F.data == "start_inline", RoleFilter("user"))
async def back_to_start(call: CallbackQuery):
    await call.message.edit_text(
        "🏠 Asosiy menyu",
        reply_markup=start_inline_keyboard()
    )

@router.callback_query(F.data == "start_inline", RoleFilter("admin"))
async def back_to_start(call: CallbackQuery):
    await call.message.edit_text(
        "🏠 Asosiy menyu",
        reply_markup=admin_start_inline_keyboard()
    )