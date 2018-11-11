from telegram.ext import Updater, CommandHandler

token = None
updater = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text(
        'Hi! Sende /menu und ich sage dir, was heute auf der Speisekarte steht. Mit /sub_daily_menu <hour> <minute> '
        'kannst du einstellen, dass ich dir an jedem Werktag automatisch um eine bestimmte Uhrzeit eine Nachricht mit '
        'dem Speiseplan schicke. Dein Abo kannst mit /show_sub überprüfen oder mit /unsub_daily_menu jederzeit '
        'widerrufen.')


def menu(bot, update):
    """Send the menu."""
    import menu
    update.message.reply_text(menu.get_menu())


def error(bot, update, error):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, error)


def callback_daily_menu(bot, job):
    import menu
    bot.send_message(job.context[0], text=menu.get_menu())


def set_daily_menu(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id

    try:
        override = False
        # If there is already a sub it will be removed and only the new sub will be used
        if 'job' in chat_data:
            job = chat_data['job']
            job.schedule_removal()
            del chat_data['job']
            override = True

        hour = int(args[0])
        minute = int(args[1])

        # Add job to queue
        import datetime
        import menu
        if menu.test_mode:
            job = job_queue.run_daily(callback_daily_menu,
                                      datetime.time(hour=hour, minute=minute),
                                      context=[chat_id, hour, minute])
        else:
            job = job_queue.run_daily(callback_daily_menu,
                                      datetime.time(hour=hour, minute=minute),
                                      days=(0, 1, 2, 3, 4),
                                      context=[chat_id, hour, minute])

        chat_data['job'] = job

        if override:
            update.message.reply_text('Erfolgreich abonniert. Dein altes Abo wurde überschrieben.')
        else:
            update.message.reply_text('Erfolgreich abonniert.')

    except (IndexError, ValueError):
        import traceback
        traceback.print_exc()
        update.message.reply_text('Es ist ein Fehler aufgetreten. Bitte probieren Sie /set_daily_menu <h> <m>')


def show_daily_menu(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('Du hast kein Abo.')
        return

    job = chat_data['job']
    hour = job.context[1]
    minute = job.context[2]
    update.message.reply_text('Du hast ein Abo für ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ' Uhr.')


def unset_daily_menu(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('Du hast kein Abo.')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Dein Abo wurde erfolgreich entfernt.')


def main():
    """Run bot."""

    if token is None:
        load_token_from_file()

    global updater
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))

    dp.add_handler(CommandHandler("menu", menu))

    dp.add_handler(CommandHandler("sub_daily_menu",
                                  set_daily_menu,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unsub_daily_menu",
                                  unset_daily_menu,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("show_sub",
                                  show_daily_menu,
                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


def load_token_from_file():
    import codecs
    import menu
    if menu.get_test_mode():
        token_file = codecs.open('./schmankerlBotDev.token', encoding='utf-8')
    else:
        token_file = codecs.open('./schmankerlBot.token', encoding='utf-8')
    global token
    token = token_file.read()
    token_file.close()


if __name__ == '__main__':
    main()
