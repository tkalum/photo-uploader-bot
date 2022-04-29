import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import aiofiles
from random import choice 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from telegraph import upload_file
from youtube_search import YoutubeSearch
import requests
from pytube import YouTube
import youtube_dl

tgraph = Client(
    "Image upload bot",
    bot_token='5115439510:AAEMH6f2TsnkkYSEsVzndabwBlaljPNjzMY',
    api_id=19611094,
    api_hash='c5198b0dab5cdd8e0eaaf3e0c742fbd3'
)

START_TEXT = """**Hello {} 😌
I am small media or file to telegra.ph link uploader bot.**
>> `I can convert under 5MB photo or video to telegraph link.`
Powered by @tk_botz_update👑"""

HELP_TEXT = """**Hey, Follow these steps:**
➠ Just give me a media under 5MB
➠ Then I will download it
➠ I will then upload it to the telegra.ph link
**Available Commands**
/start - Checking Bot Online
/help - For more help
/about - For more about me
Powered by @tk_botz_update👑"""

ABOUT_TEXT = """--**About Me**-- 😎
🤖 **Name :** [Telegraph Uploader](https://telegram.me/{})
👨‍💻 **Creator :** [unkwon boy](https://t.me/UnknownB_o_y)
📢 **Channel :** [Fayas Noushad](https://telegram.me/tk_botz_update)
📝 **Language :** [Python3](https://python.org)
🧰 **Framework :** [Pyrogram](https://pyrogram.org)"""



START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('About 🔰', callback_data='about'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('About 🔰', callback_data='about'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )


async def send_msg(user_id, message):
	try:
		await message.copy(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : deactivated\n"
	except UserIsBlocked:
		return 400, f"{user_id} : user is blocked\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : user id invalid\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"


@tgraph.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@tgraph.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
        await update.reply_photo('https://telegra.ph/file/41fe7e055f684cf08795d.jpg')
        await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        
        disable_web_page_preview=True,
        
	reply_markup=START_BUTTONS
    )

@tgraph.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
        await update.reply_text(
        text=HELP_TEXT,
      	disable_web_page_preview=True,
	reply_markup=HELP_BUTTONS
    )
	
	
@tgraph.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
        await update.reply_text(
        text=ABOUT_TEXT.format((await bot.get_me()).username),
        disable_web_page_preview=True,
	reply_markup=ABOUT_BUTTONS
    )

@tgraph.on_message(filters.photo)
async def getimage(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    img_path = await message.download()
    await dwn.edit_text("Uploading as telegra.ph link...")
    try:
        url_path = upload_file(img_path)[0]
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Link", url=f"https://telegra.ph{url_path}"
                    ),
                    InlineKeyboardButton(
                        text="Share Link",
                        url=f"https://telegram.me/share/url?url=https://telegra.ph{url_path}",
                    )
                ]
            ]
        )
    )
    os.remove(img_path)

@tgraph.on_message(filters.command('song'))
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜 ••• 🚀')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)

        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
        yt = YouTube(link)
    except Exception as e:
        m.edit(
            "❌ Found Nothing.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("𝘿𝙤𝙬𝙣𝙡𝙤𝒹𝙞𝙣𝙜 𝙨𝙤𝙣𝙜•••😉")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '🎵 𝙐𝙥𝙡𝙤𝙖𝙙𝙚𝙙 𝙗𝙮 @TheAnkiVectorbot•••\n 𝙟𝙤𝙞𝙣 @ankivectorUpdates •••'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        s = message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur, performer=str(yt.author))
        m.delete()
    except Exception as e:
        m.edit('❌ Error\n Report @AnkiSupport_Official')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


tgraph.run()
