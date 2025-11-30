import logging
import random

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================= НАСТРОЙКИ =================

TOKEN = "8201349641:AAGls32JyAgqlt3uHiZcl2TVOMiO7uz0eHA"
CARDS_FOLDER = "cards"   # папка с картинками

# СПИСОК ВСЕХ КАРТ (Ваши реальные имена файлов!)
CARDS = [
    {"name_ru": "3 Мушкетёра", "file": "3M"},
    {"name_ru": "Королева лучниц", "file": "ArcherQueen"},
    {"name_ru": "Лучницы", "file": "Archers"},
    {"name_ru": "Стрелы", "file": "Arrows"},
    {"name_ru": "Малыш-дракон", "file": "BabyD"},
    {"name_ru": "Шар", "file": "Balloon"},
    {"name_ru": "Бандитка", "file": "Bandit"},
    {"name_ru": "Бочка с варварами", "file": "BarbBarrel"},
    {"name_ru": "Хижина варваров", "file": "BarbHut"},
    {"name_ru": "Варвары", "file": "Barbs"},
    {"name_ru": "Бочка", "file": "Barrel"},
    {"name_ru": "Летучие мыши", "file": "Bats"},
    {"name_ru": "Боевой лекарь", "file": "BattleHealer"},
    {"name_ru": "Берсерк", "file": "Berserker"},
    {"name_ru": "Бомбер", "file": "Bomber"},
    {"name_ru": "Башня-бомбардир", "file": "BombTower"},
    {"name_ru": "Бандит-босс", "file": "BossBandit"},
    {"name_ru": "Камнемёт", "file": "Bowler"},
    {"name_ru": "Пушка", "file": "Cannon"},
    {"name_ru": "Пушка на колёсах", "file": "CannonCart"},
    {"name_ru": "Клон", "file": "Clone"},
    {"name_ru": "Тёмный принц", "file": "DarkPrince"},
    {"name_ru": "Копейщик-гоблин", "file": "DartGob"},
    {"name_ru": "Землетрясение", "file": "Earthquake"},
    {"name_ru": "Элитные варвары", "file": "eBarbs"},
    {"name_ru": "Электродракон", "file": "eDragon"},
    {"name_ru": "Электрический гигант", "file": "ElectroGiant"},
    {"name_ru": "Электродух", "file": "ElectroSpirit"},
    {"name_ru": "Эликсирный голем", "file": "ElixirGolem"},
    {"name_ru": "Электромаг", "file": "eWiz"},
    {"name_ru": "Палач", "file": "Exe"},
    {"name_ru": "Огненный шар", "file": "Fireball"},
    {"name_ru": "Огненная колдунья", "file": "Firecracker"},
    {"name_ru": "Огненный дух", "file": "FireSpirit"},
    {"name_ru": "Рыбак", "file": "Fisherman"},
    {"name_ru": "Летающая машина", "file": "FlyingMachine"},
    {"name_ru": "Ледяная буря", "file": "Freeze"},
    {"name_ru": "Печь", "file": "Furnace"},
    {"name_ru": "Призрак", "file": "Ghost"},
    {"name_ru": "Гигант", "file": "Giant"},
    {"name_ru": "Гигантский скелет", "file": "GiantSkelly"},
    {"name_ru": "Банда гоблинов", "file": "GobGang"},
    {"name_ru": "Гоблинский гигант", "file": "GobGiant"},
    {"name_ru": "Хижина гоблинов", "file": "GobHut"},
    {"name_ru": "Гоблинская клетка", "file": "GoblinCage"},
    {"name_ru": "Гоблинское проклятие", "file": "GoblinCurse"},
    {"name_ru": "Гоблин-подрывник", "file": "GoblinDemolisher"},
    {"name_ru": "Сверлящий гоблин", "file": "GoblinDrill"},
    {"name_ru": "Гоблинская машина", "file": "GoblinMachine"},
    {"name_ru": "Гоблинштейн", "file": "Goblinstein"},
    {"name_ru": "Гоблины", "file": "Gobs"},
    {"name_ru": "Золотой рыцарь", "file": "GoldenKnight"},
    {"name_ru": "Голем", "file": "Golem"},
    {"name_ru": "Кладбище", "file": "Graveyard"},
    {"name_ru": "Стражи", "file": "Guards"},
    {"name_ru": "Дух исцеления", "file": "HealSpirit"},
    {"name_ru": "Хог", "file": "Hog"},
    {"name_ru": "Орда миньонов", "file": "Horde"},
    {"name_ru": "Охотник", "file": "Hunter"},
    {"name_ru": "Ледяной голем", "file": "IceGolem"},
    {"name_ru": "Ледяной дух", "file": "IceSpirit"},
    {"name_ru": "Ледяной маг", "file": "IceWiz"},
    {"name_ru": "Адская башня", "file": "Inferno"},
    {"name_ru": "Инферно-дракон", "file": "InfernoD"},
    {"name_ru": "Рыцарь", "file": "Knight"},
    {"name_ru": "Лавовый гонщик", "file": "Lava"},
    {"name_ru": "Молния", "file": "Lightning"},
    {"name_ru": "Маленький принц", "file": "LittlePrince"},
    {"name_ru": "Бревно", "file": "Log"},
    {"name_ru": "Дровосек", "file": "Lumber"},
    {"name_ru": "Магический лучник", "file": "MagicArcher"},
    {"name_ru": "Мега-рыцарь", "file": "MegaKnight"},
    {"name_ru": "Могучий шахтёр", "file": "MightyMiner"},
    {"name_ru": "Миньоны", "file": "Minions"},
    {"name_ru": "Зеркало", "file": "Mirror"},
    {"name_ru": "Мега-миньон", "file": "MM"},
    {"name_ru": "Монах", "file": "Monk"},
    {"name_ru": "Мортира", "file": "Mortar"},
    {"name_ru": "Мать-ведьма", "file": "MotherWitch"},
    {"name_ru": "Шахтёр", "file": "Miner"},
    {"name_ru": "Мушкетёр", "file": "Musk"},
    {"name_ru": "Ночная ведьма", "file": "NightWitch"},
    {"name_ru": "П.Е.К.К.А", "file": "PEKKA"},
    {"name_ru": "Феникс", "file": "Phoenix"},
    {"name_ru": "Яд", "file": "Poison"},
    {"name_ru": "Принц", "file": "Prince"},
    {"name_ru": "Принцесса", "file": "Princess"},
    {"name_ru": "Коллектор эликсира", "file": "Pump"},
    {"name_ru": "Ярость", "file": "Rage"},
    {"name_ru": "Таран", "file": "Ram"},
    {"name_ru": "Всадник на баране", "file": "RamRider"},
    {"name_ru": "Раздолбайки", "file": "Rascals"},
    {"name_ru": "Королевский гигант", "file": "RG"},
    {"name_ru": "Ракета", "file": "Rocket"},
    {"name_ru": "Королевская доставка", "file": "RoyalDelivery"},
    {"name_ru": "Королевские кабаны", "file": "RoyalHogs"},
    {"name_ru": "Королевские рекруты", "file": "RoyalRecruits"},
    {"name_ru": "Руно-гигант", "file": "RuneGiant"},
    {"name_ru": "Скелетная армия", "file": "Skarmy"},
    {"name_ru": "Скелетные драконы", "file": "SkeletonDragons"},
    {"name_ru": "Король скелетов", "file": "SkeletonKing"},
    {"name_ru": "Скелетики", "file": "Skellies"},
    {"name_ru": "Скелетная бочка", "file": "SkellyBarrel"},
    {"name_ru": "Снежок", "file": "Snowball"},
    {"name_ru": "Спарки", "file": "Sparky"},
    {"name_ru": "Копейщики-гоблины", "file": "SpearGobs"},
    {"name_ru": "Императрица духов", "file": "SpiritEmpress"},
    {"name_ru": "Подозрительный куст", "file": "SuspiciousBush"},
    {"name_ru": "Тесла", "file": "Tesla"},
    {"name_ru": "Могила", "file": "Tombstone"},
    {"name_ru": "Торнадо", "file": "Tornado"},
    {"name_ru": "Валькирия", "file": "Valk"},
    {"name_ru": "Лозы", "file": "Vines"},
    {"name_ru": "Пустота", "file": "Void"},
    {"name_ru": "Камнеплюи", "file": "WallBreakers"},
    {"name_ru": "Ведьма", "file": "Witch"},
    {"name_ru": "Колдун", "file": "Wiz"},
    {"name_ru": "Арбалет", "file": "XBow"},
    {"name_ru": "Разряд", "file": "Zap"},
    {"name_ru": "Заппы", "file": "Zappies"},
]

# логирование
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ================= ЛОГИКА ШПИОНОВ =================

def choose_spies_count(players: int) -> int:
    probs = {1: 0.96, 2: 0.03, 3: 0.01}
    max_spies = min(players - 1, 3)
    filtered = {k: v for k, v in probs.items() if k <= max_spies}

    s = sum(filtered.values())
    for k in filtered:
        filtered[k] /= s

    rnd = random.random()
    cum = 0
    for k, p in filtered.items():
        cum += p
        if rnd <= cum:
            return k
    return 1


# ================= ХЕНДЛЕРЫ =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data.clear()

    keyboard = [
        [InlineKeyboardButton("3", callback_data="players_3"),
         InlineKeyboardButton("4", callback_data="players_4"),
         InlineKeyboardButton("5", callback_data="players_5")],
        [InlineKeyboardButton("6", callback_data="players_6"),
         InlineKeyboardButton("7", callback_data="players_7"),
         InlineKeyboardButton("8", callback_data="players_8")],
    ]

    await update.message.reply_text(
        "Выберите количество игроков:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def players_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    players = int(query.data.split("_")[1])
    spies = choose_spies_count(players)
    roles = ["spy"] * spies + ["citizen"] * (players - spies)
    random.shuffle(roles)

    # ВАЖНО: карта выбирается случайно один раз
    chosen_card = random.choice(CARDS)

    context.chat_data["players"] = players
    context.chat_data["roles"] = roles
    context.chat_data["card"] = chosen_card
    context.chat_data["index"] = 0

    await query.edit_message_text(
        text=f"Игроков: {players}\nШпионов: {spies}\n\nТелефон у Игрока 1.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Показать роль Игрока 1", callback_data="show")]]
        )
    )


async def show_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    roles = context.chat_data["roles"]
    card = context.chat_data["card"]
    idx = context.chat_data["index"]
    player = idx + 1

    role = roles[idx]

    if role == "spy":
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Игрок {player}, ты ШПИОН!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Скрыть", callback_data="hide")]]
            )
        )
    else:
        card_name = card["name_ru"]
        file = card["file"]

        with open(f"{CARDS_FOLDER}/{file}.png", "rb") as img:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=img,
                caption=f"Игрок {player}, твоя карта: {card_name}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Скрыть", callback_data="hide")]]
                ),
                parse_mode=ParseMode.MARKDOWN
            )

    await query.edit_message_text(f"Игрок {player} смотрит свою роль...")


async def hide_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        await context.bot.delete_message(query.message.chat_id, query.message.message_id)
    except:
        pass

    context.chat_data["index"] += 1
    idx = context.chat_data["index"]
    players = context.chat_data["players"]

    if idx >= players:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Все роли показаны. Начните обсуждение!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Новая игра", callback_data="new_game")]]
            )
        )
    else:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Передайте телефон Игроку {idx+1}.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    f"Показать роль Игрока {idx+1}",
                    callback_data="show"
                )]]
            )
        )


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.chat_data.clear()
    await start(query, context)


# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(players_chosen, pattern="^players_"))
    app.add_handler(CallbackQueryHandler(show_role, pattern="^show$"))
    app.add_handler(CallbackQueryHandler(hide_role, pattern="^hide$"))
    app.add_handler(CallbackQueryHandler(new_game, pattern="^new_game$"))

    app.run_polling()


if __name__ == "__main__":
    main()
