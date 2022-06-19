import telebot

import psycopg2

bot = telebot.TeleBot('5361629949:AAErixgFwU9mgklBEkoaYFfWrLvONexIioE')






@bot.message_handler(commands=["start"])
def start(m, res=False):
    telegram_login = m.from_user.username

    conn = psycopg2.connect(
        "postgres://gatlojkpfwfhkh:182f7ef5b5600cf03119f601a28425a011175e20981a77803451713b2549a354@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d9nqgdsn9g528l")

    cur = conn.cursor()
    cur.execute("SELECT * FROM book_sender_client WHERE telegram_login='{}' ".format(telegram_login))
    clients = cur.fetchall()

    if len(clients):
        cur.execute("UPDATE book_sender_client SET telegram_id='{}' WHERE telegram_login='{}'".format(m.chat.id, telegram_login))
        conn.commit()
        cur.close()
        bot.send_message(m.chat.id, 'Підписка створена. Відтепер ви будете отримувати нові книги.')
    else:
        bot.send_message(m.chat.id, 'Введіть свій телегам логін на стоінці вибору категій')


@bot.message_handler(commands=["check"])
def check(m, res=False):
    telegram_login = m.from_user.username

    conn = psycopg2.connect(
        "postgres://gatlojkpfwfhkh:182f7ef5b5600cf03119f601a28425a011175e20981a77803451713b2549a354@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d9nqgdsn9g528l")

    cur = conn.cursor()
    cur.execute("SELECT * FROM book_sender_client WHERE telegram_login='{}' ".format(telegram_login))
    clients = cur.fetchall()
    if len(clients):
        cur.execute("UPDATE book_sender_client SET telegram_id='{}' WHERE telegram_login='{}'".format(m.chat.id,
                                                                                                      telegram_login))
        conn.commit()
        cur.close()
        bot.send_message(m.chat.id, 'Підписка створена. Відтепер ви будете отримувати нові книги.')
    else:
        bot.send_message(m.chat.id, 'Введіть свій телегам логін на стоінці вибору категій')


@bot.message_handler(commands=["stop"])
def stop(m, res=False):
    telegram_login = m.from_user.username

    conn = psycopg2.connect(
        "postgres://gatlojkpfwfhkh:182f7ef5b5600cf03119f601a28425a011175e20981a77803451713b2549a354@ec2-34-207-12-160.compute-1.amazonaws.com:5432/d9nqgdsn9g528l")

    cur = conn.cursor()
    cur.execute("UPDATE book_sender_client SET telegram_id='' WHERE telegram_id='{}'".format(m.chat.id))
    conn.commit()
    cur.close()
    bot.send_message(m.chat.id, 'Підписка закінчена.')

bot.polling(none_stop=True, interval=0)