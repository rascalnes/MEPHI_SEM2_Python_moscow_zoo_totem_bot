#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram-бот викторина "Твоё тотемное животное в Московском зоопарке"
Для популяризации программы опеки
"""

import logging
import html
import json
from typing import Dict, List, Tuple
from datetime import datetime

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ConversationHandler
)
from telegram.constants import ParseMode

import config
from quiz_data import QUESTIONS, TOTEM_ANIMALS, calculate_totem

# Настройка логирования для мониторинга производительности
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
(
    START_QUIZ,
    ANSWER_QUESTION,
    SHOW_RESULT,
    FEEDBACK,
    CONTACT_MANAGER
) = range(5)

# Хранилище данных пользователей (в реальном проекте использовать БД)
user_data_store: Dict[int, Dict] = {}


# Клавиатура главного меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🎮 Начать викторину"), KeyboardButton("ℹ️ О программе опеки")],
        [KeyboardButton("📞 Связаться с зоопарком"), KeyboardButton("⭐ Оставить отзыв")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context):
    """Обработчик команды /start"""
    user = update.effective_user
    user_id = user.id

    # Инициализация данных пользователя
    user_data_store[user_id] = {
        "current_question": 0,
        "answers": [],
        "quiz_active": False,
        "result": None,
        "username": user.username,
        "first_name": user.first_name,
        "start_time": datetime.now().isoformat()
    }

    welcome_text = (
        f"🐾 *Добро пожаловать в викторину Московского зоопарка, {user.first_name}!* 🐾\n\n"
        "Я помогу тебе найти твоё *тотемное животное* и расскажу о программе опеки.\n\n"
        "✨ *Как это работает:*\n"
        "• Ответь на 6 вопросов с долей юмора, но на основе реальных фактов\n"
        "• Получи своего тотемного зверя\n"
        "• Узнай, как стать опекуном животного в Московском зоопарке\n\n"
        "🚫 *Важно:* Большие панды не участвуют в программе опеки, поэтому они не в викторине.\n\n"
        "👇 *Нажми кнопку ниже, чтобы начать!*"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

    # Логирование для мониторинга
    logger.info(f"User {user_id} ({user.username}) started the bot")


async def about_guardianship(update: Update, context):
    """Информация о программе опеки"""
    guardianship_text = (
        "🌟 *Что такое программа опеки?* 🌟\n\n"
        "Опека в Московском зоопарке — это возможность:\n"
        "• 💚 Взять животное под личную опеку\n"
        "• 🎁 Получить именной сертификат\n"
        "• 🎟️ Бесплатно посещать зоопарк\n"
        "• 📸 Участвовать в фотосессиях с питомцем\n"
        "• 🏆 Вносить вклад в сохранение видов\n\n"
        f"📞 *Контакты отдела опеки:*\n"
        f"📧 Email: `{config.ZOO_CONTACT_EMAIL}`\n"
        f"📱 Телефон: `{config.ZOO_CONTACT_PHONE}`\n\n"
        "🌐 *Подробнее:* https://moscowzoo.ru/guardianship/\n\n"
        "Хотите узнать своё тотемное животное? Нажмите *«Начать викторину»*!"
    )

    await update.message.reply_text(
        guardianship_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )


async def start_quiz(update: Update, context):
    """Запуск викторины"""
    user_id = update.effective_user.id

    if user_id not in user_data_store:
        await start(update, context)

    # Сброс данных викторины
    user_data_store[user_id]["current_question"] = 0
    user_data_store[user_id]["answers"] = []
    user_data_store[user_id]["quiz_active"] = True

    await send_question(update, context, user_id)


async def send_question(update: Update, context, user_id: int):
    """Отправка вопроса пользователю"""
    user_data = user_data_store[user_id]
    q_index = user_data["current_question"]

    if q_index >= len(QUESTIONS):
        await calculate_and_show_result(update, context, user_id)
        return

    question = QUESTIONS[q_index]

    # Создание клавиатуры с вариантами ответов
    keyboard = []
    for i, option in enumerate(question["options"]):
        keyboard.append([InlineKeyboardButton(
            f"{chr(65 + i)}. {option['text'][:50]}",
            callback_data=f"ans_{q_index}_{i}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка вопроса
    question_text = f"📋 *Вопрос {q_index + 1}/{len(QUESTIONS)}*\n\n{question['text']}"

    # Используем edit или новое сообщение
    if update.callback_query:
        await update.callback_query.edit_message_text(
            question_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            question_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )


async def handle_answer(update: Update, context):
    """Обработка ответа пользователя"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if not data.startswith("ans_"):
        return

    # Парсинг ответа
    _, q_index, option_index = data.split("_")
    q_index = int(q_index)
    option_index = int(option_index)

    user_data = user_data_store.get(user_id)
    if not user_data or not user_data.get("quiz_active"):
        await query.edit_message_text("❌ Викторина не активна. Начните заново командой /start")
        return

    # Сохранение ответа
    question = QUESTIONS[q_index]
    selected_option = question["options"][option_index]
    user_data["answers"].append(selected_option["points"])
    user_data["current_question"] += 1

    # Подтверждение ответа
    await query.edit_message_text(
        f"✅ *Принято!*\n\n{chr(65 + option_index)}. {selected_option['text']}\n\n"
        f"➡️ Переходим к следующему вопросу...",
        parse_mode=ParseMode.MARKDOWN
    )

    # Отправка следующего вопроса через секунду
    if user_data["current_question"] < len(QUESTIONS):
        # Убираем sleep и отправляем новый вопрос напрямую
        await send_question(update, context, user_id)
    else:
        await calculate_and_show_result(update, context, user_id)


async def delayed_question(query, context, user_id):
    """Задержка перед следующим вопросом для UX"""
    import asyncio
    await asyncio.sleep(1)
    await send_question(query, context, user_id)


async def calculate_and_show_result(update, context, user_id):
    """Подсчёт результатов и показ тотемного животного"""
    user_data = user_data_store.get(user_id)
    if not user_data or not user_data.get("quiz_active"):
        return

    # Подсчёт тотемного животного
    totem_key, scores = calculate_totem(user_data["answers"])
    totem = TOTEM_ANIMALS[totem_key]

    user_data["result"] = totem_key
    user_data["quiz_active"] = False

    # Формирование результата
    result_text = (
        f"🎉 *Итоги викторины* 🎉\n\n"
        f"{totem['name']}\n\n"
        f"✨ *Описание:*\n{totem['description']}\n\n"
        f"📚 *Факт:* {totem['fact']}\n\n"
        f"💚 *Хотите помочь?*\n"
        f"Узнайте о программе опеки по кнопке ниже!"
    )

    # Создание клавиатуры для результата
    keyboard = [
        [InlineKeyboardButton("💚 Стать опекуном", callback_data="guardianship")],
        [InlineKeyboardButton("🔄 Пройти ещё раз", callback_data="restart_quiz")],
        [InlineKeyboardButton("📤 Поделиться", callback_data="share_result")],
        [InlineKeyboardButton("📞 Связаться с зоопарком", callback_data="contact_zoo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка изображения животного
    try:
        with open(f"images/{totem['image']}", 'rb') as photo:
            if hasattr(update, 'callback_query') and update.callback_query:
                await update.callback_query.message.reply_photo(
                    photo=photo,
                    caption=result_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_photo(
                    photo=photo,
                    caption=result_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
    except FileNotFoundError:
        # Если изображение не найдено, отправляем текст
        if hasattr(update, 'callback_query') and update.callback_query:
            await update.callback_query.edit_message_text(
                result_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                result_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )

    # Логирование результата
    logger.info(f"User {user_id} got totem: {totem_key}")


async def handle_result_action(update: Update, context):
    """Обработка действий после викторины"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    action = query.data

    user_data = user_data_store.get(user_id, {})
    result = user_data.get("result", "manul")

    if action == "guardianship":
        # Информация об опеке конкретного животного
        totem = TOTEM_ANIMALS.get(result, TOTEM_ANIMALS["manul"])
        guardianship_text = (
            f"💚 *Вы можете стать опекуном {totem['name']}!* 💚\n\n"
            f"Стоимость опеки: *от 50 000 ₽/год*\n\n"
            f"Что вы получите:\n"
            f"• Именной сертификат\n"
            f"• Табличку на вольере\n"
            f"• Бесплатные билеты в зоопарк\n"
            f"• Фотосессию с животным\n\n"
            f"📞 *Свяжитесь с нами:*\n"
            f"📧 {config.ZOO_CONTACT_EMAIL}\n"
            f"📱 {config.ZOO_CONTACT_PHONE}\n\n"
            f"🔗 [Подробнее о программе]({totem['opeka_link']})"
        )
        await query.edit_message_text(
            guardianship_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад к результату", callback_data="back_to_result")],
                [InlineKeyboardButton("📞 Написать сотруднику", callback_data="contact_zoo")]
            ])
        )

    elif action == "restart_quiz":
        # Перезапуск викторины
        user_data["current_question"] = 0
        user_data["answers"] = []
        user_data["quiz_active"] = True
        await send_question(query, context, user_id)

    elif action == "share_result":
        # Генерация результата для шаринга со ссылкой на бота
        totem = TOTEM_ANIMALS.get(result, TOTEM_ANIMALS["manul"])
        share_text = (
            f"🐾 *Моё тотемное животное в Московском зоопарке — {totem['name']}!* 🐾\n\n"
            f"{totem['fact'][:100]}...\n\n"
            f"✨ *Узнай своё тотемное животное:*\n"
            f"👉 @{context.bot.username} 👈\n\n"
            f"#МосковскийЗоопарк #ТотемноеЖивотное #Опекун"
        )
        await query.edit_message_text(
            share_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Скопировать текст", callback_data="copy_share_text")],
                [InlineKeyboardButton("🔙 К результату", callback_data="back_to_result")]
            ])
        )

    elif action == "back_to_result":
        # Возврат к результату
        await calculate_and_show_result(query, context, user_id)

    elif action == "contact_zoo":
        # Контактный механизм
        user = query.from_user
        result = user_data.get("result", "неизвестное животное")

        contact_text = (
            f"📞 *Связь с зоопарком* 📞\n\n"
            f"Вы можете задать вопросы об опеке:\n"
            f"• По телефону: `{config.ZOO_CONTACT_PHONE}`\n"
            f"• По email: `{config.ZOO_CONTACT_EMAIL}`\n"
            f"• В Telegram: @{config.ZOO_MANAGER_USERNAME}\n\n"
            f"⚠️ *Для сотрудника:*\n"
            f"Пользователь @{user.username} прошёл викторину и получил результат: *{result}*"
        )
        await query.edit_message_text(
            contact_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_result")]
            ])
        )

    elif action == "copy_share_text":
        await query.answer("Текст скопирован! Поделитесь в соцсетях 📤", show_alert=True)


async def feedback(update: Update, context):
    """Сбор обратной связи"""
    await update.message.reply_text(
        "⭐ *Оставьте отзыв о викторине* ⭐\n\n"
        "Напишите ваши пожелания или комментарии.\n"
        "Это поможет нам стать лучше!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            [["❌ Отмена"]],
            resize_keyboard=True
        )
    )
    return FEEDBACK


async def handle_feedback(update: Update, context):
    """Обработка отзыва"""
    user = update.effective_user
    feedback_text = update.message.text

    if feedback_text == "❌ Отмена":
        await update.message.reply_text(
            "Отмена отправки отзыва.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END

    # Сохранение отзыва (в реальном проекте — в БД или файл)
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {user.id} (@{user.username}): {feedback_text}\n")

    await update.message.reply_text(
        "🙏 *Спасибо за ваш отзыв!*\n\n"
        "Он поможет сделать викторину ещё лучше.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

    logger.info(f"Feedback from user {user.id}: {feedback_text[:100]}")
    return ConversationHandler.END


async def cancel_feedback(update: Update, context):
    """Отмена отправки отзыва"""
    await update.message.reply_text(
        "Отмена.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END


async def contact_manager(update: Update, context):
    """Обработчик кнопки связи с сотрудником"""
    user = update.effective_user

    contact_text = (
        f"📞 *Как связаться с зоопарком* 📞\n\n"
        f"• Телефон: `{config.ZOO_CONTACT_PHONE}`\n"
        f"• Email: `{config.ZOO_CONTACT_EMAIL}`\n"
        f"• Telegram: @{config.ZOO_MANAGER_USERNAME}\n\n"
        f"*Часы работы:* Пн-Вс с 10:00 до 18:00\n\n"
        f"При обращении укажите, что вы прошли викторину!"
    )

    await update.message.reply_text(
        contact_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )


async def error_handler(update: Update, context):
    """Глобальный обработчик ошибок (мониторинг производительности)"""
    logger.error(f"Exception while handling an update: {context.error}")

    if update and update.effective_chat:
        await update.effective_chat.send_message(
            "😕 Произошла небольшая техническая ошибка. Пожалуйста, попробуйте снова через минуту."
        )


def main():
    """Запуск бота"""
    # Создание приложения
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", start_quiz))

    # Обработчики кнопок главного меню
    application.add_handler(MessageHandler(
        filters.Regex("^🎮 Начать викторину$"), start_quiz
    ))
    application.add_handler(MessageHandler(
        filters.Regex("^ℹ️ О программе опеки$"), about_guardianship
    ))
    application.add_handler(MessageHandler(
        filters.Regex("^📞 Связаться с зоопарком$"), contact_manager
    ))
    application.add_handler(MessageHandler(
        filters.Regex("^⭐ Оставить отзыв$"), feedback
    ))

    # Обработчик ответов викторины
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^ans_"))
    application.add_handler(CallbackQueryHandler(handle_result_action,
                                                 pattern="^(guardianship|restart_quiz|share_result|back_to_result|contact_zoo|copy_share_text)$"))

    # Conversation для обратной связи
    feedback_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^⭐ Оставить отзыв$"), feedback)],
        states={
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback)],
        },
        fallbacks=[MessageHandler(filters.Regex("^❌ Отмена$"), cancel_feedback)],
    )
    application.add_handler(feedback_handler)

    # Глобальный обработчик ошибок
    application.add_error_handler(error_handler)

    # Запуск бота
    print("🤖 Бот запущен...")
    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()