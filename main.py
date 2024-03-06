import logging
import os

from telegram import Chat, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from telegram import Message, MessageEntity
from telegram.ext import CallbackContext

from vid_utils import Video

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def extract_group(message: Message, context: CallbackContext) -> tuple[str, Message]:
    """Extracts a question from a message in a group chat."""
    if (
        message.reply_to_message
        and message.reply_to_message.from_user.username == context.bot.username
    ):
        # treat a reply to the bot as a follow-up question
        question = f"+ {message.text}"
        return question, message

    mention = (
        message.entities[0]
        if message.entities and message.entities[0].type == MessageEntity.MENTION
        else None
    )
    if not mention:
        # the message is not a reply to the bot,
        # so ignore it unless it's mentioning the bot
        return "", message

    mention_text = message.text[mention.offset : mention.offset + mention.length]
    if mention_text.lower() != context.bot.name.lower():
        # the message mentions someone else
        return "", message

    # the message is mentioning the bot,
    # so remove the mention to get the question
    question = message.text[: mention.offset] + message.text[mention.offset + mention.length :]
    question = question.strip()

    # messages in topics are technically replies to the 'topic created' message
    # so we should ignore such replies
    if message.reply_to_message and not message.reply_to_message.forum_topic_created:
        # the real question is in the original message
        question = (
            f"{question}: {message.reply_to_message.text}"
            if question
            else message.reply_to_message.text
        )
        return question, message.reply_to_message

    return question, message

async def download_choosen_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.message.chat.type == Chat.PRIVATE:
        question = update.message.text
    else:
        question, message = extract_group(update.message, context)
   
    if not question:
        logger.info("No mention, ignore")
        return
    
    link = question
    
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Downloading...")

    logger.info("Start downloading")
        
    video = Video(link)
    video.download()

    with video.send() as file:
        logger.info("file {}".format(file))
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file, 'rb'))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please send video link to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN", None)
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    download_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), download_choosen_format)

    application.add_handler(start_handler)
    application.add_handler(download_handler)


    application.run_polling()
    