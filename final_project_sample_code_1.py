from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CommandHandler, CallbackQueryHandler
from my0511secret import token

black = '⚫️'
white = '⚪️'


def enc(board):
    # board is a dictionary mapping (row, col) to grid
    # grid = [[board.get((row, col), '') for col in range(8)] for row in range(8)]
    number = 0
    base = 3
    for row in range(8):
        for col in range(8):
            number *= base
            # if grid[row][col] == black:
            if board.get((row, col)) == black:
                number += 2
            # elif grid[row][col] == white:
            elif board.get((row, col)) == white:
                number += 1
    return str(number)


def dec(number):
    board = {}
    base = 3
    for row in [7, 6, 5, 4, 3, 2, 1, 0]:
        for col in [7, 6, 5, 4, 3, 2, 1, 0]:
            if number % 3 == 2:
                board[(row, col)] = black
            elif number % 3 == 1:
                board[(row, col)] = white
            number //= base
    return board


def board_markup(board):
    # board will be encoded and embedded to callback_data
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board.get((row, col), f'{row},{col}'), callback_data=f'{row}{col}{enc(board)}') for col in range(8)]
        for row in range(8)])


# Define a few command handlers. These usually take the two arguments update and
# context.
async def func(update, context):
    data = update.callback_query.data
    # user clicked the button on row int(data[0]) and col int(data[1])
    row = int(data[0])
    col = int(data[1])
    await context.bot.answer_callback_query(update.callback_query.id, f'你按的 row {row} col {col}')
    # TODO: check if the button is clickable. if not, report it is not clickable and return

    # the board is encoded and stored as data[2:]
    board = dec(int(data[2:]))
    board[(row, col)] = black
    # reply_markup = board_markup(board)
    await context.bot.edit_message_text('目前盤面',
                                        reply_markup=board_markup(board),
                                        chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id)

async def start(update, context):
    board = {(3,3): '⚫️', (3,4): '⚪️', (4,3): '⚪️', (4,4): '⚫️'}
    # reply_markup = board_markup(board)
    await update.message.reply_text('目前盤面', reply_markup=board_markup(board))



def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(func))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
