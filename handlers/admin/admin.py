from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from filters.filter import RoleFilter
from keyboars.inline import admin_panel_inline_keyboard,users_inline,role_inline_keyboard,start_inline_keyboard,admin_start_inline_keyboard

router = Router()

@router.callback_query(F.data == "admin_panel",RoleFilter("admin"))
async def admin_panel(call: CallbackQuery):
    await call.message.answer("Admin panelga xush kelibsiz!",reply_markup=admin_panel_inline_keyboard())


@router.callback_query(F.data == "manage_users",RoleFilter("admin"))
async def manage_users(call: CallbackQuery,db):
    users = await db.get_users()

    if not users:
        await call.message.answer("Userlar yo'q",reply_markup=admin_panel_inline_keyboard())
        return

    await call.message.answer(
        "👥📊 Userlar ro'yxati:",
        reply_markup=users_inline(users)
    )

@router.callback_query(F.data.startswith("user_"),RoleFilter("admin"))
async def choose_role(callback: CallbackQuery,db):
    user_id = callback.data.split("_")[1]
    await callback.message.answer(
        f"👤 Role tanlang:",
        reply_markup=role_inline_keyboard(user_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("set_role_"),RoleFilter("admin"))
async def set_role(callback: CallbackQuery, db):
    _, _, user_id,role = callback.data.split("_")
    await db.set_user_role(
        user_id=int(user_id), role=role)
    await callback.answer()

    await callback.message.answer(
        f"✅ Userning roli '{role}' ga o'zgartirildi.",
        reply_markup=admin_panel_inline_keyboard()
    )
    await callback.answer("Rol o'zgartirildi.")
    await callback.answer()


@router.callback_query(F.data=="admin_start", RoleFilter("admin"))
async def admin_start_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "👤 Admin panelga xush kelibsiz!",
        reply_markup=admin_start_inline_keyboard()
    )

@router.callback_query(F.data == "profile_user")
async def profile_user(call: CallbackQuery, db):
    user_id = call.from_user.id
    profile = await db.user_profile(user_id)
    text = f"👤 Profile:\n\nIsm: {profile['full_name']}\nYosh: {profile['age']}\nEmail: {profile['email']}\nKontakt: {profile['contact']}"
    await call.message.edit_text(text, reply_markup=start_inline_keyboard())

@router.callback_query(lambda c: c.data == "start_user", RoleFilter("admin"))
async def start_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "👤 Admin panelga xush kelibsiz!",
        reply_markup=start_inline_keyboard()
    )
@router.callback_query(F.data == "profile_admin", RoleFilter("admin"))
async def profile_admin(call: CallbackQuery, db):
    user_id = call.from_user.id
    profile = await db.user_profile(user_id)
    text = f"👤 Admin Profile:\n\nIsm: {profile['full_name']}\nYosh: {profile['age']}\nEmail: {profile['email']}\nKontakt: {profile['contact']}"
    await call.message.edit_text(text, reply_markup=admin_start_inline_keyboard())
    