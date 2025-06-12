from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import requests
from html import escape
from datetime import timedelta
from collections import defaultdict

logs = []
user_stats = defaultdict(lambda: {"messages": 0, "photos": 0, "voices": 0})
warnings = defaultdict(int)  # username: количество предупреждений

async def log_command_usage(update: Update, command: str):
    user = update.effective_user
    logs.append(f"{user.first_name} ({user.id}) использовал команду {command} в {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/start")
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    user = update.effective_user
    username = user.username if user.username else user.first_name
    await update.message.reply_text(
        f"Привет, {username}! Я бот. Выберите команду:",
        reply_markup=reply_markup
    )

async def randomem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/randomem")
    try:
        response = requests.get("https://meme-api.com/gimme")
        if response.status_code == 200:
            data = response.json()
            meme_url = data.get("url")
            title = data.get("title", "Мем")
            if meme_url:
                await update.message.reply_photo(meme_url, caption=title)
            else:
                await update.message.reply_text("Не удалось получить мем. Попробуйте позже.")
        else:
            await update.message.reply_text("Не удалось получить мем. Попробуйте позже.")
    except Exception:
        await update.message.reply_text("Ошибка при получении мема.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/help")
    await update.message.reply_text(
        "Команда /help вызвана. Я здесь, чтобы помочь!\n"
        "Список команд:\n"
        "/start - Начать взаимодействие\n"
        "/help - Получить помощь\n"
        "/info - Информация о боте\n"
        "/anime - Получить аниме-картинку\n"
        "/randomem - Случайный мем\n"
        "/rustmeme - Мем по Rust\n"
        "/weather <город> - Погода в городе\n"
        "/ban <user_id> - Заблокировать пользователя\n"
        "/unban <user_id> - Разблокировать пользователя\n"
        "/mut <user_id> [минуты] - Замутить пользователя на время\n"
        "/unmut <user_id> - Размутить пользователя\n"
        "/stats - Статистика пользователей (сообщения, фото, голосовые)\n"
        "/warn <user_id> - Выдать предупреждение\n"
        "/unwarn <user_id> - Снять предупреждение\n"
        "/warnings - Показать список предупреждений\n"
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/info")
    await update.message.reply_text("Информация о боте: Я простой бот, созданный для демонстрации.")

async def anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/anime")
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    if response.status_code == 200:
        image_url = response.json()["url"]
        await update.message.reply_photo(image_url, caption="Вот твоя аниме-картинка!")
    else:
        await update.message.reply_text("Не удалось получить аниме-картинку. Попробуйте позже.")

async def b_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/b")
    await update.message.reply_text("ТЯ БОНЬКНУЛИ")

async def logs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/logs")
    if logs:
        await update.message.reply_text("\n".join(logs[-100:]))
    else:
        await update.message.reply_text("Логи пока пусты.")

# Используем username вместо user_id для банов, мутов и варнов
def extract_username(arg):
    return arg.lstrip('@').lower()

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/ban")
    if context.args:
        username = extract_username(context.args[0])
        await update.message.reply_text(f"Пользователь @{username} заблокирован.")
    else:
        await update.message.reply_text("Пожалуйста, укажите username для блокировки.")

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/unban")
    if context.args:
        username = extract_username(context.args[0])
        await update.message.reply_text(f"Пользователь @{username} разблокирован.")
    else:
        await update.message.reply_text("Пожалуйста, укажите username для разблокировки.")

async def mut_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/mut")
    if context.args:
        username = extract_username(context.args[0])
        mute_time = None
        if len(context.args) > 1:
            try:
                mute_time = int(context.args[1])
            except ValueError:
                await update.message.reply_text("Время мута должно быть числом (в минутах).")
                return
        if mute_time:
            await update.message.reply_text(
                f"Пользователь @{username} замучен на {mute_time} минут."
            )
        else:
            await update.message.reply_text(f"Пользователь @{username} замучен.")
    else:
        await update.message.reply_text("Пожалуйста, укажите username для мута и (необязательно) время в минутах.")

async def unmut_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/unmut")
    if context.args:
        username = extract_username(context.args[0])
        await update.message.reply_text(f"Пользователь @{username} размучен.")
    else:
        await update.message.reply_text("Пожалуйста, укажите username для размута.")




async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/stats")
    if user_stats:
        stats_lines = []
        for user_id, stats in user_stats.items():
            stats_lines.append(
                f"ID {user_id}: сообщений — {stats['messages']}, фото — {stats['photos']}, голосовых — {stats['voices']}"
            )
        await update.message.reply_text("\n".join(stats_lines))
    else:
        await update.message.reply_text("Статистика пока пуста.")

async def message_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.voice:
        user_stats[user_id]["voices"] += 1
    elif update.message.photo:
        user_stats[user_id]["photos"] += 1
    else:
        user_stats[user_id]["messages"] += 1

async def rustmeme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/rustmeme")
    try:
        response = requests.get("https://meme-api.com/gimme/playrust")
        if response.status_code == 200:
            data = response.json()
            meme_url = data.get("url")
            title = data.get("title", "Rust мем")
            if meme_url:
                await update.message.reply_photo(meme_url, caption=title)
            else:
                await update.message.reply_text("Не удалось получить Rust мем. Попробуйте позже.")
        else:
            await update.message.reply_text("Не удалось получить Rust мем. Попробуйте позже.")
    except Exception:
        await update.message.reply_text("Ошибка при получении Rust мема.")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/weather")
    if context.args:
        city = " ".join(context.args)
    else:
        await update.message.reply_text("Пожалуйста, укажите город. Пример: /weather Москва")
        return

    try:
        # Получаем координаты города через geocoding API (open-meteo)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru&format=json"
        geo_resp = requests.get(geo_url)
        if geo_resp.status_code == 200 and geo_resp.json().get("results"):
            geo = geo_resp.json()["results"][0]
            lat = geo["latitude"]
            lon = geo["longitude"]
            city_name = geo["name"]
        else:
            await update.message.reply_text("Город не найден.")
            return

        # Получаем погоду по координатам
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url)
        if weather_resp.status_code == 200:
            data = weather_resp.json()
            weather = data.get("current_weather", {})
            temp = weather.get("temperature")
            wind = weather.get("windspeed")
            desc = weather.get("weathercode", "Нет данных")
            await update.message.reply_text(
                f"Погода в {city_name}:\nТемпература: {temp}°C\nВетер: {wind} м/с\nКод погоды: {desc}"
            )
        else:
            await update.message.reply_text("Не удалось получить погоду. Попробуйте позже.")
    except Exception:
        await update.message.reply_text("Ошибка при получении погоды.")

async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/warn")
    if context.args:
        username = extract_username(context.args[0])
        warnings[username] += 1
        count = warnings[username]
        await update.message.reply_text(f"Пользователь @{username} получил предупреждение. Всего предупреждений: {count}")
    else:
        await update.message.reply_text("Пожалуйста, укажите username для предупреждения.")

async def unwarn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/unwarn")
    if context.args:
        username = extract_username(context.args[0])
        if warnings[username] > 0:
            warnings[username] -= 1
            await update.message.reply_text(f"С пользователя @{username} снято предупреждение. Осталось: {warnings[username]}")
        else:
            await update.message.reply_text(f"У пользователя @{username} нет предупреждений.")
    else:
        await update.message.reply_text("Пожалуйста, укажите username для снятия предупреждения.")

async def warnings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_command_usage(update, "/warnings")
    if warnings:
        lines = []
        for username, count in warnings.items():
            lines.append(f"@{username}: предупреждений — {count}")
        await update.message.reply_text("\n".join(lines))
    else:
        await update.message.reply_text("Пока нет предупреждений.")

async def api_test_command(update, context):
    try:
        # Отключаем проверку SSL-сертификата (ТОЛЬКО для разработки!)
        response = requests.get("https://localhost:44332/", verify=False)
        if response.status_code == 200:
            data = response.json()
            await update.message.reply_text(f"Ответ от API: {data}")
        else:
            await update.message.reply_text("Ошибка при обращении к API.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")




