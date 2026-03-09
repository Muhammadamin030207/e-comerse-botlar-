from email import message
from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from databases.database import Database
from states.add_product import AddProductRegister
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters.filter import RoleFilter
from keyboars.inline import inline_product_options,inline_products,admin_start_inline_keyboard,cart_inline_keyboard
from states.update_product import UpdateProductState
router = Router()
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@router.callback_query(F.data == "products_admin")
async def show_products(callback: CallbackQuery, db):
    await callback.answer()
    products = await db.get_products()

    await callback.message.answer(
        text="📦 Mahsulotlar ro'yxati:",
        reply_markup=inline_products(products)
    )

@router.callback_query(F.data == "manage_products", RoleFilter("admin"))
async def manage_products(call: CallbackQuery, db: Database):
    await call.answer()

    products = await db.get_products()
    
    if not products:
        await call.message.answer("📦 Hozircha hech qanday mahsulot yo'q.")
        return



    for product in products:
        keyboard = inline_product_options(product["id"])
        text = f"📦 {product['name']}\n💰 Narxi: {product['price']} so'm\n📝 {product['description']}"
        await call.message.answer(text=text, reply_markup=keyboard) 

@router.callback_query(F.data == "products_user")
async def show_products(callback: CallbackQuery, db: Database):
    await callback.answer()
    products = await db.get_products()
    await callback.message.answer(
        text="📦 Mahsulotlar ro'yxati:",
        reply_markup=inline_products(products)
    )


@router.callback_query(F.data.startswith("product_"), RoleFilter("user"))
async def show_product(call: CallbackQuery, db: Database):
    await call.answer()
    product_id = int(call.data.split("_")[1])
    product = await db.get_product(product_id)

    text = f"📦 {product['name']}\n\n💰 Narxi: {product['price']} so'm\n\n📝 {product['description']}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Savatchaga qo'shish", callback_data=f"addcart_{product_id}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="products_user")]
        ]
    )

    await call.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("addcart_"), RoleFilter("user"))
async def add_to_cart(call: CallbackQuery, db: Database):
    product_id = int(call.data.split("_")[1])
    user_id = await db.get_user_id(call.from_user.id)
    await db.add_product_to_cart(user_id, product_id)
    await call.answer("✅ Mahsulot savatchaga qo'shildi 🗑")

# Savatcha
@router.callback_query(F.data == "cart_user", RoleFilter("user"))
async def view_cart(call: CallbackQuery, db: Database):
    user_id = await db.get_user_id(call.from_user.id)
    products = await db.get_cart_products(user_id)

    if not products:
        await call.message.answer("Savatda hech qanday mahsulot yo'q.")
        return

    await call.message.answer("Savatdagi mahsulotlar:", reply_markup=cart_inline_keyboard(products))
    await call.answer()


@router.callback_query(F.data.startswith("remove_"), RoleFilter("user"))
async def remove_from_cart(call: CallbackQuery, db: Database):
    product_id = int(call.data.split("_")[1])
    user_id = await db.get_user_id(call.from_user.id)
    await db.remove_product_from_cart(user_id, product_id)
    await call.message.answer("✅ Mahsulot savatchadan o'chirildi! 🗑")
    await call.answer()


@router.callback_query(F.data == "checkout", RoleFilter("user"))
async def checkout(call: CallbackQuery, db: Database):
    user_id = await db.get_user_id(call.from_user.id)
    order_id = await db.get_or_create_cart(user_id)
    await db.pool.execute("UPDATE orders SET order_status='pending' WHERE id=$1", order_id)

    
    await call.message.answer("✅ Buyurtmangiz qabul qilindi! 📦")

    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Bosh menyu", callback_data="start_inline")]
        ]
    )
    await call.message.answer("Bosh menyuga qaytish:", reply_markup=keyboard)

    await call.answer()


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


@router.callback_query(F.data.startswith("adminproduct_"), RoleFilter("admin"))
async def product(call: CallbackQuery):
    product_id = call.data.split("_")[1]
    await call.message.answer("Mahsulotni tahrirlash yoki o'chirish uchun quyidagi tugmalardan birini bosing:", reply_markup=inline_product_options(int(product_id)))
    await call.answer()

@router.callback_query(F.data.startswith("delete_product_"), RoleFilter("admin"))
async def product(call: CallbackQuery,db):
    product_id = call.data.split("_")[2]
    await db.delete_product(int(product_id))
    await call.message.answer("✅ Mahsulot muvaffaqiyatli o'chirildi!", reply_markup=admin_start_inline_keyboard())
    await call.answer()

@router.callback_query(F.data.startswith("edit_product_"), RoleFilter("admin"))
async def product(call: CallbackQuery,state : FSMContext):
    product_id = int(call.data.split("_")[2])
    await state.update_data(product_id=product_id)
    await call.message.answer("Mahsulot yangi nomini kiriting:")
    await state.set_state(UpdateProductState.name)

@router.message(StateFilter(UpdateProductState.name))
async def product(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("💰 Mahsulot yangi narxini kiriting (so'm da):")
    await state.set_state(UpdateProductState.price)

@router.message(StateFilter(UpdateProductState.price))
async def product(msg: Message, state: FSMContext):
    await state.update_data(price=int(msg.text))
    await msg.answer("Mahsulot yangi tasnifini kiriting:")
    await state.set_state(UpdateProductState.description)


@router.message(StateFilter(UpdateProductState.description))
async def product(msg: Message, state: FSMContext, db):
    await state.update_data(description=msg.text)
    data = await state.get_data()
    await db.update_product(
        data["product_id"],
        data["name"],
        data["price"],
        data["description"]
    )

    await msg.answer("✅ Mahsulot muvaffaqiyatli yangilandi 🎉",reply_markup=admin_start_inline_keyboard())
    await state.clear()

@router.callback_query(F.data.startswith("product_"), RoleFilter("user"))
async def add_to_cart(call: CallbackQuery, db,):
    product_id = call.data.split("_")[1]
    user_id = await db.get_user_id(call.from_user.id)
    await db.add_product_to_cart(user_id, int(product_id))
    await call.message.answer("✅ Mahsulot savatchaga qo'shildi 🗑")
    await call.answer("✅ Mahsulot savatchaga qo'shildi! 🗑")
    await call.answer()


@router.callback_query(F.data == "cart_user", RoleFilter("user"))
async def view_cart(call: CallbackQuery, db):
    user_id = await db.get_user_id(call.from_user.id)
    products = await db.get_cart_products(user_id)

    if not products:
        await call.message.answer("Savatda hech qanday mahsulot yo'q.")
        return

    await call.message.answer("Savatdagi mahsulotlar:", reply_markup=cart_inline_keyboard(products))
    await call.answer()

@router.callback_query(F.data.startswith("remove_"), RoleFilter("user"))
async def remove_from_cart(call: CallbackQuery, db):
    product_id = int(call.data.split("_")[1])
    user_id = await db.get_user_id(call.from_user.id)
    await db.remove_product_from_cart(user_id, product_id)
    await call.answer("✅ Mahsulot savatchadan o'chirildi! 🗑")
    await call.message.answer("✅ Mahsulot savatchadan o'chirildi! 🗑")
    await call.answer() 