from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def register_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Ro'yxatdan o'tish", callback_data="register")],
        ]
    )

def confirm_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=" ✅ Tasdiqlash", callback_data="confirm"), InlineKeyboardButton(text=" 📝 Tahrirlash", callback_data="edit")]
        ]
    )

def start_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Profile", callback_data="profile_user"), InlineKeyboardButton(text="📦 Mahsulotlar", callback_data="products_user")],
            [InlineKeyboardButton(text="🛒 Mening Buyurtmalarim", callback_data="orders_user"), InlineKeyboardButton(text="🗑 Savatcha", callback_data="cart_user")],
        ]
    )

def admin_start_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Profile", callback_data="profile_admin"), InlineKeyboardButton(text="📦 Mahsulotlar", callback_data="products_admin")],
            [InlineKeyboardButton(text="🛒 Buyurtmalar", callback_data="orders_admin"), InlineKeyboardButton(text="⚙️ Admin Panel", callback_data="admin_panel")]
        ]
    )

def admin_panel_inline_keyboard():
    return InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕📦 Mahsulot qo'shish", callback_data="add_product")],
        [InlineKeyboardButton(text="🛠📋 Mahsulotlar (Admin)", callback_data="manage_products")],
        [InlineKeyboardButton(text="👥📊 Userlar", callback_data="manage_users")],
        [InlineKeyboardButton(text="🔙⬅️ Orqaga", callback_data="admin_start")]
    ]
    )

def users_inline(users):
    keyboard = []

    for user in users:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{user['full_name']} ({user['role']})",
                callback_data=f"user_{user['user_id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_panel")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def role_inline_keyboard(user_id):
    keyboard = [
        [
            InlineKeyboardButton(
                text="👑✨ Admin qilish",
                callback_data=f"set_role_{user_id}_admin"
            )
        ],
        [
            InlineKeyboardButton(
                text="👤⚡ User qilish",
                callback_data=f"set_role_{user_id}_user"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙⬅️ Orqaga",
                callback_data="manage_users"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def inline_products(products):
    keyboard=[]

    for product in products:
        keyboard.append([InlineKeyboardButton(
            text=f"{product['name']} - ({product['price']} so'm)",
            callback_data=f"product_{product['id']}"
        )])
    keyboard.append([InlineKeyboardButton(
        text="🔙 Orqaga",
        callback_data="start_inline"
    )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def inline_product_options(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"edit_product_{product_id}"),
                InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"delete_product_{product_id}")
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"admin_start")
            ]
        ]
    )
def cart_inline_keyboard(products):
    keyboard = []

    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} - ({product['price']} so'm)",
                callback_data=f'product_{product['id']}'),
            InlineKeyboardButton(
                text="❌ O'chirish",
                callback_data=f"remove_{product['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ Buyurtma berish",
            callback_data="checkout"
        ),
        InlineKeyboardButton(
            text="🔙 Orqaga",
            callback_data="start_inline"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)