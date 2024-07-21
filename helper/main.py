import os
import message,app
import telegram
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CommandHandler,MessageHandler,filters,ApplicationBuilder,CallbackQueryHandler
import google.generativeai as genai
import PIL.Image
genai.configure(api_key=app.apiKey)
model=genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
with open("token.bot","r",encoding="utf-8") as file:
    bot=ApplicationBuilder().token(file.read()).build()
async def img(update,contextt):
    info=update.effective_user
    id=await message.Sendmessage(info.id,"downloading your photo")
    path=os.path.join("cach",str(info.id))
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        try:
            get=await update.message.photo[-1].get_file()
        except:
            get=await update.message.effective_attachment.get_file()
        await get.download_to_drive(path+"/photo.png")
        await message.Editmessage(info.id,"describing your image",id)
        try:
            res=model.generate_content([f"""The following is a detailed description of an image intended to provide a vivid and comprehensive understanding for blind users. Describe the scene, objects, actions, and any other relevant details with specific locations, distances, and sizes where possible. Clearly and concisely describe each element to help the listener visualize the scene. If objects are unclear, indicate this. If text is present in the image, output the text along with its location.
                                      
[IMAGE DESCRIPTION START]
The image shows a bustling city street during the day. On the left side of the image, approximately 100 meters from the bottom, there is a row of tall buildings with glass windows reflecting the sunlight. The street is lined with trees spaced about 20 meters apart, each around 10 meters tall. There are people walking on the sidewalk, some holding shopping bags; the sidewalk is about 3 meters wide.
A yellow taxi is parked at the curb on the left side of the street, around 50 meters from the bottom of the image, and a red double-decker bus is driving down the street, approximately 150 meters from the bottom of the image. In the background, the sky is clear with a few scattered clouds.
A street vendor is selling hot dogs from a cart near the corner of the street, positioned about 30 meters from the bottom left corner. A group of children is playing near a fountain in the park, visible in the distance on the right side of the image, roughly 200 meters from the bottom right corner. The fountain is large, with water cascading down multiple tiers, and the children are running around it, laughing and playing. Some objects in the background are not clear.
[IMAGE DESCRIPTION END]
Provide a similarly detailed description for the given image.""",PIL.Image.open(path + "/photo.png")])
            result=res.text
            await message.Editmessage(info.id,result,id)
        except Exception as e:
            print(e)
            os.remove(path= + "/photo.png")
            await message.Editmessage(info.id,"an error detected",id)
    except Exception as e:
        print(e)
        await message.Editmessage(info.id,"error while downloading",id)


async def start(update,contextt):
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("donate",url="https://www.paypal.me/AMohammed231")],[InlineKeyboardButton("help",callback_data="help")]])
    await message.Sendmessage(chat_id=info.id,text="welcome " + str(info.first_name) + " to this bot. please send description for any image",reply_markup=keyboard)
async def helb(update,contextt):
    links="""<a href="https://t.me/mesteranasm">telegram</a>

<a href="https://t.me/tprogrammers">telegram channel</a>

<a href="https://x.com/mesteranasm">x</a>

<a href="https://Github.com/mesteranas">Github</a>

email:
anasformohammed@gmail.com

<a href="https://Github.com/mesteranas/anas_main_telegram_bot">visite project on Github</a>
"""
    info=update.effective_user
    await message.Sendmessage(info.id,"""name: {}\nversion: {}\ndescription: {}\n developer: {}\n contect us {}""".format(app.name,str(app.version),app.description,app.developer,links))
async def callBake(update,contextt):
    q=update.callback_query
    q.answer()
    if q.data=="help":
        await helb(update,contextt)

print("running")
bot.add_handler(CommandHandler("start",start))
bot.add_handler(CommandHandler("help",helb))
bot.add_handler(CallbackQueryHandler(callBake))
bot.add_handler(MessageHandler(filters.Document.ALL,img))
bot.add_handler(MessageHandler(filters.PHOTO,img))
bot.run_polling()