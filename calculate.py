#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
TOTAL_INHERITANCE, DEBTS, HAS_SPOUSE, HAS_WIFE, NUM_DAUGHTERS, NUM_SONS, NUM_GRANDDAUGHTERS, NUM_GRANDSONS, HAS_FATHER, HAS_MOTHER, HAS_GRANDFATHER, HAS_GRANDMOTHER, NUM_COUSINS_SISTERS, NUM_COUSINS_BROTHERS = range(
    14)


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask for the total inheritance amount."""
    update.message.reply_text(
        'Ассаламу алейкум! Я помогу рассчитать доли наследства по исламским законам.\n'
        'Введите общую сумму наследства (только число):')
    # Initialize user data
    context.user_data.clear()
    return TOTAL_INHERITANCE


def handle_total_inheritance(update: Update, context: CallbackContext) -> int:
    """Parse and store the total inheritance amount."""
    try:
        total = float(update.message.text.replace(',', '.'))
        if total <= 0:
            raise ValueError("Сумма наследства должна быть положительной")

        context.user_data['total_inheritance'] = total
        update.message.reply_text(
            f'Сумма наследства: {total}\nВведите общую сумму долгов (если нет, введите 0):'
        )
        return DEBTS
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите корректное число:')
        return TOTAL_INHERITANCE


def handle_debts(update: Update, context: CallbackContext) -> int:
    """Parse and store the debts amount."""
    try:
        debts = float(update.message.text.replace(',', '.'))
        if debts < 0:
            raise ValueError("Сумма долгов не может быть отрицательной")

        context.user_data['debts'] = debts
        update.message.reply_text(
            'Есть ли супруг (муж)? (введите 1 - да, 0 - нет)')
        return HAS_SPOUSE
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите корректное число:')
        return DEBTS


def handle_has_spouse(update: Update, context: CallbackContext) -> int:
    """Parse and store whether the deceased has a spouse (husband)."""
    try:
        text = update.message.text.strip()
        if text not in ["0", "1"]:
            raise ValueError("Пожалуйста, введите 1 для 'да' или 0 для 'нет'")

        context.user_data['has_spouse'] = bool(int(text))
        update.message.reply_text(
            'Есть ли супруга (жена)? (введите 1 - да, 0 - нет)')
        return HAS_WIFE
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return HAS_SPOUSE


def handle_has_wife(update: Update, context: CallbackContext) -> int:
    """Parse and store whether the deceased has a wife."""
    try:
        text = update.message.text.strip()
        if text not in ["0", "1"]:
            raise ValueError("Пожалуйста, введите 1 для 'да' или 0 для 'нет'")

        context.user_data['has_wife'] = bool(int(text))
        update.message.reply_text('Сколько дочерей? (введите число)')
        return NUM_DAUGHTERS
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return HAS_WIFE


def handle_num_daughters(update: Update, context: CallbackContext) -> int:
    """Parse and store the number of daughters."""
    try:
        num = int(update.message.text.strip())
        if num < 0:
            raise ValueError("Число не может быть отрицательным")

        context.user_data['num_daughters'] = num
        update.message.reply_text('Сколько сыновей? (введите число)')
        return NUM_SONS
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите целое число:')
        return NUM_DAUGHTERS


def handle_num_sons(update: Update, context: CallbackContext) -> int:
    """Parse and store the number of sons."""
    try:
        num = int(update.message.text.strip())
        if num < 0:
            raise ValueError("Число не может быть отрицательным")

        context.user_data['num_sons'] = num
        update.message.reply_text('Сколько внучек? (введите число)')
        return NUM_GRANDDAUGHTERS
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите целое число:')
        return NUM_SONS


def handle_num_granddaughters(update: Update, context: CallbackContext) -> int:
    """Parse and store the number of granddaughters."""
    try:
        num = int(update.message.text.strip())
        if num < 0:
            raise ValueError("Число не может быть отрицательным")

        context.user_data['num_granddaughters'] = num
        update.message.reply_text('Сколько внуков? (введите число)')
        return NUM_GRANDSONS
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите целое число:')
        return NUM_GRANDDAUGHTERS


def handle_num_grandsons(update: Update, context: CallbackContext) -> int:
    """Parse and store the number of grandsons."""
    try:
        num = int(update.message.text.strip())
        if num < 0:
            raise ValueError("Число не может быть отрицательным")

        context.user_data['num_grandsons'] = num
        update.message.reply_text(
            'Жив ли отец наследодателя? (введите 1 - да, 0 - нет)')
        return HAS_FATHER
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите целое число:')
        return NUM_GRANDSONS


def handle_has_father(update: Update, context: CallbackContext) -> int:
    """Parse and store whether the deceased's father is alive."""
    try:
        text = update.message.text.strip()
        if text not in ["0", "1"]:
            raise ValueError("Пожалуйста, введите 1 для 'да' или 0 для 'нет'")

        context.user_data['has_father'] = bool(int(text))
        update.message.reply_text(
            'Жива ли мать наследодателя? (введите 1 - да, 0 - нет)')
        return HAS_MOTHER
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return HAS_FATHER


def handle_has_mother(update: Update, context: CallbackContext) -> int:
    """Parse and store whether the deceased's mother is alive."""
    try:
        text = update.message.text.strip()
        if text not in ["0", "1"]:
            raise ValueError("Пожалуйста, введите 1 для 'да' или 0 для 'нет'")

        context.user_data['has_mother'] = bool(int(text))
        update.message.reply_text(
            'Жив ли дедушка (по отцовской линии)? (введите 1 - да, 0 - нет)')
        return HAS_GRANDFATHER
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return HAS_MOTHER


def handle_has_grandfather(update: Update, context: CallbackContext) -> int:
    """Parse and store whether the deceased's grandfather is alive."""
    try:
        text = update.message.text.strip()
        if text not in ["0", "1"]:
            raise ValueError("Пожалуйста, введите 1 для 'да' или 0 для 'нет'")

        context.user_data['has_grandfather'] = bool(int(text))
        update.message.reply_text(
            'Жива ли бабушка (по отцовской линии)? (введите 1 - да, 0 - нет)')
        return HAS_GRANDMOTHER
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return HAS_GRANDFATHER


def handle_has_grandmother(update: Update, context: CallbackContext) -> int:
    """Parse and store whether the deceased's grandmother is alive."""
    try:
        text = update.message.text.strip()
        if text not in ["0", "1"]:
            raise ValueError("Пожалуйста, введите 1 для 'да' или 0 для 'нет'")

        context.user_data['has_grandmother'] = bool(int(text))
        update.message.reply_text(
            'Сколько родных сестёр у наследодателя? (введите число)')
        return NUM_COUSINS_SISTERS
    except ValueError as e:
        update.message.reply_text(f'Ошибка: {str(e)}')
        return HAS_GRANDMOTHER


def handle_num_cousins_sisters(update: Update,
                               context: CallbackContext) -> int:
    """Parse and store the number of sisters."""
    try:
        num = int(update.message.text.strip())
        if num < 0:
            raise ValueError("Число не может быть отрицательным")

        context.user_data['num_cousins_sisters'] = num
        update.message.reply_text(
            'Сколько родных братьев у наследодателя? (введите число)')
        return NUM_COUSINS_BROTHERS
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите целое число:')
        return NUM_COUSINS_SISTERS


def handle_num_cousins_brothers(update: Update,
                                context: CallbackContext) -> int:
    """Parse and store the number of brothers and complete the calculation."""
    try:
        num = int(update.message.text.strip())
        if num < 0:
            raise ValueError("Число не может быть отрицательным")

        context.user_data['num_cousins_brothers'] = num

        # Calculate inheritance shares
        inheritance_data = calculate_inheritance(context.user_data)

        # Format the response
        response = format_inheritance_response(context.user_data, inheritance_data)

        update.message.reply_text(response)
        return ConversationHandler.END
    except ValueError as e:
        update.message.reply_text(
            f'Ошибка: {str(e)}. Пожалуйста, введите целое число:')
        return NUM_COUSINS_BROTHERS


def calculate_inheritance(user_data):
    """Calculate inheritance shares based on Islamic inheritance laws."""
    total_inheritance = float(user_data.get('total_inheritance', 0))
    debts = float(user_data.get('debts', 0))

    # Calculate net inheritance after debts
    net_inheritance = max(0, total_inheritance - debts)

    if net_inheritance <= 0:
        return {
            "amounts": {"Ошибка": "После выплаты долгов не осталось средств для распределения"},
            "fractions": {},
            "percentages": {}
        }

    # Initialize shares for different family members
    amounts = {}  # Денежные суммы
    fractions = {}  # Доли в виде дробей
    percentages = {}  # Процентное соотношение
    remaining = net_inheritance

    # Islamic inheritance calculation rules
    # 1. First allocate fixed shares (Fard)
    # 2. Then distribute remaining to agnatic heirs (Asaba)

    # Spouse shares
    if user_data.get('has_spouse', False):
        has_descendants = (user_data.get('num_sons', 0) > 0
                           or user_data.get('num_daughters', 0) > 0
                           or user_data.get('num_grandsons', 0) > 0
                           or user_data.get('num_granddaughters', 0) > 0)

        if has_descendants:
            spouse_share = net_inheritance * 0.25
            fractions["Супруг (муж)"] = "1/4"
            percentages["Супруг (муж)"] = 25.0
        else:
            spouse_share = net_inheritance * 0.5
            fractions["Супруг (муж)"] = "1/2"
            percentages["Супруг (муж)"] = 50.0
            
        amounts["Супруг (муж)"] = spouse_share
        remaining -= spouse_share

    if user_data.get('has_wife', False):
        has_descendants = (user_data.get('num_sons', 0) > 0
                           or user_data.get('num_daughters', 0) > 0
                           or user_data.get('num_grandsons', 0) > 0
                           or user_data.get('num_granddaughters', 0) > 0)

        if has_descendants:
            wife_share = net_inheritance * 0.125
            fractions["Супруга (жена)"] = "1/8"
            percentages["Супруга (жена)"] = 12.5
        else:
            wife_share = net_inheritance * 0.25
            fractions["Супруга (жена)"] = "1/4"
            percentages["Супруга (жена)"] = 25.0
            
        amounts["Супруга (жена)"] = wife_share
        remaining -= wife_share

    # Parents shares
    if user_data.get('has_father', False):
        has_sons = user_data.get('num_sons', 0) > 0
        if has_sons:
            father_share = net_inheritance * (1/6)
            fractions["Отец"] = "1/6"
            percentages["Отец"] = 16.67
        else:
            father_share = remaining  # Father gets residue if no sons
            fractions["Отец"] = "Остаток"
            if net_inheritance > 0:
                percentages["Отец"] = (father_share / net_inheritance) * 100
            else:
                percentages["Отец"] = 0
            
        amounts["Отец"] = father_share
        remaining -= father_share

    if user_data.get('has_mother', False):
        has_children = (user_data.get('num_sons', 0) > 0
                        or user_data.get('num_daughters', 0) > 0)
        has_siblings = (user_data.get('num_cousins_brothers', 0) > 0
                        or user_data.get('num_cousins_sisters', 0) > 0)

        if has_children or has_siblings:
            mother_share = net_inheritance * (1/6)
            fractions["Мать"] = "1/6"
            percentages["Мать"] = 16.67
        else:
            mother_share = net_inheritance * (1/3)
            fractions["Мать"] = "1/3"
            percentages["Мать"] = 33.33

        amounts["Мать"] = mother_share
        remaining -= mother_share

    # If father is not alive but grandfather is alive
    if not user_data.get('has_father', False) and user_data.get('has_grandfather', False):
        grandfather_share = net_inheritance * (1/6)
        amounts["Дедушка (по отцу)"] = grandfather_share
        fractions["Дедушка (по отцу)"] = "1/6"
        percentages["Дедушка (по отцу)"] = 16.67
        remaining -= grandfather_share

    # If mother is not alive but grandmother is alive
    if not user_data.get('has_mother', False) and user_data.get('has_grandmother', False):
        grandmother_share = net_inheritance * (1/6)
        amounts["Бабушка (по матери)"] = grandmother_share
        fractions["Бабушка (по матери)"] = "1/6"
        percentages["Бабушка (по матери)"] = 16.67
        remaining -= grandmother_share

    # Children shares
    num_sons = user_data.get('num_sons', 0)
    num_daughters = user_data.get('num_daughters', 0)

    if num_sons > 0 or num_daughters > 0:
        # In Islamic law, a son gets twice the share of a daughter
        total_parts = num_sons * 2 + num_daughters

        if total_parts > 0:
            share_per_part = remaining / total_parts

            if num_sons > 0:
                son_share = share_per_part * 2
                son_percentage = (son_share / net_inheritance) * 100 if net_inheritance > 0 else 0
                
                if num_sons > 1:
                    amounts[f"Сыновья ({num_sons})"] = son_share * num_sons
                    amounts[f"Каждому сыну"] = son_share
                    fractions[f"Каждому сыну"] = f"{2}/{total_parts} остатка"
                    percentages[f"Каждому сыну"] = son_percentage
                else:
                    amounts["Сын"] = son_share
                    fractions["Сын"] = f"{2}/{total_parts} остатка"
                    percentages["Сын"] = son_percentage

            if num_daughters > 0:
                daughter_share = share_per_part
                daughter_percentage = (daughter_share / net_inheritance) * 100 if net_inheritance > 0 else 0
                
                if num_daughters > 1:
                    amounts[f"Дочери ({num_daughters})"] = daughter_share * num_daughters
                    amounts[f"Каждой дочери"] = daughter_share
                    fractions[f"Каждой дочери"] = f"1/{total_parts} остатка"
                    percentages[f"Каждой дочери"] = daughter_percentage
                else:
                    amounts["Дочь"] = daughter_share
                    fractions["Дочь"] = f"1/{total_parts} остатка"
                    percentages["Дочь"] = daughter_percentage

            remaining = 0  # All remaining inheritance distributed

    # If no children, distribute to grandchildren
    if num_sons == 0 and num_daughters == 0 and remaining > 0:
        num_grandsons = user_data.get('num_grandsons', 0)
        num_granddaughters = user_data.get('num_granddaughters', 0)

        if num_grandsons > 0 or num_granddaughters > 0:
            total_parts = num_grandsons * 2 + num_granddaughters

            if total_parts > 0:
                share_per_part = remaining / total_parts

                if num_grandsons > 0:
                    grandson_share = share_per_part * 2
                    grandson_percentage = (grandson_share / net_inheritance) * 100 if net_inheritance > 0 else 0
                    
                    if num_grandsons > 1:
                        amounts[f"Внуки ({num_grandsons})"] = grandson_share * num_grandsons
                        amounts[f"Каждому внуку"] = grandson_share
                        fractions[f"Каждому внуку"] = f"{2}/{total_parts} остатка"
                        percentages[f"Каждому внуку"] = grandson_percentage
                    else:
                        amounts["Внук"] = grandson_share
                        fractions["Внук"] = f"{2}/{total_parts} остатка"
                        percentages["Внук"] = grandson_percentage

                if num_granddaughters > 0:
                    granddaughter_share = share_per_part
                    granddaughter_percentage = (granddaughter_share / net_inheritance) * 100 if net_inheritance > 0 else 0
                    
                    if num_granddaughters > 1:
                        amounts[f"Внучки ({num_granddaughters})"] = granddaughter_share * num_granddaughters
                        amounts[f"Каждой внучке"] = granddaughter_share
                        fractions[f"Каждой внучке"] = f"1/{total_parts} остатка"
                        percentages[f"Каждой внучке"] = granddaughter_percentage
                    else:
                        amounts["Внучка"] = granddaughter_share
                        fractions["Внучка"] = f"1/{total_parts} остатка"
                        percentages["Внучка"] = granddaughter_percentage

                remaining = 0  # All remaining inheritance distributed

    # If still remaining inheritance, distribute to siblings
    if remaining > 0:
        num_brothers = user_data.get('num_cousins_brothers', 0)
        num_sisters = user_data.get('num_cousins_sisters', 0)

        if num_brothers > 0 or num_sisters > 0:
            total_parts = num_brothers * 2 + num_sisters

            if total_parts > 0:
                share_per_part = remaining / total_parts

                if num_brothers > 0:
                    brother_share = share_per_part * 2
                    brother_percentage = (brother_share / net_inheritance) * 100 if net_inheritance > 0 else 0
                    
                    if num_brothers > 1:
                        amounts[f"Братья ({num_brothers})"] = brother_share * num_brothers
                        amounts[f"Каждому брату"] = brother_share
                        fractions[f"Каждому брату"] = f"{2}/{total_parts} остатка"
                        percentages[f"Каждому брату"] = brother_percentage
                    else:
                        amounts["Брат"] = brother_share
                        fractions["Брат"] = f"{2}/{total_parts} остатка"
                        percentages["Брат"] = brother_percentage

                if num_sisters > 0:
                    sister_share = share_per_part
                    sister_percentage = (sister_share / net_inheritance) * 100 if net_inheritance > 0 else 0
                    
                    if num_sisters > 1:
                        amounts[f"Сестры ({num_sisters})"] = sister_share * num_sisters
                        amounts[f"Каждой сестре"] = sister_share
                        fractions[f"Каждой сестре"] = f"1/{total_parts} остатка"
                        percentages[f"Каждой сестре"] = sister_percentage
                    else:
                        amounts["Сестра"] = sister_share
                        fractions["Сестра"] = f"1/{total_parts} остатка"
                        percentages["Сестра"] = sister_percentage

                remaining = 0  # All remaining inheritance distributed

    # Возвращаем словарь с разными типами представления долей
    return {
        'amounts': amounts,  # Денежные суммы
        'fractions': fractions,  # Дроби по исламскому праву
        'percentages': percentages  # Проценты
    }


def format_inheritance_response(user_data, shares_data):
    """Format the inheritance calculation results for display."""
    total_inheritance = float(user_data.get('total_inheritance', 0))
    debts = float(user_data.get('debts', 0))
    net_inheritance = total_inheritance - debts

    # Проверяем структуру данных
    if isinstance(shares_data, dict) and 'amounts' in shares_data:
        # Новый формат данных
        amounts = shares_data.get('amounts', {})
        fractions = shares_data.get('fractions', {})
        percentages = shares_data.get('percentages', {})
    else:
        # Старый формат данных (обратная совместимость)
        amounts = shares_data
        fractions = {}
        percentages = {}

    response = "📋 *РЕЗУЛЬТАТЫ РАСЧЕТА НАСЛЕДСТВА*\n\n"
    response += f"💰 *Общая сумма наследства:* {total_inheritance:.2f}\n"
    response += f"💸 *Долги:* {debts:.2f}\n"
    response += f"🏦 *Чистая сумма для распределения:* {net_inheritance:.2f}\n\n"
    response += "*Распределение наследства:*\n"

    if not amounts:
        response += "❌ Не удалось рассчитать доли наследства.\n"
    else:
        # Сортируем наследников для лучшего представления
        for heir in sorted(amounts.keys()):
            amount = amounts[heir]
            # Обрабатываем значение, чтобы убедиться, что это число
            try:
                if isinstance(amount, (int, float)):
                    amount_value = amount
                else:
                    amount_value = float(amount)
                
                # Добавляем информацию о доли в виде дроби
                fraction_info = ""
                if heir in fractions:
                    fraction_info = f" ({fractions[heir]})"
                
                # Добавляем процентное соотношение
                percentage_info = ""
                if heir in percentages:
                    percentage_info = f" - {percentages[heir]:.2f}%"
                
                response += f"• {heir}: {amount_value:.2f}{fraction_info}{percentage_info}\n"
            except (ValueError, TypeError):
                # Если это не число (например, сообщение об ошибке)
                response += f"• {heir}: {amount}\n"

    response += "\n✅ Расчет выполнен согласно исламским законам наследования.\n"
    response += "ℹ️ Для нового расчета используйте команду /start"

    return response


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel and end the conversation."""
    update.message.reply_text(
        'Расчет отменен. Чтобы начать снова, используйте команду /start')
    return ConversationHandler.END


def error_handler(update, context):
    """Log errors caused by updates."""
    error_message = str(context.error)
    logger.warning(f'Update "{update}" caused error "{error_message}"')
    
    # Игнорируем ошибку конфликта при запуске нескольких экземпляров бота
    if "Conflict: terminated by other getUpdates request" in error_message:
        logger.info("Обнаружен другой экземпляр бота, работающий с тем же токеном.")
        return
        
    # Оба дополнительных условия нужны для защиты от возможных ошибок
    try:
        if update and hasattr(update, 'message') and update.message:
            update.message.reply_text(
                'Произошла ошибка. Пожалуйста, начните снова с команды /start')
    except Exception as e:
        logger.error(f"Ошибка в обработчике ошибок: {e}")


def help_command(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Этот бот помогает рассчитать доли наследства по исламским законам.\n'
        'Используйте команду /start для начала процесса расчета.\n'
        'Вам нужно будет ответить на несколько вопросов о наследодателе и его семье.'
    )


def main():
    """Start the bot."""
    # Get the token from environment variables or use a default one for development
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN","7151952822:AAFw_5hivRwHnchYDChApEYQrJC6SzYFNjc")

    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TOTAL_INHERITANCE: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_total_inheritance)
            ],
            DEBTS:
            [MessageHandler(Filters.text & ~Filters.command, handle_debts)],
            HAS_SPOUSE: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_has_spouse)
            ],
            HAS_WIFE:
            [MessageHandler(Filters.text & ~Filters.command, handle_has_wife)],
            NUM_DAUGHTERS: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_num_daughters)
            ],
            NUM_SONS:
            [MessageHandler(Filters.text & ~Filters.command, handle_num_sons)],
            NUM_GRANDDAUGHTERS: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_num_granddaughters)
            ],
            NUM_GRANDSONS: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_num_grandsons)
            ],
            HAS_FATHER: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_has_father)
            ],
            HAS_MOTHER: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_has_mother)
            ],
            HAS_GRANDFATHER: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_has_grandfather)
            ],
            HAS_GRANDMOTHER: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_has_grandmother)
            ],
            NUM_COUSINS_SISTERS: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_num_cousins_sisters)
            ],
            NUM_COUSINS_BROTHERS: [
                MessageHandler(Filters.text & ~Filters.command,
                               handle_num_cousins_brothers)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register error handler
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
