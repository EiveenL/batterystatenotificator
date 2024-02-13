import telebot
import psutil
from telebot import types
import requests

#Conexion con nuestro BOT

TOKEN = '6974390425:AAF3gGw_eTZ-8uGPkVPpH5frxGQUWi9BW4M'
API_KEY = 'cbe62b0404c921605b7b76073e593a55'

bot = telebot.TeleBot(TOKEN)
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# Función para obtener el porcentaje de la batería
def obtener_porcentaje_bateria():
    return psutil.sensors_battery().percent

def get_weather(city_name):
    complete_url = BASE_URL + "q=" + city_name + "&appid=" + API_KEY
    response = requests.get(complete_url)
    data = response.json()
    print(data)
    if data["cod"] != 404:
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"] - 273.15
        description = weather_data["description"]
        return f"Temperatura: {temperature:.2f}°C\n{description.capitalize()}"
    else:
        return 'Ciudad no encontrada'

@bot.message_handler(commands=['clima'])
def send_weather(message):
    city_name = message.text.split()[1] if len(message.text.split()) > 1 else None
    if city_name:
        weather_info = get_weather(city_name)
        bot.reply_to(message, weather_info)
    else:
        bot.reply_to(message, "Por favor, proporciona el nombre de la ciudad. Ejemplo: /clima Madrid")


#Creacion de comandos simples como `/start` y `/help`
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hola! Soy tu primer bot creado con Telebot')



@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Puedes interactuar conmigo usando comandos. Por ahora, solo respondo a /start y /help')

@bot.message_handler(commands=['minecraft'])
def send_options(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    #Creando botones
    btn_si = types.InlineKeyboardButton('Si', callback_data='mine_si')
    btn_no = types.InlineKeyboardButton('No', callback_data='mine_no') 


    #Agrega botones al markup
    markup.add(btn_si, btn_no)


    #Enviar mensaje con los botones
    bot.send_message(message.chat.id, "¿Te gusta minecraft?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data == 'mine_si':
        bot.answer_callback_query(call.id, '¡A mi tambien!')
    elif call.data == 'mine_no':
        bot.answer_callback_query(call.id, '¡Bueno cada uno tienes sus gustos!')

@bot.message_handler(commands=['bateria'])
def verificar_bateria(message):
    porcentaje = obtener_porcentaje_bateria()

    if porcentaje == 100:
        bot.reply_to(message, "¡Batería cargada al 100%! ")
    elif porcentaje <= 20:
        bot.reply_to(message, "¡Atención! La batería está al " + str(porcentaje) + "%. ¡Conecta el cargador! ")
    else:
        bot.reply_to(message, "El porcentaje actual de la batería es " + str(porcentaje) + "%.")


@bot.message_handler(commands=['foto'])
def send_image(message):
    img_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png'
    bot.send_photo(chat_id=message.chat.id, photo=img_url, caption='Aqui tienes tu imagen')


if __name__ == "__main__":
    bot.polling(none_stop=True)