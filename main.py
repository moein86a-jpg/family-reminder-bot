import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8405322168:AAGwx9nhxfmo0_7bn3rB9ulgrXcPgnOJ4pE"
AUTHORIZED_CHAT_ID = 5222594798

bot = telebot.TeleBot(BOT_TOKEN)

devices = {
    "a8f2c9": {"name": "علی - Pixel 7", "online": True},
    "b2d9f0": {"name": "رضا - Galaxy A51", "online": True},
    "c3e4a1": {"name": "نازنین - Redmi 12", "online": False}
}

user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != AUTHORIZED_CHAT_ID:
        bot.reply_to(message, "❌ شما اجازه دسترسی ندارید.")
        return

    keyboard = InlineKeyboardMarkup()
    for dev in devices:
        keyboard.add(InlineKeyboardButton(devices[dev]["name"], callback_data=f"device_{dev}"))
    bot.send_message(message.chat.id, "📱 انتخاب گوشی:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def button(call):
    if call.message.chat.id != AUTHORIZED_CHAT_ID:
        bot.edit_message_text("❌ شما اجازه دسترسی ندارید.", call.message.chat.id, call.message.message_id)
        return

    data = call.data

    if data.startswith("device_"):
        device_id = data.split("_")[1]
        user_state[call.message.chat.id] = {"device": device_id}
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📳 ویبره", callback_data="vibrate"))
        keyboard.add(InlineKeyboardButton("🔊 پخش ویس", callback_data="voice"))
        keyboard.add(InlineKeyboardButton("🔒 قفل صفحه", callback_data="lock"))
        keyboard.add(InlineKeyboardButton("⛔ توقف", callback_data="stop"))
        bot.edit_message_text("📟 فرمان‌ها:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        return

    bot.edit_message_text(f"✅ فرمان '{data}' برای {devices.get(user_state.get(call.message.chat.id, {}).get('device', ''), {}).get('name', 'نامشخص')} اجرا شد!", call.message.chat.id, call.message.message_id)

print("ربات شروع شد...")
bot.infinity_polling()
