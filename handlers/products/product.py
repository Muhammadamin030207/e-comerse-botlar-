from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from keyboars.inline import inline_products
from states.add_product import AddProductRegister
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

router = Router()






@router.callback_query(F.data == "products_admin")
async def show_products(callback: CallbackQuery, db):
    await callback.answer()
    products = await db.get_products()

    await callback.message.answer(
        text="📦 Mahsulotlar ro'yxati:",
        reply_markup=inline_products(products)
    )



@router.callback_query(F.data == "products_user")
async def show_products(callback: CallbackQuery, db):
    await callback.answer()
    products = await db.get_products()

    await callback.message.answer(
        text="📦 Mahsulotlar ro'yxati:",
        reply_markup=inline_products(products)
    )

@router.callback_query(F.data == "add_product")
async def add_product_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("📦 Mahsulot nomini kiriting:")
    await state.set_state(AddProductRegister.name)



@router.message(StateFilter(AddProductRegister.name))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Mahsulot narxini kiriting (so'm da):")
    await state.set_state(AddProductRegister.price)



@router.message(StateFilter(AddProductRegister.price))
async def process_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Narx faqat son bo‘lishi kerak!")
        return

    await state.update_data(price=int(message.text))
    await message.answer("📝 Mahsulot tasnifini kiriting:")
    await state.set_state(AddProductRegister.description)


@router.message(StateFilter(AddProductRegister.description))
async def process_description(message: Message, state: FSMContext, db):
    await state.update_data(description=message.text)
    data = await state.get_data()

    await db.add_product(
        data["name"],
        data["price"],
        data["description"]
    )

    await message.answer("✅ Mahsulot muvaffaqiyatli qo‘shildi 🎉")
    await state.clear()