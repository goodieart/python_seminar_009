from random import randint as rand
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
chat_id = ''
TOKEN = '5505836319:AAFIQ0x1PVZu8HMebi6VBGEgqNM7K87dnZI'

sweets = 117
player = {'id': 'Игрок 1', 'score': 0}
cpu = {'id': 'Игрок 2', 'score': 0}

first_player = player
turn = player

running = True

bot = None
dp = None

def tg_init():
    global turn, running, bot, dp
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        await message.reply(f"Есть {sweets} конфет. Сколько хочешь взять?")
    
    @dp.message_handler()
    async def echo(message: types.Message):
        if player_turn(int(message.text)) == 0:
            next_turn()
            await message.answer(f'{turn["id"]} взял {make_turn()} конфет\nОсталось {sweets} конфет')
            if check_winner():
                await message.answer(f'{turn["id"]} победил со счетом {turn["score"]}!')
            next_turn()
        else:
            await message.answer('Нельзя взять столько конфет!')
    executor.start_polling(dp, skip_updates=True)


def random_turn():
    return rand(1, 28)


def make_turn():
    global sweets, turn
    grab = 0
    if turn['id'] == 'Игрок 2':
        if sweets > 28:
            grab = random_turn()
            sweets -= grab
            turn['score'] += grab
        else:
            grab = sweets
            sweets = 0
            turn['score'] += grab
    return grab


def next_turn():
    global turn, player, cpu
    turn = player if turn == cpu else cpu


def player_turn(count: int):
    global sweets
    if count > sweets or count > 28:
        return 1
    else:
        sweets -= count
        turn['score'] += count
        return 0

def set_first_player():
    global cpu, player, first_player
    r = rand(0, 1)
    if r == 1:
        first_player = cpu
    return f'{f"Игрок 2" if first_player == cpu else "Игрок 1"}'


def check_winner():
    global player
    global cpu
    if sweets == 0: return True
    return False

