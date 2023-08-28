from googletrans import Translator
import json
import telebot
from telebot import types
from langdetect import detect
from background import keep_alive
from langdetect import DetectorFactory
import schedule
import time
from threading import Thread
#MON AMI
translate = Translator()
users = []

akk = ''
DetectorFactory.seed = 0
with open('users.json', 'r') as read_users:
  users = json.load(read_users)
print(users)
messagesGroups = []
bot = telebot.TeleBot('6121254022:AAFhAdnFxD11lhr9oiA1dGLuOpDLdeDue6Q')
translator = Translator()

id_admin_Bo = 1011139757
id_admin_Ol = 740669427


@bot.message_handler(commands=['start'])
def first_message(message):
  text = f'''
Привет!
Бот создан для удобсва обучения французскому. Он может переводить сообщения с русского на французский и наоборот. В боте вы сможете быстро записаться к репетитору Ольге, также вы будете получать рассылку с напоминаниями о занятиях. Если бот не отвечает — перезапустите его, введя команду /start
  '''
  bot.send_message(message.chat.id, text)
  first_page(message)

@bot.message_handler(content_types=['text'])
def first_page(message):
  text = 'Вы на главной странице'
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton('Аккаунт')
  btn2 = types.KeyboardButton('Регистрация')
  btn3 = types.KeyboardButton('Переводчик')
  markup.add(btn1, btn2, btn3)
  bot.send_message(message.chat.id,
                   text,
                   parse_mode='html',
                   reply_markup=markup)
  bot.register_next_step_handler(message, click)


@bot.message_handler(content_types=['text'])
def click(message):
  if (message.text == 'Аккаунт'):
    account(message)
  elif (message.text == 'Переводчик'):
    translatoring(message)
  elif (message.text == 'Регистрация'):
    registrator(message)

@bot.message_handler(content_types=['text'])
def account(message):
  print(message.text)
  global akk
  akk = ''
  i = 0
  id = message.chat.id

  for i in range(len(users)):

    if (users[i]['ID'] == id):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton('Изменить данные')
      btn2 = types.KeyboardButton('На главную')
      markup.add(btn1, btn2)
      akk = f'''
Имя: {users[i]['Name']}
Фамилия: {users[i]['LastName']}
Возраст:{users[i]['Age']}
Номер телефона:{users[i]['Phone_Number']}
Тариф: {users[i]['Tarif']}
'''
      bot.send_message(message.chat.id,
                       akk,
                       parse_mode='html',
                       reply_markup=markup)
      break
    else:
      continue
  if (akk == ''):
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('На главную')
    markup2.add(btn2)
    akk = 'У вас пока нет аккаунта, зарегестрируйтесь'
    bot.send_message(message.chat.id,
                     akk,
                     parse_mode='html',
                     reply_markup=markup2)
  bot.register_next_step_handler(message, account_page2)


@bot.message_handler(content_types=['text'])
def account_page2(message):
  if (message.text == 'На главную'):
    first_page(message)
  elif (message.text == 'Изменить данные'):
    account_page3(message)


@bot.message_handler(content_types=['text'])
def account_page3(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton('Изменить имя')
  btn2 = types.KeyboardButton('Изменить фамилию')
  btn3 = types.KeyboardButton('Изменить возраст')
  btn4 = types.KeyboardButton('Изменить номер телефона')
  btn5 = types.KeyboardButton('Изменить тариф')
  btn6 = types.KeyboardButton('На главную')
  markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
  bot.send_message(message.chat.id,
                   'Какие данные хотите заменить?',
                   parse_mode='html',
                   reply_markup=markup)
  bot.register_next_step_handler(message, account_page4)


@bot.message_handler(content_types=['text'])
def account_page4(message):
  if (message.text == 'Изменить имя'):
    btn1(message)
  elif (message.text == 'Изменить фамилию'):
    btn2(message)
  elif (message.text == 'Изменить возраст'):
    btn3(message)
  elif (message.text == 'Изменить номер телефона'):
    btn4(message)
  elif (message.text == 'Изменить тариф'):
    btn5(message)
  elif (message.text == 'На главную'):
    btn6(message)


@bot.message_handler(content_types=['text'])
def btn1(message):
  bot.send_message(message.chat.id, 'Введите новое имя')
  bot.register_next_step_handler(message, namechange)


@bot.message_handler(content_types=['text'])
def namechange(message):
  i = 0
  id = message.chat.id
  global anket1
  for i in range(len(users)):
    if (users[i]['ID'] == id):
      old_name = users[i]['Name']
      users[i]['Name'] = message.text
      anket1 = f'''ПОЛЬЗОВАТЕЛЬ ИЗМЕНИЛ ИМЯ❗❗❗❗
Имя: {users[i]['Name']}
Старое имя: {old_name}
Фамилия: {users[i]['LastName']}
Возраст:{users[i]['Age']}
Номер телефона:{users[i]['Phone_Number']}
Тариф: {users[i]['Tarif']}
'''
      bot.send_message(message.chat.id, "Вы успешно изменили имя")
      with open('users.json', 'w') as users_write:
        json.dump(users, users_write, ensure_ascii=False)
      bot.send_message(id_admin_Bo, anket1)
      account_page3(message)
      break
    else:
      continue


@bot.message_handler(content_types=['text'])
def btn2(message):
  bot.send_message(message.chat.id, 'Введите новую фамилию')
  bot.register_next_step_handler(message, lastnamechange)


@bot.message_handler(content_types=['text'])
def lastnamechange(message):
  i = 0
  id = message.chat.id
  global anket2
  for i in range(len(users)):
    if (users[i]['ID'] == id):
      old_lastname = users[i]['LastName']
      users[i]['LastName'] = message.text
      anket2 = f'''ПОЛЬЗОВАТЕЛЬ ИЗМЕНИЛ ФАМИЛИЮ❗❗❗❗
Имя: {users[i]['Name']}
Фамилия: {users[i]['LastName']}
Старая фамилия: {old_lastname}
Возраст:{users[i]['Age']}
Номер телефона:{users[i]['Phone_Number']}
Тариф: {users[i]['Tarif']}
'''
      bot.send_message(message.chat.id, "Вы успешно изменили фамилию")
      with open('users.json', 'w') as users_write:
        json.dump(users, users_write, ensure_ascii=False)
      bot.send_message(id_admin_Bo, anket2)
      account_page3(message)
      break
    else:
      continue


@bot.message_handler(content_types=['text'])
def btn3(message):
  bot.send_message(message.chat.id, 'Введите новый возраст')
  bot.register_next_step_handler(message, agechange)


@bot.message_handler(content_types=['text'])
def agechange(message):
  i = 0
  id = message.chat.id
  global anket3
  for i in range(len(users)):
    if (users[i]['ID'] == id):
      old_age = users[i]['Age']
      users[i]['Age'] = message.text
      anket3 = f'''ПОЛЬЗОВАТЕЛЬ ИЗМЕНИЛ ВОЗРАСТ❗❗❗❗
Имя: {users[i]['Name']}
Фамилия: {users[i]['LastName']}
Возраст:{users[i]['Age']}
Старый возраст: {old_age}
Номер телефона:{users[i]['Phone_Number']}
Тариф: {users[i]['Tarif']}
'''
      bot.send_message(message.chat.id, "Вы успешно изменили возраст")
      with open('users.json', 'w') as users_write:
        json.dump(users, users_write, ensure_ascii=False)
      bot.send_message(id_admin_Bo, anket3)
      account_page3(message)
      break
    else:
      continue


@bot.message_handler(content_types=['text'])
def btn4(message):
  bot.send_message(message.chat.id, 'Введите новую номер телефона')
  bot.register_next_step_handler(message, phonechange)


@bot.message_handler(content_types=['text'])
def phonechange(message):
  i = 0
  id = message.chat.id
  global anket4
  for i in range(len(users)):
    if (users[i]['ID'] == id):
      old_phone = users[i]['Phone_Number']
      users[i]['Phone_Number'] = message.text
      anket4 = f'''ПОЛЬЗОВАТЕЛЬ ИЗМЕНИЛ НОМЕР ТЕЛЕФОНА❗❗❗❗
Имя: {users[i]['Name']}
Фамилия: {users[i]['LastName']}
Возраст:{users[i]['Age']}

Номер телефона:{users[i]['Phone_Number']}
Старый номер телефона: {old_phone}
Тариф: {users[i]['Tarif']}
'''
      bot.send_message(message.chat.id, "Вы успешно изменили номер телефона")
      with open('users.json', 'w') as users_write:
        json.dump(users, users_write, ensure_ascii=False)
      bot.send_message(id_admin_Bo, anket4)
      account_page3(message)
      break
    else:
      continue


@bot.message_handler(content_types=['text'])
def btn5(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton('Разговорный клуб')
  btn2 = types.KeyboardButton('Индивидуальные занятия')
  btn3 = types.KeyboardButton('Групповые занятия')
  markup.add(btn1, btn2, btn3)
  bot.send_message(message.chat.id,
                   'Выберите новый тариф',
                   parse_mode='html',
                   reply_markup=markup)
  bot.register_next_step_handler(message, tarifchange)


@bot.message_handler(content_types=['text'])
def tarifchange(message):
  i = 0
  id = message.chat.id
  global anket5
  for i in range(len(users)):
    if (users[i]['ID'] == id):
      old_tarif = users[i]['Tarif']
      users[i]['Tarif'] = message.text
      anket5 = f'''ПОЛЬЗОВАТЕЛЬ ИЗМЕНИЛ ТАРИФ❗❗❗❗
Имя: {users[i]['Name']}
Фамилия: {users[i]['LastName']}
Возраст:{users[i]['Age']}
Номер телефона:{users[i]['Phone_Number']}
Тариф: {users[i]['Tarif']}
Старый тариф:{old_tarif}
'''
      bot.send_message(message.chat.id, "Вы успешно изменили тариф")
      with open('users.json', 'w') as users_write:
        json.dump(users, users_write, ensure_ascii=False)
      bot.send_message(id_admin_Bo, anket5)
      account_page3(message)
      break
    else:
      continue


@bot.message_handler(content_types=['text'])
def btn6(message):
  first_page(message)


@bot.message_handler(content_types=['text'])
def translatoring(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btnFirst1 = types.KeyboardButton('На главную')
  btnFirst2 = types.KeyboardButton('рус --> франц')
  btnFirst3 = types.KeyboardButton('франц --> рус')
  markup.add(btnFirst1, btnFirst2, btnFirst3)
  bot.send_message(message.chat.id,
                   'Выберите режим перевода',
                   parse_mode='html',
                   reply_markup=markup)
  bot.register_next_step_handler(message, trans)

@bot.message_handler(content_types=['text'])
def trans(message):
  if (message.text == 'На главную'):
    first_page(message)
  elif (message.text == 'рус --> франц'):
    rusfrobb(message)
  elif (message.text == 'франц --> рус'):
    frrusobb(message)

@bot.message_handler(content_types=['text'])
def rusfrobb(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btnFirst1 = types.KeyboardButton('На главную')
  btnFirst2 = types.KeyboardButton('Поменять режим перевода')
  markup.add(btnFirst1, btnFirst2)
  bot.send_message(message.chat.id,'Введите слово или предложение, ваш режим — рус --> франц' , parse_mode='html', reply_markup=markup)
  bot.register_next_step_handler(message, rusfr)
def rusfr(message):
  if(message.text == 'На главную'):
    first_page(message)
  elif(message.text == 'Поменять режим перевода'):
    translatoring(message)
  else: 
    translated_text = translator.translate(message.text, src='ru', dest='fr')
    bot.send_message(message.chat.id, translated_text.text)
    rusfrobb(message)
    
@bot.message_handler(content_types=['text'])
def frrusobb(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btnFirst1 = types.KeyboardButton('На главную')
  btnFirst2 = types.KeyboardButton('Поменять режим перевода')
  markup.add(btnFirst1, btnFirst2)
  bot.send_message(message.chat.id,'Введите слово или предложение, ваш режим — франц --> рус' , parse_mode='html', reply_markup=markup)
  bot.register_next_step_handler(message, frrus)
def frrus(message):
  if(message.text == 'На главную'):
    first_page(message)
  elif(message.text == 'Поменять режим перевода'):
    translatoring(message)
  else: 
    translated_text = translator.translate(message.text, src='fr', dest='ru')
    bot.send_message(message.chat.id, translated_text.text)
    frrusobb(message)
@bot.message_handler(content_types=['text'])
def registrator(message):
  yet = 0
  for i in range(len(users)):
    user = users[i]
    print(user)
    if (user['ID'] != message.chat.id):
      continue
    else:
      yet += 1
    i += 1
  print(yet)
  if (yet == 0):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     'Вы хотите записаться на занятие?',
                     parse_mode='html',
                     reply_markup=markup)
    bot.register_next_step_handler(message, reg_form)
  else:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('На главную')
    markup.add( btn2)
    bot.send_message(message.chat.id,
                     'У вас уже есть тариф, вы можете поменять его в разделе аккаунт', parse_mode='html',
                     reply_markup=markup)
    bot.register_next_step_handler(message, first_page)

@bot.message_handler(content_types=['text'])
def rereg(message):
  if (message.text == 'Изменить тариф'):
    markup_tarif = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Разговорный клуб')
    btn2 = types.KeyboardButton('Индивидуальные занятия')
    btn3 = types.KeyboardButton('Групповые занятия')
    markup_tarif.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     f'''Выберите тариф
Разговорный клуб:
  ⭕400 руб / 30 минут

Индивидуальные занятия:
  ⭕500 руб / 30 минут
  ⭕1000 руб / 1 час

Групповые занятия:
  ⭕700 руб/ 1 час
                   ''',
                     parse_mode='html',
                     reply_markup=markup_tarif)
    bot.register_next_step_handler(message, rereg_Admin)
  elif (message.text == 'Назад'):
    first_page(message)

@bot.message_handler(content_types=['text'])
def reg_form(message):
  markup_del = types.ReplyKeyboardRemove()
  if (message.text == 'Да'):
    bot.send_message(message.chat.id, 'Отлично', reply_markup=markup_del)
    form1(message)
  elif (message.text == 'Назад'):
    bot.send_message(message.chat.id,
                     'Жаль что вы не записались на занятие',
                     reply_markup=markup_del)
    first_page(message)
  else:
    bot.send_message(message.chat.id,
                     'Я вас не понял',
                     reply_markup=markup_del)
    registrator(message)

@bot.message_handler(content_types=['text'])
def rereg_Admin(message):
  markup_del = types.ReplyKeyboardRemove()
  global ankets2
  global oldtarif
  id = message.chat.id
  global userrereg
  print(users)
  for i in range(len(users)):
    if (users[i]['ID'] == id):
      oldtarif = users[i]['Tarif']
      users[i]['Tarif'] = message.text
      ankets2 = f'''ПОЛЬЗОВАТЕЛЬ ИЗМЕНИЛ ТАРИФ❗❗❗❗
Имя: {users[i]['Name']}
Фамилия: {users[i]['LastName']}
Возраст:{users[i]['Age']}
Номер телефона:{users[i]['Phone_Number']}
Старый тариф: {oldtarif}
Новый тариф: {users[i]['Tarif']}
'''
      break
    else:
      continue
  print(users)
  with open('users.json', 'w') as users_write:
    json.dump(users, users_write, ensure_ascii=False)
  bot.send_message(id_admin_Bo, ankets2)
  markup_del = types.ReplyKeyboardRemove()
  bot.send_message(id, 'Тариф успешно изменен', reply_markup=markup_del)
  first_page(message)

@bot.message_handler(content_types=['text'])
def form1(message):
  markup = types.ReplyKeyboardMarkup()
  btn1 = types.KeyboardButton('На главную')
  markup.add(btn1)
  bot.send_message(message.chat.id,
                   'Введите ваше имя',
                   parse_mode='html',
                   reply_markup=markup)

  bot.register_next_step_handler(
    message,
    form2,
  )

@bot.message_handler(content_types=['text'])
def form2(message):
  global firstName
  firstName = message.text
  if (message.text == 'На главную'):
    bot.send_message(message.chat.id, "Регистрация на занятие отменена")
    first_page(message)
  else:
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('На главную')
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     'Введите вашу фамилию',
                     parse_mode='html',
                     reply_markup=markup)

    bot.register_next_step_handler(message, form3)

@bot.message_handler(content_types=['text'])
def form3(message):
  global lastName
  lastName = message.text
  if (message.text == 'На главную'):
    bot.send_message(message.chat.id, "Регистрация на занятие отменена")
    first_page(message)
  else:
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('На главную')
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     'Укажите ваш возраст',
                     parse_mode='html',
                     reply_markup=markup)

    bot.register_next_step_handler(message, form4)

@bot.message_handler(content_types=['text'])
def form4(message):
  global age
  age = message.text
  if (message.text == 'На главную'):
    bot.send_message(message.chat.id, "Регистрация на занятие отменена")
    first_page(message)
  else:
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('На главную')
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     'Укажите контактный номер телефона',
                     parse_mode='html',
                     reply_markup=markup)
    bot.register_next_step_handler(message, form5)

@bot.message_handler(content_types=['text'])
def form5(message):
  global phone_number
  if (message.text == 'На главную'):
    bot.send_message(message.chat.id, "Регистрация на занятие отменена")
    first_page(message)
  else:
    markup_tarif = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Разговорный клуб')
    btn2 = types.KeyboardButton('Индивидуальные занятия')
    btn3 = types.KeyboardButton('Групповые занятия')
    btn4 = types.KeyboardButton('На главную')
    markup_tarif.add(btn1, btn2, btn3, btn4)
    phone_number = message.text
    bot.send_message(message.chat.id,
                     f'''Выберите тариф
Разговорный клуб:
  ⭕400 руб / 30 минут
  
Индивидуальные занятия:
  ⭕500 руб / 30 минут
  ⭕1000 руб / 1 час
  
Групповые занятия:
  ⭕700 руб/ 1 час
                     ''',
                     parse_mode='html',
                     reply_markup=markup_tarif)
    bot.register_next_step_handler(message, form6)

@bot.message_handler(content_types=['text'])
def form6(message):
  if (message.text == 'На главную'):
    bot.send_message(message.chat.id, "Регистрация на занятие отменена")
    first_page(message)
  else:
    global tarif
    tarif = message.text
    if (message):
      bot.send_message(message.chat.id, 'Вы успешно записались на занятие')
      add_admin(message)

@bot.message_handler(content_types=['text'])
def add_admin(message):

  ankets = f'''НОВАЯ ЗАПИСЬ НА ЗАНЯТИЕ❗❗❗❗
Имя: {firstName}
Фамилия: {lastName}
Возраст:{age}
Номер телефона:{phone_number}
Тариф: {tarif}
'''
  user = {
    'ID': message.chat.id,
    'Name': firstName,
    'LastName': lastName,
    'Age': age,
    'Phone_Number': phone_number,
    'Tarif': tarif
  }
  users.append(user)
  with open('users.json', 'w') as users_write:
    json.dump(users, users_write, ensure_ascii=False)
  bot.send_message(id_admin_Bo, ankets)
  first_page(message)


keep_alive()
def messages_group():
  for i in range(len(users)):
    if (users[i]['Tarif'] == 'Групповые занятия'):
      messagesGroups.append(users[i]['ID'])
    else:
      continue
  for i in range(len(messagesGroups)):
    bot.send_message(messagesGroups[i], 'Привет')


def run():
  schedule.every().friday.at('21:56').do(messages_group)
  while 1:
    schedule.run_pending()
    time.sleep(1)


thread = Thread(target=run)
thread.start()

bot.polling(none_stop=True)
