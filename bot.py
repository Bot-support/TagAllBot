import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("** I am member Tagger **, I can Tag almost all members in group or channel 🤓\nClick **/help** for more infomation.\n",
                    buttons=(
                      [
                         Button.url('📣 UPDATES', 'https://t.me/DeeCodeBots'), 
                         Button.url('⭐SUPPORT', 'https://t.me/DeCodeSupport'), 
                      ], 
                      [
                        Button.url('➕ ADD ME TO YOUR GROUP', 'https://t.me/MEMBER_TAGERBOT?startgroup=true'),   
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Hey  I Am Member Tagger \n\n You can Tag members by using Commands shown below,\n\n /all text \n\n @all text \n\n #all text**"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('📣 UPDATES', 'https://t.me/DeeCodeBots')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/tagall|/mall|/tall|/all|#all|@all ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(" ❌ YOU ARE NOT AN ADMIN IN THESE GROUP")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which sended before i added to group)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("GIVE ME A TEXT TO TAG MEMBERS OR REPLY TO A TEXT WHICH YOU WANTS TO TAG ALL")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print("Started.. Join @DecodeSupport")
client.run_until_disconnected()
