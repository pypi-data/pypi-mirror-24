import logging

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from .channel import Channel


class Manager(object):
    channels = {}
    env = 'dev'
    host = '0.0.0.0'
    port = 5000
    webhook_url = "https://your-app.herokuapp.com/0"

    def __init__(self, token: str):
        self.token = token
        self.logger = logging.getLogger(self.__class__.__name__)
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.chosen_channel = None

    def config(self, env=None, host=None, port=None, webhook_url=None):
        if env:
            self.env = env
        if host:
            self.host = host
        if port:
            self.port = port
        if webhook_url:
            self.webhook_url = webhook_url

    def register(self, channel_class: Channel.__class__):
        channel = channel_class(self.updater)
        self.channels[channel.name] = channel
        return self

    def activate(self):
        for name, channel in self.channels.items():
            channel.start_posting()

    def set_up_commands(self):
        commands = {
            'start': self.command_help,
            'help': self.command_help,
            'list': self.command_list,
            'choose': self.command_choose,
        }
        for name, command in commands.items():
            self.dispatcher.add_handler(CommandHandler(name, command))
        self.dispatcher.add_handler(CallbackQueryHandler(self.command_accept_choice))
        self.dispatcher.add_error_handler(self.command_error)

    def start(self):
        self.activate()
        self.set_up_commands()

        if self.env == 'prod':
            self.start_webhook()
        elif self.env == 'dev':
            self.start_polling()
        else:
            self.logger.error('unknown env type')

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def start_webhook(self):
        self.updater.start_webhook(listen=self.host, port=self.port,
                                   url_path=self.token)
        self.updater.bot.set_webhook(self.webhook_url)
        self.updater.idle()

    def command_help(self, bot: Bot, update: Update):
        text = "/help or /start - print this message.\n" \
               "/choose - choose channels.\n" \
               "/list - print list of available channels.\n"
        if self.chosen_channel:
            channel_text = self.chosen_channel.help_text() or ' - no commands'
            text += f"\n`{self.chosen_channel.name}` commands:\n" + channel_text
        bot.send_message(chat_id=update.message.chat_id,
                         text=text, parse_mode=ParseMode.MARKDOWN)

    def command_list(self, bot: Bot, update: Update):
        del bot
        text = 'Channels list:\n'
        for name, channel in self.channels.items():
            text += f' - {name}\n'
        update.message.reply_text(text)

    def command_choose(self, bot: Bot, update: Update):
        channels = []
        for name, channel in self.channels.items():
            button = InlineKeyboardButton(text=name, callback_data=name)
            channels.append(button)

        keyboard = [channels]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(chat_id=update.message.chat_id,
                         text='Choose channel.',
                         reply_markup=reply_markup)

    def command_accept_choice(self, bot: Bot, update: Update):
        query = update.callback_query
        if self.chosen_channel:
            self.chosen_channel.remove_commands_handlers()
        self.chosen_channel: Channel = self.channels[query.data]
        self.chosen_channel.add_commands_handlers()
        bot.edit_message_text(text=f'Channel "{query.data}" was chosen.',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        update.message = query.message  # because callback update doesn't have message at all,
        self.command_help(bot, update)  # whereas command_help use message.chat_id

    def command_error(self, bot: Bot, update: Update, error):
        del bot
        self.logger.warning('Update "%s" caused error "%s"' % (update, error))
