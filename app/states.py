from aiogram.fsm.state import StatesGroup, State

class Parsing(StatesGroup):
    wait_products_count = State()

class GetAttendants(StatesGroup):
    wait = State()