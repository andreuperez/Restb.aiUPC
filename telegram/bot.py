from config import *
import telebot
from PIL import Image
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
import subprocess



HOSTNAME = ""
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#responde al conmando /strat
@bot.message_handler(commands=["start"])
def cmd_start(message):
    global id
    text_html = '<b>Benvingut al Bot de Telegram!</b>' + '\n' + 'Escriviu la comanda /consulta per a realitzar una nova consulta.'  + '\n' + 'Escriviu la comanda /processar per a processar la consulta.'
    id = message.chat.id
    bot.send_message(message.chat.id, text_html, parse_mode="html", disable_web_page_preview=True)

@bot.message_handler(commands=["consulta"])
def cmd_start(message):
    markup = ForceReply()
    msg = bot.reply_to(message, "Introdueixi el codi postal", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_m2)

def preguntar_m2(message):
    global codi
    codi = message.text
    markup = ForceReply()
    msg = bot.reply_to(message, "Introdueixi els m2 de l'habitatge", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_imatges)

def preguntar_imatges(message):
    global m2
    m2 = message.text
    markup = ForceReply()
    msg = bot.reply_to(message, "Introdueixi les imatges de l'habitatge", reply_markup=markup)

@bot.message_handler(content_types=["photo"])
def bot_mensajes_texto(message):
    global names
    photo_size = message.photo[-1]
    file_info = bot.get_file(photo_size.file_id)
    print(file_info.file_path)
    file_bytes = bot.download_file(file_info.file_path)
    name = "./public/images/" + file_info.file_path.split("/")[1]
    url_name = HOSTNAME + "/images/" +  file_info.file_path.split("/")[1]
    names.append(url_name)
    print(names)
    with open(name, "wb") as f:
        f.write(file_bytes)

@bot.message_handler(commands=["processar"])
def cmd_start(message):
    global names, codi, m2, id
    # Ejecutar mi_script.py
    
    p = subprocess.Popen(["python", "restb.aiAPI.py", codi, m2] + names, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Obtener la salida del script
    out, err = p.communicate()

    # Imprimir la salida
    price = out.decode("utf-8")
    text_html = '<b>' + price + '</b>' 
    bot.send_message(id, text_html, parse_mode="html", disable_web_page_preview=True)
    names = []

    
    

if __name__ == '__main__':
    global names
    print('Iniciando el bot')
    names = list()
    bot.infinity_polling()
    