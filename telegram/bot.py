from config import *
import telebot
from PIL import Image

bot = telebot.TeleBot(TELEGRAM_TOKEN)

#responde al conmando /strat
@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    """Da la bienvenida al usuario del bot"""
    bot.reply_to(message, "Hola!")

#Responder a los mensajes de textos que no son comandos
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    if message.text.startswith("/"): #Per a que no agafi comandes
        bot.send_message(message.chat.id, "Comanda no disponible!")
    else:
        bot.send_message(message.chat.id, "Programem!")

@bot.message_handler(content_types=["photo"])
def bot_mensajes_texto(message):

    photo_size = message.photo[-1]
    # Descargamos el archivo en un arreglo de bytes
    
    file_info = bot.get_file(photo_size.file_id)
    print(file_info.file_path)
    file_bytes = bot.download_file(file_info.file_path)
    with open("archivo_descargado.jpg", "wb") as f:
        f.write(file_bytes)

    # Descargamos la imagen en miniatura
    

    '''
    # Obtenemos el objeto File correspondiente a la imagen en miniatura
    photo_file = bot.get_file(photo_size.file_id)

    # Descargamos el archivo en un arreglo de bytes
    photo_data = photo_file.download_as_bytearray()

    # Guardamos los datos en un archivo
    with open('miniatura.jpg', 'wb') as f:
        f.write(photo_data)
    '''
    

if __name__ == '__main__':
    print('Inicialndo el bot')
    bot.infinity_polling()