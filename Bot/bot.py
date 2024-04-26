from telethon import TelegramClient, events, types
from telethon.tl.custom import Button
from System.settings import BOT_TOKEN, API_ID, API_HASH, ALLOWED_HOSTS
from . import functions
from django.utils.translation import activate, gettext as _


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.CallbackQuery())
async def choose_lang(event):
    #set language for user
    language = await functions.get_lang(event.chat.id)
    activate(language)

    data = event.data.decode('utf-8')
    if data == 'setting':
        languages = [[Button.inline("O'zbek🇺🇿", 'uzbek'), Button.inline('Русский🇷🇺', 'russian')], [Button.inline(_('Back'), 'cancel')]]
        await bot.edit_message(event.chat.id, event.message_id, _('choose lang'), buttons=languages)
    elif data == 'uzbek':
        await functions.set_lang(event.chat.id, 'uz')
        await cancel(event)
    elif data == 'russian':
        await functions.set_lang(event.chat.id, 'ru')
        await cancel(event)
    elif data == 'cancel':
        await cancel(event)


@bot.on(events.CallbackQuery())
async def ticket_and_docs(event):
    data = event.data.decode('utf-8')
    if data == 'ticket':
        if await functions.opened_ticket(event.chat.id):
            btns = [Button.inline(_('Back'), 'cancel')]
            await bot.edit_message(event.chat.id, event.message_id, _('more than one ticket isnt allowed'), buttons=btns)
        else:
            themes = await functions.get_themes(event.chat.id)
            btns = [[Button.inline(text, f'theme-{text}')] for text in themes]
            await bot.edit_message(event.chat.id, event.message_id, _('choose ticket theme'), buttons=btns)
    elif data[0:5] == 'theme':
        await functions.set_status(event.chat.id, 'writing a problem')
        await functions.save_theme(event.chat.id, data[6:-1])
        await bot.send_message(event.chat.id, _('please write your problem here'))
        await bot.delete_messages(event.chat.id, event.message_id)
    elif data == 'docs':
        lang = await functions.get_lang(event.chat.id)
        btn = [[types.KeyboardButtonWebView(_('read documentation'), f"https://{ALLOWED_HOSTS[0]}/{lang}/docs")], [Button.inline(_('Back'), 'cancel')]]
        await bot.edit_message(event.chat.id, event.message_id, _('you can have more info reading the doc below'), buttons=btn)


@bot.on(events.NewMessage(incoming=True))
async def receiving_problem(event):
    #set language for user
    language = await functions.get_lang(event.chat.id)
    activate(language)

    status = await functions.get_status(event.chat.id)
    text = event.message.text
    if status == 'writing a problem' and text != '/start' :
        await functions.open_ticket(event)
        await event.reply(_('message received. wait for response from admins'))
        await functions.set_status(event.chat.id, 'messages are sent to admin')
    if status == 'messages are sent to admin' and text != '/start':
        await functions.save_answer(event)
        await event.reply(_('message is sent to admin, wait for response'))


@bot.on(events.NewMessage(pattern='/start', incoming=True))
async def welcome(event):
    btn = [
        [Button.inline(_('ticket'), 'ticket'), Button.inline(_('docs'), 'docs')], 
        [Button.inline(_('setting'), 'setting')]
    ]
    await functions.save_user(event)
    await bot.send_message(event.chat_id, _('welcome'), buttons=btn)


async def cancel(event):
    #set language for user
    language = await functions.get_lang(event.chat.id)
    activate(language)

    btns = [
        [Button.inline(_('ticket'), 'ticket'), Button.inline(_('docs'), 'docs')], 
        [Button.inline(_('setting'), 'setting')]
        ]
    await bot.edit_message(event.chat.id, event.message_id, _('choose one of below'), buttons=btns)