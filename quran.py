from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import AudioPiped

from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle

import asyncio, json, pytgcalls

from config import *

app = Client(
    "call",
    API_ID,
    API_HASH,
    session_string=SESSION_STRING
)
call = PyTgCalls(app)

quran = json.loads(open("./quran.json", "r").read())
already = []

async def Call():
    while not await asyncio.sleep(1.5):
        print(len(already))
        if len(already) == 114:
            already.clear()
        if already:
            surah = quran[already.index(already[-1]) + 1]
            surah_name = "سورة " + surah["name_translations"]["ar"]
            surah_url = surah["recitation"]
        else:
            surah = quran[0]
            surah_name = "سورة " + surah["name_translations"]["ar"]
            surah_url = surah["recitation"]
        try:
                    getGroupCall = await call.get_active_call(CHAT_ID)
                    if not getGroupCall.is_playing:
                        await call.leave_group_call(CHAT_ID)
        except Exception:
                    try:
                        await call.leave_group_call(CHAT_ID)
                    except:
                        pass
        try:
                    if not CHANNEL_USERNAMWE:
                        await call.join_group_call(
                            CHAT_ID,
                            AudioPiped(surah_url),
                        )
                    else:
                        await call.join_group_call(
                            CHAT_ID,
                            AudioPiped(surah_url),
                            join_as=await app.resolve_peer(CHANNEL_USERNAMWE)
                        )
                    channel = await app.invoke(GetFullChannel(channel=await app.resolve_peer(CHAT_ID)))
                    data = EditGroupCallTitle(call=channel.full_chat.call, title="مشاري راشد العفاسي | "+surah_name)
                    await app.invoke(data)
                    already.append(surah)
        except pytgcalls.exceptions.AlreadyJoinedError:
                    print("Already Joined")
        except Exception as e:
                    print(e)

async def main():
    await app.start()
    print("APP START")
    await call.start()
    print("CALL START")
    asyncio.create_task(Call())
    print("DONE")
    await idle()
    
asyncio.run(main())