from telethon import TelegramClient, events
from telethon.tl.custom import Button
from System.settings import BOT_TOKEN, API_ID, API_HASH, ADMINS
from . import functions


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

#setting universal variables
btn = [
        [Button.text('Ticket', resize=True, single_use=True), Button.text('Documentation')], 
        [Button.text('Settings')]
    ]

langs = ["O'zbek", 'English', 'Русский']
languages = [[Button.text(text, resize=True, single_use=True)] for text in langs]

#Spedefic answer for admin
@bot.on(events.NewMessage(pattern='/start', from_users=ADMINS, incoming=True))
async def admin_start(event):
    await functions.save_user(event)
    await event.reply('Salom admin. Bot xizmatingizga tayyor!', buttons=btn)

@bot.on(events.NewMessage(pattern='/start', chats=ADMINS, blacklist_chats=True, incoming=True))
async def send_welcome(event):
    await functions.save_user(event)
    await bot.send_message(event.chat_id, f'Welcome to bot, {event.chat.first_name}. Choose one of below.', buttons=btn)

@bot.on(events.NewMessage(pattern='✖️Cancel', incoming=True))
async def cancel(event):
    return await send_welcome(event)

@bot.on(events.NewMessage(incoming=True))
async def moderator(event):
    user = await functions.get_user(event.chat.id)
    exception = await functions.exceptions()
    text = event.message.text
    if 'sent first message' in user.status and text not in exception:
        await functions.save_answer(event)
        await event.reply('Javobingiz yuborildi. Iltimos kuting.')

@bot.on(events.NewMessage(incoming=True))
async def ticket_save(event):
    user = await functions.get_user(event.chat.id)
    if user.status == 'waiting for ticket text':
        await functions.save_ticket(event, user)
        await bot.send_message(event.chat_id, 'Ticket ochildi. Iltimos admindan javobni kuting.', buttons=btn)
        await functions.save('status', event.chat.id, 'sent first message')

@bot.on(events.NewMessage(incoming=True))
async def choose_theme(event):
    user = await functions.get_user(event.chat.id)
    if user.status == 'choosing a theme' and event.message.text != '✖️Cancel':
        await functions.save('theme', event.chat.id, event.message.text)
        await event.reply('Mavzu yaratildi. Endi muammoni to\'liqroq yoriting.')
        await functions.save('status', event.chat.id, 'waiting for ticket text')

@bot.on(events.NewMessage(pattern='Ticket', incoming=True))
async def ticket_menu(event):
    if event.message.text == "Ticket":
        user = await functions.get_user(event.chat.id)
        if user.opened_ticket:
            await event.reply('Bittadan ko\'p ticket ochish mumkin emas!')
        else:
            themes = await functions.get('buttons')
            btns = [[Button.text(text, resize=True, single_use=True)] for text in themes]
            await bot.send_message(event.chat.id, 'Quyidagi mavzulardan birini tanlang', buttons=btns)
            await functions.save('status', event.chat.id, 'choosing a theme')

@bot.on(events.NewMessage(incoming=True))
async def subcategories_text(event):
    user = await functions.get_user(event.chat.id)
    if 'subcat' in user.status:
        link = await functions.get_link(event.message.text)
        await bot.send_message(event.chat.id, link, buttons=btn)
        first_m = user.status.split('subcat')[0]
        await functions.save('status', event.chat.id, first_m)

@bot.on(events.NewMessage(incoming=True))
async def subcategories_menu(event):
    user = await functions.get_user(event.chat.id)
    if 'category' in user.status:
        subs = await functions.get_subs(event.message.text)
        btns = [[Button.text(text, resize=True, single_use=True)] for text in subs]
        await bot.send_message(event.chat_id, 'Endi subcategoriyani tanlang', buttons=btns)
        first_m = user.status.split('category')[0]
        await functions.save('status', event.chat.id, f'{first_m}subcat')

@bot.on(events.NewMessage(incoming=True, pattern='Documentation'))
async def docs(event):
    cats = await functions.get('categories')
    btns = [[Button.text(text, resize=True, single_use=True)] for text in cats]
    await bot.send_message(event.chat_id, 'Quyidagi categoriyalardan birini tanlang', buttons=btns)
    user = await functions.get_user(event.chat.id)
    await functions.save('status', event.chat.id, f'{user.status} category')

@bot.on(events.NewMessage(incoming=True, pattern='Settings'))
async def settings(event):
    if event.message.text == 'Settings':
        await bot.send_message(event.chat.id, 'Choose your language:', buttons=languages)

@bot.on(events.NewMessage(incoming=True))
async def language(event):
    if event.message.text in langs:
        await bot.send_message(event.chat.id, f'Language setting has been changed to {event.message.text}', buttons=btn)
        await functions.language(event)