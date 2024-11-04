import subprocess
import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime
import server
from config import TOKEN, AUTHORIZED_USERS, EXCLUSIVE, USE_PROXIES

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Should make this a Database probably
    with open(f'{os.path.dirname(__file__)}/user_ids','a') as file:
        file.write(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} {update.effective_chat.first_name}, {update.effective_chat.username}, {update.effective_chat.id}\n")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The Commands are:\n*/cube*\n*/train*\n*/merge*\n*/twerk*\n*/poly*\n*/trim*\n*/cafe*\n*/zoo*\n*/tile*\n"
                    "*/fluff*\n*/stone*\n*/bounce*\n*/hide*\n*/pin*\n*/count*\n*/infect*\n*/water*\n*/factory*\n*/all*"
                    "\nThese will generate 4 keys for their respective games\\.",
        parse_mode='MARKDOWNV2'
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You can also set how many keys are generated\\. For example, */cube 8* will generate *EIGHT* keys for the cube game\\.",
        parse_mode='MARKDOWNV2'
        )

async def game_handler(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    chosen_game: int, 
    all: bool, 
    delay = 0
    ):
    if EXCLUSIVE and not update.effective_chat.id in AUTHORIZED_USERS:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Clone this bot from the [github](https://github.com/Emperor-One/Hamster-Key-Telegram-Bot) repo and follow the instructions to create your own bot in seconds\\.",
            parse_mode='MARKDOWNV2'
        )
        with open(f'{os.path.dirname(__file__)}/unauthorized','a') as file:
            unauthorized_message = f"Unauthorized User: {update.effective_chat.first_name} - {update.effective_chat.username}: {update.effective_chat.id}"
            server.logger.warning(unauthorized_message)
            file.write(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} {unauthorized_message}\n")
        return

    # delay for the /all command
    await asyncio.sleep(delay)
    server.logger.info(f"Delay for {delay} seconds")


    server.logger.info(f"Generating for client: {update.effective_chat.first_name} - {update.effective_chat.username}: {update.effective_chat.id}")
    if not all:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating\\.\\.\\.", parse_mode='MARKDOWNV2')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"This will only take a moment\\.\\.\\.", parse_mode='MARKDOWNV2')


    key_count = 0
    no_of_keys = int(context.args[0]) if context.args else 4

    async for key in server.run(chosen_game=chosen_game, no_of_keys=no_of_keys, use_proxies=USE_PROXIES):
        formatted_key = f"`{key}`"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{key_count + 1}\\. {formatted_key}", parse_mode='MARKDOWNV2')
        server.logger.info(f"Message sent to client: {update.effective_chat.first_name} - {update.effective_chat.username}: {update.effective_chat.id}")
        key_count += 1

async def cube(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=1, all=all)

async def train(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=2, all=all)

async def merge(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=3, all=all)

async def twerk(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=4, all=all)

async def poly(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=5, all=all)

async def trim(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=6, all=all)

async def zoo(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=7, all=all)

async def tile(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=8, all=all)

async def fluff(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=9, all=all)

async def stone(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=10, all=all)

async def bounce(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=11, all=all)

async def hide(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=12, all=all)

async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=13, all=all)

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=14, all=all)

async def infect(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=15, all=all)

async def water(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=16, all=all)

async def factory(update: Update, context: ContextTypes.DEFAULT_TYPE, all = False):
    await game_handler(update, context, chosen_game=17, all=all)

async def all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if EXCLUSIVE and not update.effective_chat.id in AUTHORIZED_USERS:
        return
    
    server.logger.info(f"Generating ALL GAMES for client: {update.effective_chat.first_name} - {update.effective_chat.username}: {update.effective_chat.id}")

    await context.bot.send_message(chat_id=update.effective_chat.id, text="🐹")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Currently generating for all games\\.\\.\\.", parse_mode='MARKDOWNV2')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Come Back in about 5\\-10 minutes\\.", parse_mode='MARKDOWNV2')

    # Wait a certain number of seconds between each game
    tasks = [game_handler(update, context, i + 1, True, i * 30) for i in range(len(server.GAMES))]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    server.logger.info("Server is running. Awaiting users...")

    application.add_handler(CommandHandler('start', start, block=False))
    application.add_handler(CommandHandler('cube', cube, block=False))
    application.add_handler(CommandHandler('train', train, block=False))
    application.add_handler(CommandHandler('merge', merge, block=False))
    application.add_handler(CommandHandler('twerk', twerk, block=False))
    application.add_handler(CommandHandler('poly', poly, block=False))
    application.add_handler(CommandHandler('trim', trim, block=False))
    application.add_handler(CommandHandler('zoo', zoo, block=False))
    application.add_handler(CommandHandler('tile', tile, block=False))
    application.add_handler(CommandHandler('fluff', fluff, block=False))
    application.add_handler(CommandHandler('stone', stone, block=False))
    application.add_handler(CommandHandler('bounce', bounce, block=False))
    application.add_handler(CommandHandler('hide', hide, block=False))
    application.add_handler(CommandHandler('pin', pin, block=False))
    application.add_handler(CommandHandler('count', count, block=False))
    application.add_handler(CommandHandler('infect', infect, block=False))
    application.add_handler(CommandHandler('water', water, block=False))
    application.add_handler(CommandHandler('factory', factory, block=False))


    application.add_handler(CommandHandler('all', all, block=False))


    application.run_polling()
