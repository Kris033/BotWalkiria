from telegram import Update
from telegram.ext import ContextTypes
from html import escape

async def horny_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("тя бонькнули 😏")

async def gf_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_a = update.effective_user
    user_b = None
    if update.message.reply_to_message:
        user_b = update.message.reply_to_message.from_user
    elif context.args:
        username = context.args[0].lstrip('@')
        user_b = type('User', (), {'id': 0, 'first_name': username})
    if user_b:
        mention_a = f'<a href="tg://user?id={user_a.id}">{escape(user_a.first_name)}</a>'
        if hasattr(user_b, 'id') and user_b.id != 0:
            mention_b = f'<a href="tg://user?id={user_b.id}">{escape(user_b.first_name)}</a>'
        else:
            mention_b = escape(user_b.first_name)
        text = f"{mention_a} обнял(а) {mention_b}! 🤗"
    await update.message.reply_text(text, parse_mode="HTML")

async def rust_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = "https://sun9-66.userapi.com/impg/1_3odmNPnx_b94HrDYPF5bBalVSodx04ouRgyg/IGiG5Lsvvx8.jpg?size=604x396&quality=96&sign=213ed8a00f011256bdbea6c242f8bc6e&type=album"
    await update.message.reply_photo(image_url, caption="Рейд начался! Вперёд, к победе! вот таблица ⚔️")

async def kiss_triger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_a = update.effective_user
    user_b = None

    if update.message.reply_to_message:
        user_b = update.message.reply_to_message.from_user
    elif context.args:
        username = context.args[0].lstrip('@')
        user_b = type('User', (), {'id': 0, 'first_name': username})

    if user_b:
        mention_a = f'<a href="tg://user?id={user_a.id}">{escape(user_a.first_name)}</a>'
        if hasattr(user_b, 'id') and user_b.id != 0:
            mention_b = f'<a href="tg://user?id={user_b.id}">{escape(user_b.first_name)}</a>'
        else:
            mention_b = escape(user_b.first_name)
        text = f"{mention_a} поцеловал(а) {mention_b}! 😘"
    else:
        text = "Укажите, кого поцеловать: ответьте на сообщение пользователя или напишите /kiss @username"

    await update.message.reply_text(text, parse_mode="HTML")




    