import os
import ast
import operator
import telebot

TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def calc(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in ops:
        return ops[type(node.op)](calc(node.left), calc(node.right))

    if isinstance(node, ast.UnaryOp) and type(node.op) in ops:
        return ops[type(node.op)](calc(node.operand))

    raise ValueError("Invalid expression")


@bot.message_handler(func=lambda message: True)
def calculator(message):
    try:
        result = calc(ast.parse(message.text, mode="eval").body)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        bot.reply_to(message, f"Result = {result}")
    except:
        pass


print("Calculator Bot is running...")
bot.infinity_polling()
