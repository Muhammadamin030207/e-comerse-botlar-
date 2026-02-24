from aiogram.fsm.state import StatesGroup,State

class AddProductRegister(StatesGroup):
    name=State()
    price=State()
    description=State()