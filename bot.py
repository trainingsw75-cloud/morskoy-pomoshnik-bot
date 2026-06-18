import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_TOKEN')

SITE_URL = "https://morskoy-pomoshnik.pages.dev"
SITE_GH  = "https://trainingsw75-cloud.github.io"

# ═══════════════════════════════════════
#  МЕНЮ
# ═══════════════════════════════════════
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 Документы и инструкции", callback_data="docs")],
        [InlineKeyboardButton("🛠️ Инструменты моряка",    callback_data="tools")],
        [InlineKeyboardButton("🤖 AI Генератор контента",  callback_data="ai_gen")],
        [InlineKeyboardButton("🧠 AI Психолог",            callback_data="ai_psych")],
        [InlineKeyboardButton("💰 Калькулятор отпускных",  callback_data="calc")],
        [InlineKeyboardButton("🎓 Тест готовности",        callback_data="test")],
        [InlineKeyboardButton("📰 Дайджест моряка",        callback_data="digest")],
        [InlineKeyboardButton("📅 Календарь отпуска",      callback_data="calendar")],
        [InlineKeyboardButton("🌐 Открыть сайт",           url=SITE_URL)],
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Главное меню", callback_data="start")],
        [InlineKeyboardButton("🌐 Открыть сайт", url=SITE_URL)],
    ])

# ═══════════════════════════════════════
#  /start
# ═══════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user.first_name else "Моряк"
    text = (
        f"⚓ <b>Морской помощник</b>\n\n"
        f"Привет, <b>{name}</b>! 👋\n\n"
        f"Я помогаю морякам и вахтовикам:\n"
        f"• 📄 Оформить документы (Госуслуги, МФЦ, ФНС)\n"
        f"• 💰 Получить пособия и гранты до 350 000 ₽\n"
        f"• 🤖 Создавать контент через AI\n"
        f"• 🧠 Получить психологическую поддержку\n"
        f"• 💰 Рассчитать отпускные\n\n"
        f"<i>Всё бесплатно — выберите раздел:</i>"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu(), parse_mode='HTML')
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  ДОКУМЕНТЫ
# ═══════════════════════════════════════
async def docs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "📄 <b>Документы и инструкции</b>\n\n"
        "Помогаем оформить:\n\n"
        "🏛️ <b>Госуслуги:</b>\n"
        "• Загранпаспорт (ускоренно для моряков)\n"
        "• Запись к врачу удалённо\n"
        "• СНИЛС, ИНН — восстановление\n"
        "• Регистрация ИП через МФЦ\n"
        "• 3-НДФЛ декларация\n\n"
        "💰 <b>Пособия и выплаты:</b>\n"
        "• Пособие по безработице в отпуске\n"
        "• Соцконтракт до 350 000 ₽\n"
        "• Субсидия на жильё для северян\n"
        "• Детские пособия (оформление женой)\n"
        "• Льготная пенсия моряка\n\n"
        "⚖️ <b>Налоги и ФНС:</b>\n"
        "• Налоговые вычеты (имущественный, соц.)\n"
        "• Проверка задолженностей\n"
        "• КБМ по ОСАГО\n\n"
        f"🌐 Все инструкции: {SITE_URL}"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  ИНСТРУМЕНТЫ
# ═══════════════════════════════════════
async def tools_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Калькулятор отпускных", url=f"{SITE_URL}/finance-calc.html")],
        [InlineKeyboardButton("🎓 Тест готовности",       url=f"{SITE_URL}/exam-test.html")],
        [InlineKeyboardButton("📝 Генератор постов ВК",   url=f"{SITE_URL}/#generator")],
        [InlineKeyboardButton("🤖 AI Генератор",          url=f"{SITE_URL}/#ai-generator")],
        [InlineKeyboardButton("🧠 AI Психолог",           url=f"{SITE_URL}/#ai-psychologist")],
        [InlineKeyboardButton("🔙 Назад",                  callback_data="start")],
    ])
    text = (
        "🛠️ <b>Инструменты моряка</b>\n\n"
        "Все инструменты бесплатны:\n\n"
        "💰 <b>Калькулятор отпускных</b> — учитывает северные надбавки и НДФЛ\n\n"
        "🎓 <b>Тест готовности</b> — знаете ли вы все сроки и документы?\n\n"
        "📝 <b>Генератор постов ВК</b> — создаёт посты по шаблонам\n\n"
        "🤖 <b>AI Генератор</b> — контент через YandexGPT, GigaChat\n\n"
        "🧠 <b>AI Психолог</b> — поддержка при стрессе и разлуке\n\n"
        "Нажмите на инструмент чтобы открыть:"
    )
    await q.edit_message_text(text, reply_markup=keyboard, parse_mode='HTML')

# ═══════════════════════════════════════
#  AI ГЕНЕРАТОР
# ═══════════════════════════════════════
async def ai_gen_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "🤖 <b>AI Генератор контента</b>\n\n"
        "Создавайте посты и статьи через российские нейросети:\n\n"
        "🟣 <b>YandexGPT</b> — тексты, идеи, заголовки\n"
        "🎨 <b>Kandinsky</b> — картинки и обложки\n"
        "🔵 <b>GigaChat</b> — длинные тексты, анализ\n\n"
        "📌 Форматы:\n"
        "• Пост для ВКонтакте\n"
        "• Статья для сайта\n"
        "• Пошаговая инструкция\n"
        "• Сценарий видео\n\n"
        f"👉 Открыть генератор: {SITE_URL}/#ai-generator"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  AI ПСИХОЛОГ
# ═══════════════════════════════════════
async def ai_psych_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "🧠 <b>AI Психолог для моряков</b>\n\n"
        "Поддержка в сложных ситуациях:\n\n"
        "😰 Стресс в рейсе\n"
        "💔 Разлука с семьёй\n"
        "🔄 Адаптация после рейса\n"
        "💰 Финансовый стресс\n"
        "🌫️ Страх будущего\n\n"
        "🆘 <b>Экстренная помощь:</b>\n"
        "Телефон доверия: <b>8-800-2000-122</b>\n"
        "(круглосуточно, бесплатно)\n\n"
        f"👉 Открыть психолога: {SITE_URL}/#ai-psychologist"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  КАЛЬКУЛЯТОР
# ═══════════════════════════════════════
async def calc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "💰 <b>Калькулятор отпускных</b>\n\n"
        "Рассчитайте точную сумму с учётом:\n\n"
        "✅ Северных надбавок\n"
        "✅ Районного коэффициента\n"
        "✅ НДФЛ 13%\n"
        "✅ Дней отпуска (28 + доп.)\n\n"
        "Средний моряк часто недополучает\n"
        "2 000 — 15 000 ₽ из-за ошибок расчёта!\n\n"
        f"👉 Открыть калькулятор: {SITE_URL}/finance-calc.html"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  ТЕСТ
# ═══════════════════════════════════════
async def test_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "🎓 <b>Тест готовности моряка</b>\n\n"
        "Проверьте — знаете ли вы:\n\n"
        "📋 Какие документы нужны в первые дни отпуска?\n"
        "⏰ Сроки подачи на пособие по безработице?\n"
        "💰 Размер социального контракта в вашем регионе?\n"
        "📊 Когда нужно подавать 3-НДФЛ?\n\n"
        "Тест займёт 5 минут и покажет\n"
        "какие темы нужно изучить.\n\n"
        f"👉 Пройти тест: {SITE_URL}/exam-test.html"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  ДАЙДЖЕСТ
# ═══════════════════════════════════════
async def digest_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "📰 <b>Дайджест моряка — июнь 2026</b>\n\n"
        "🆕 <b>Пособия по безработице</b>\n"
        "С 1 мая 2026 — не нужна справка с судна.\n"
        "Достаточно трудового договора.\n\n"
        "💰 <b>Соцконтракт в Татарстане</b>\n"
        "Увеличен до 400 000 ₽ для прибрежных городов.\n\n"
        "📱 <b>Госуслуги обновили приложение</b>\n"
        "Загранпаспорт теперь без МФЦ.\n\n"
        "⚠️ <b>Штрафы за неоформленные дроны</b>\n"
        "ФАВТ — от 50 000 ₽. Проверьте регистрацию!\n\n"
        f"🌐 Все новости: {SITE_URL}/#digest"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  КАЛЕНДАРЬ
# ═══════════════════════════════════════
async def calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "📅 <b>Календарь отпуска моряка</b>\n\n"
        "📌 <b>День 1:</b>\n"
        "Получить трудовую/СТД-Р, справку о заработке\n\n"
        "📌 <b>День 2-3:</b>\n"
        "МФЦ — справки о составе семьи и доходах\n"
        "(запись через Госуслуги заранее!)\n\n"
        "📌 <b>День 4-5:</b>\n"
        "Центр занятости — встать на учёт, подать на пособие\n\n"
        "📌 <b>Неделя 2:</b>\n"
        "ФНС — проверить задолженности, подать 3-НДФЛ\n\n"
        "📌 <b>Неделя 3-4:</b>\n"
        "Соцзащита — заявление на соцконтракт + бизнес-план\n\n"
        "📌 <b>Месяц 2:</b>\n"
        "Курсы предпринимательства + ожидание решений\n\n"
        f"🌐 Полный сайт: {SITE_URL}"
    )
    await q.edit_message_text(text, reply_markup=back_menu(), parse_mode='HTML')

# ═══════════════════════════════════════
#  ТЕКСТОВЫЕ СООБЩЕНИЯ
# ═══════════════════════════════════════
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    if any(w in msg for w in ['документ', 'паспорт', 'снилс', 'инн', 'мфц', 'госуслуг']):
        await update.message.reply_text(
            "📄 По документам — нажмите кнопку ниже:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📄 Документы", callback_data="docs"),
                InlineKeyboardButton("🌐 Сайт", url=SITE_URL)
            ]])
        )
    elif any(w in msg for w in ['пособи', 'безработ', 'грант', 'соцконтракт', 'цзн']):
        await update.message.reply_text(
            "💰 По пособиям:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💰 Пособия", callback_data="docs"),
                InlineKeyboardButton("🌐 Сайт", url=SITE_URL)
            ]])
        )
    elif any(w in msg for w in ['отпускн', 'калькул', 'расчёт', 'рассчит']):
        await update.message.reply_text(
            f"💰 Калькулятор отпускных: {SITE_URL}/finance-calc.html"
        )
    elif any(w in msg for w in ['психол', 'стресс', 'семь', 'разлук']):
        await update.message.reply_text(
            f"🧠 AI Психолог: {SITE_URL}/#ai-psychologist\n\n"
            "🆘 Телефон доверия: 8-800-2000-122"
        )
    else:
        await update.message.reply_text(
            f"⚓ Выберите раздел:",
            reply_markup=main_menu()
        )

# ═══════════════════════════════════════
#  CALLBACK ROUTER
# ═══════════════════════════════════════
async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    handlers = {
        'start':    start,
        'docs':     docs_handler,
        'tools':    tools_handler,
        'ai_gen':   ai_gen_handler,
        'ai_psych': ai_psych_handler,
        'calc':     calc_handler,
        'test':     test_handler,
        'digest':   digest_handler,
        'calendar': calendar_handler,
    }
    handler = handlers.get(data)
    if handler:
        await handler(update, context)
    else:
        await update.callback_query.answer("Раздел в разработке")

# ═══════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════
def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable is not set!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  start))
    app.add_handler(CallbackQueryHandler(button_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    logger.info("⚓ Морской помощник bot started!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
