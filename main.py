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
btn_cart = types.KeyboardButton('Посмотреть корзину')
markup_menu.add(btn_address, btn_payment, btn_delivery, btn_catalog, btn_cart)

markup_menu2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_buy = types.KeyboardButton('Купить')
btn_main_menu = types.KeyboardButton('Главное меню')
markup_menu2.add(btn_buy, btn_main_menu)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Наличные', callback_data='cash')
btn_in_card = types.InlineKeyboardButton('Картой', callback_data='card')
btn_in_bank = types.InlineKeyboardButton('Банкоский перевод', callback_data='bank')

markup_inline_payment.add(btn_in_bank, btn_in_card, btn_in_cash)

markup_inline_delivery = types.InlineKeyboardMarkup()
btn_in_courier = types.InlineKeyboardButton('Курьером', callback_data='courier')
btn_in_post = types.InlineKeyboardButton('Почтой', callback_data='post')
btn_in_pickup = types.InlineKeyboardButton('Самовывоз', callback_data='pickup')
markup_inline_delivery.add(btn_in_courier, btn_in_post, btn_in_pickup)

ilyas_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_orders = types.KeyboardButton('Посмотреть заказы')
btn_ready_orders = types.KeyboardButton('Посмотреть выполненные заказы')
ilyas_menu.add(btn_orders, btn_ready_orders)

ilyas_inline = types.InlineKeyboardMarkup()
btn_in_send = types.InlineKeyboardButton('Отправлен', callback_data='send')
btn_in_wait = types.InlineKeyboardButton('Ожидает', callback_data='wait')
btn_in_paid = types.InlineKeyboardButton('Оплачен', callback_data='paid')
ilyas_inline.add(btn_in_send, btn_in_wait, btn_in_paid)


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    response = requests.get(f"http://127.0.0.1:8000/api/customer/{int(message.from_user.id)}/",
                            headers={"Content-type": "application/json"})
    if response.status_code == 404:
        data = {"id": int(message.from_user.id), "name": message.from_user.first_name,
                "surname": message.from_user.last_name if message.from_user.last_name is not None else "Нет",
                "username": message.from_user.username}
        requests.post("http://127.0.0.1:8000/api/customer/", data=data)
        requests.post("http://127.0.0.1:8000/api/cart/", json={"customer_id": data['id']})
    if message.chat.id == config.ilyas_id:
        bot.reply_to(message, "Здарова, пидрилкин", reply_markup=ilyas_menu)
    else:
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
        view_products(products, photos, message.chat.id, 'Добавить в корзину')
    elif message.text == "Посмотреть корзину":
        check_cart(message)
    elif message.text == "Главное меню":
        bot.reply_to(message, "Возвращаемся", reply_markup=markup_menu)
    elif message.text == "Купить":
        bot.send_message(message.chat.id, "Выберите способ доставки:",
                         reply_markup=markup_inline_delivery)
    elif message.text == "Посмотреть заказы" and message.chat.id == config.ilyas_id:
        response = requests.get("http://127.0.0.1:8000/api/order/").json()
        for order in response:
            if order['status'] != 'Оплачен':
                goods = "Вещи:\n"
                for product in order['products']:
                    product_response = requests.get(f"http://127.0.0.1:8000/api/product/{product}/").json()
                    goods += f'{product_response["id"]} {product_response["name"]}\n'
                bot.send_message(message.chat.id,
                                 f"""Пользователь {(requests.get(f"http://127.0.0.1:8000/api/customer/{order['user_id']}").json())["name"]}
                                  {goods} Заработок: {order['money']}$
                                  Дата поступления заказа: {order['date_come']}
                                  Статус: {order['status']}""", reply_markup=ilyas_inline)
    elif message.text == "Посмотреть выполненные заказы" and message.chat.id == config.ilyas_id:
        response = requests.get("http://127.0.0.1:8000/api/order/").json()
        for order in response:
            if order['status'] == 'Оплачен':
                goods = "Вещи:\n"
                for product in order['products']:
                    product_response = requests.get(f"http://127.0.0.1:8000/api/product/{product}/").json()
                    goods += f'{product_response["id"]} {product_response["name"]}\n'
                bot.send_message(message.chat.id,
                                 f"""Пользователь {(requests.get(f"http://127.0.0.1:8000/api/customer/{order['user_id']}").json())["name"]}
                                         {goods} Заработок: {order['money']}$
                                         Дата поступления заказа: {order['date_come']}
                                         Дата выполнения заказа: {order['date_out']}
                                         Статус: {order['status']}""")
    else:
        bot.reply_to(message, "Не могу тебя понять, напиши /help")


@bot.message_handler(func=lambda message: True, content_types=['location'])
async def shop_location(message):
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
        mode = ''
        text = ''
        if call.message.reply_markup.to_dict()['inline_keyboard'][0][0]['text'] == 'Добавить в корзину':
            mode = 'update'
            text = "Товар успешно добавлен в корзину"
        elif call.message.reply_markup.to_dict()['inline_keyboard'][0][0]['text'] == 'Убрать из корзины':
            mode = 'remove'
            text = "Товар успешно убран из корзину"
        url = f"http://127.0.0.1:8000/api/cart/"
        carts = requests.get(url).json()
        cart_user = {}
        for cart in carts:
            if cart['customer_id'] == call.message.chat.id:
                cart_user = cart
                break
        response = requests.put(f"http://127.0.0.1:8000/api/cart_product/{cart_user['id']}/", json={"product_id": [int(call.data)],
                                                                                                    "cart_id": cart_user['id'],
                                                                                                    "mode": mode},
                                headers={"Content-type": "application/json"})
        if response.status_code == 404:
            response = requests.post(f"http://127.0.0.1:8000/api/cart_product/", json={"product_id": [int(call.data)],
                                                                                       "cart_id": cart_user['id']},
                                     headers={"Content-type": "application/json"})
        if mode == 'update':
            bot.send_message(call.message.chat.id, text=text, reply_markup=markup_menu)
        if mode == 'remove':
            bot.send_message(call.message.chat.id, text=text, reply_markup=markup_menu2)
            check_cart(call.message)
    elif call.data in ['courier', 'post', 'pickup']:
        url = f"http://127.0.0.1:8000/api/cart/"
        carts = requests.get(url).json()
        cart_user = {}
        for cart in carts:
            if cart['customer_id'] == call.message.chat.id:
                cart_user = cart
                break
        cart = requests.get(f"http://127.0.0.1:8000/api/cart_product/{cart_user['id']}/").json()
        response = requests.post("http://127.0.0.1:8000/api/order/", json={"user_id": call.message.chat.id,
                                                                           "products": cart['product_id'],
                                                                           "status": "Поступил",
                                                                           "delivery": call.data})
        requests.delete(f"http://127.0.0.1:8000/api/cart_product/{cart_user['id']}/")
        if call.data == "courier" or call.data == "post":
           bot.send_message(call.message.chat.id, "Введите ваш адрес: ")
        else:
            bot.send_message(call.message.chat.id, "Ваш заказ успешно принят")
        print(response)
        print(response.content)
    elif call.data in ["send", "wait", "paid"]:
        print(call.message.text)



def view_products(products, photos, chat_id, message_markup):
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
                    btn_add_to_cart = types.InlineKeyboardButton(message_markup,
                                                                 callback_data=product['id'])
                    markup_inline_add_to_cart.add(btn_add_to_cart)
                    img = open('out.jpg', 'rb')
                    bot.send_photo(chat_id, img,
                                   caption=f"{product['name']}\n{product['description']}\n" +
                                           f"Цена: {product['price']}$", reply_markup=markup_inline_add_to_cart)
                    img.close()
                break


def check_cart(message):
    url = f"http://127.0.0.1:8000/api/cart/"
    carts = requests.get(url).json()
    cart_user = {}
    for cart in carts:
        print(int(message.chat.id), cart['customer_id'])
        if cart['customer_id'] == message.chat.id:
            cart_user = cart
            break
    cart = requests.get(f"http://127.0.0.1:8000/api/cart_product/{cart_user['id']}/").json()
    products = []
    try:
        products = [requests.get(f"http://127.0.0.1:8000/api/product/{product_id}/").json() for product_id in
                    cart['product_id']]
    except KeyError:
        pass
    photos = requests.get("http://127.0.0.1:8000/api/product_photo/").json()
    view_products(products, photos, message.chat.id, 'Убрать из корзины')
    if bool(products):
        bot.send_message(message.chat.id, text="Ваша корзина", reply_markup=markup_menu2)
    else:
        bot.send_message(message.chat.id, text="Ваша корзина пуста", reply_markup=markup_menu)


bot.polling()



