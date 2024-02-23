import asyncio

import nextcord
from nextcord.ext import commands
from config import token
from gtts import gTTS
from configs import sound_list
from importlib import reload

nextcord.Intents.message_content = True

#Bot prefix and Intents.
bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

#Show a message if everything went fine and the bot is online and connected.
@bot.event
async def on_ready():
    print("____________________________________________________")
    print(f"Logged in as {bot.user.name} with id {bot.user.id}")
    print("____________________________________________________")

#Play a specific sound when someone joins a voice channel, if no sound is defined on configs\sound_list.py plays a default sound.
@bot.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel:
        if member.voice is not None:
            try:
                vc = await member.voice.channel.connect()
            except:
                vc = member.voice_client

            if vc.is_playing():
                vc.stop()

            reload(sound_list)
            try:
                source = source = await nextcord.FFmpegOpusAudio.from_probe("sounds/" + sound_list.soundlist[member.id],
                                                                            method="fallback")
            except:
                source = source = await nextcord.FFmpegOpusAudio.from_probe("sounds/CHANGE_TO_DEFAULT_SOUND.mp3", method="fallback")

            vc.play(source)

            while True:
                await asyncio.sleep(1)

                if not vc.is_playing():
                    await vc.disconnect()
                    break

#Play a specific sound from the sounds folder, you don't need to specify the file extension. (mp3, wav, etc.)
@bot.command(name="som")
async def som(ctx, arg):
    user = ctx.message.author
    if user.voice is not None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client

        try:
            source = source = await nextcord.FFmpegOpusAudio.from_probe("sounds/" + arg + ".mp3", method="fallback")

        except:
            await ctx.send("Este som não existe.")

        if vc.is_playing():
            vc.stop()

        vc.play(source)

        while True:
            await asyncio.sleep(1)

            if not vc.is_playing():
                await vc.disconnect()
                break

#Text to speech, you can change the language in line 90, default is pt-br.
@bot.command(name="tts")
async def tts(ctx, *args):
    text = " ".join(args)
    user = ctx.message.author
    if user.voice is not None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc = ctx.voice_client

        sound = gTTS(text=text, lang="pt-br", slow=False)
        sound.save("tts.mp3")

        if vc.is_playing():
            vc.stop()

        source = await nextcord.FFmpegOpusAudio.from_probe("tts.mp3", method="fallback")
        vc.play(source)

        while True:
            await asyncio.sleep(1)

            if not vc.is_playing():
                await vc.disconnect()
                break
    else:
        await ctx.send(f"Você precisa estar em um canal de voz para usar o tts! {user.mention}")

bot.run(token)
