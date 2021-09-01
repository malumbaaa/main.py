import telebot
from telebot import types
from geopy.distance import geodesic
import config
import requests
import json
import urllib

bot = telebot.TeleBot(config.API_TOKEN)
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
btn_address = types.KeyboardButton('Адреса магазинов', request_location=True)
btn_payment = types.KeyboardButton('Способы оплаты')
btn_delivery = types.KeyboardButton('Способы доставки')
btn_catalog = types.KeyboardButton('Каталог')
markup_menu.add(btn_address, btn_payment, btn_delivery, btn_catalog)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Наличные', callback_data='cash')
btn_in_card = types.InlineKeyboardButton('Картой', callback_data='card')
btn_in_bank = types.InlineKeyboardButton('Банкоский перевод', callback_data='bank')

markup_inline_payment.add(btn_in_bank, btn_in_card, btn_in_cash)




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    data = {"id": int(message.from_user.id), "name": message.from_user.first_name,
            "surname": message.from_user.last_name if message.from_user.last_name is not None else "Нет",
            "username": message.from_user.username}
    print(data)
    requests.post("http://127.0.0.1:8000/api/customer/", data=data)
    bot.reply_to(message, "Эй, привет! Я тестовый интернет магазин!)", reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "Способы доставки":
        bot.reply_to(message, "Доставка курьером, самовывоз, почта.", reply_markup=markup_menu)
    elif message.text == "Способы оплаты":
        bot.reply_to(message, "В наших магазинах действуют доступны следующие способы оплаты:",
                     reply_markup=markup_inline_payment)
    elif message.text == "Каталог":
        products = requests.get("http://127.0.0.1:8000/api/product/").json()
        photos = requests.get("http://127.0.0.1:8000/api/product_photo/").json()
        print(photos, "Это photos")
        for product in products:
            for photo in photos:
                if product["id"] == photo["product_id"]:
                    try:
                        f = open('out.jpg', 'wb')
                        f.write(urllib.request.urlopen(photo['url']).read())
                        f.close()
                    except urllib.error.HTTPError:
                        print("У нас тут ошибка")
                    else:
                        markup_inline_add_to_cart = types.InlineKeyboardMarkup()
                        btn_add_to_cart = types.InlineKeyboardButton('Добавить в корзину',
                                                                     callback_data=product['id'])
                        markup_inline_add_to_cart.add(btn_add_to_cart)
                        img = open('out.jpg', 'rb')
                        bot.send_photo(message.chat.id, img,
                                       caption=f"{product['name']}\n{product['description']}\n" +
                                               f"Цена: {product['price']}$", reply_markup=markup_inline_add_to_cart)
                        img.close()
                    break
        print(products)
    else:
        bot.reply_to(message, "Не могу тебя понять, напиши /help")


@bot.message_handler(func=lambda message: True, content_types=['location'])
def shop_location(message):
    lon = message.location.longitude
    lat = message.location.latitude

    distance = []
    for m in config.SHOPS:
        result = geodesic((m['latm'], m['lonm']), (lat, lon))
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Ближайший к вам магазин')
    bot.send_venue(message.chat.id, config.SHOPS[index]['latm'],
                   config.SHOPS[index]['lonm'],
                   config.SHOPS[index]['title'],
                   config.SHOPS[index]['address'])


@bot.callback_query_handler(func=lambda call: True)
def call_back_payment(call):
    products = requests.get("http://127.0.0.1:8000/api/product/").json()
    ids = [products[i]['id'] for i in range(len(products))]
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text="""
        Наличная оплата производится в рублях в кассе магазина
        """)
    elif call_back_payment == 'card':
        bot.send_message(call.message.chat.id, text="""
        Оплата производится по ссылке t.me//loveyou
      """)
    elif call_back_payment == 'bank':
        bot.send_message(call.message.chat.id, text="""
        реквизиты банка: ALFA BY63220123214213
      """)
    elif call.data in str(ids):
        print(call.data)
        url = f"http://127.0.0.1:8000/api/cart/"
        carts = requests.get(url).json()
        print(carts, "это карты")
        cart_user = {}
        for cart in carts:
            print(int(call.message.chat.id), cart['customer_id'])
            if cart['customer_id'] == call.message.chat.id:
                print(cart)
                cart_user = cart
                break

        cart_product = requests.get(f"http://127.0.0.1:8000/api/cart_product/{cart_user['id']}/").json()
        # print(cart_product)
        # requests.delete(f"http://127.0.0.1:8000/api/cart_product/{cart_user['id']}/")
        test = cart_product['product_id']
        requests.get(f"http://127.0.0.1:8000/api/cart_test/", params={"product_id": [call.data, *test],
                                                                     'cart_id': cart_user['id']},
                      headers={"Content-Type": "application/json"})
        bot.send_message(call.message.chat.id, text="Товар успешно добавлен в корзину")



bot.polling()



