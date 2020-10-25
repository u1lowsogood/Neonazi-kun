#!/usr/bin/env python
# -*- coding: utf8 -*-
import io
import discord
import requests
import multiprocessing
import subprocess
import math
import os
import time
from datetime import datetime
from discord.ext import tasks
import random
import urllib3
import json
import base64
import numpy
from PIL import Image
from bs4 import BeautifulSoup
from websocket import create_connection

client = discord.Client()
global voich

def download_img(url, file_name, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path + file_name, 'wb') as f:
            f.write(r.content)

def download_vid(url, file_name):
    response = requests.get(url)
    with open("2gif/" + file_name, 'wb') as saveFile:
        saveFile.write(response.content)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # JOIN VC
    if message.content == ('犯すぞゴミ') or message.content == ('全召喚') :
        vcstate = message.author.voice

        if (not vcstate) or (not vcstate.channel):
            await message.channel.send("お前どこ因縁や")
            return

        voicechannel = vcstate.channel
        await voicechannel.connect()
        activity = discord.Activity(
            name='【ケツ穴拡張！？ドスケベマンコRoyal】Solo - Squad 4/3 残糞：残り(一億 人) ', type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)
        await message.channel.send('あ？殺すぞ？')

    # LEAVE VC
    if message.content == ('失せろゴミ'):
        vcclient = message.guild.voice_client

        if not vcclient:
            await message.channel.send("おらひんは死ね")
            return

        await vcclient.disconnect()
        await message.channel.send('お前声きめえｗ抜けるわｗ')

    #GLITCH
    if message.content.startswith('glitch'):
        historykun = await message.channel.history(limit=2).flatten()
        latestmessage = historykun[1]

        if latestmessage.attachments == []:
            await message.channel.send("画像 とは | 検索")
            return

        download_img(latestmessage.attachments[0].url, latestmessage.attachments[0].filename, "glitch/")
        await message.channel.send("読み込み完了ス！ｗｗｗｗｗ")

        inputpath = "glitch/" + latestmessage.attachments[0].filename
        outputpath = "glitch/" + latestmessage.attachments[0].filename + "output.jpg"


        im = Image.open(inputpath)
        rgb_im = im.convert('RGB')
        size = rgb_im.size
        im2 = Image.new('RGB',size)

        for x in range(size[0]):
            for y in range(size[1]):
                r,g,b = rgb_im.getpixel((x,y))
                rx=x
                ry=y
                while True:
                    sikii = random.randint(0,30)
                    rx = random.randint(x-sikii, x+sikii)
                    ry = random.randint(y-sikii, y+sikii)
                    if (rx > 0 and ry > 0) and (rx < size[0] and ry < size[1]):
                        break
                im2.putpixel((rx,ry),(r,g,b,0))
        """for x in range(size[0]//3):
            for y in range(size[1]//3):
                r,g,b = rgb_im.getpixel((x+3,y+3))
                im2.putpixel((x,y),(r,g,b,0))"""

        im2.save(outputpath, quality=100)

        await message.channel.send(file=discord.File(outputpath))

        await message.channel.send("完成品ス！ｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")

        subprocess.run("rm " + inputpath,shell=True)
        subprocess.run("rm " + outputpath,shell=True)

    # PIK2GIF
    if message.content.startswith('2gif'):
        
        historykun = await message.channel.history(limit=2).flatten()
        latestmessage = historykun[1]

        if "," in message.content:
            if message.content.split(",")[1] == "help":
                await message.channel.send("自分の頭で考えろゴミｗｗｗｗｗｗｗｗ")
                return

        if latestmessage.attachments == []:
            await message.channel.send("「画像」を御存じ無い・・・？？？ｗｗｗｗｗ")
            return

        download_vid(latestmessage.attachments[0].url, latestmessage.attachments[0].filename)

        await message.channel.send("きったねえ画像保存させんなゴミｗｗｗｗｗ")

        await message.channel.send("サブプロ、稼働！ｗ")

        exepath = "C:/ffmpeg-20200715-a54b367-win64-static/bin/ffmpeg.exe"
        inputpath = "D:/いろいろあるやつ/VSCode/workspace/AdonillaUtilityToolz/2gif/" + latestmessage.attachments[0].filename
        outputpath = "D:/いろいろあるやつ/VSCode/workspace/AdonillaUtilityToolz/2gif/" + latestmessage.attachments[0].filename + ".output.gif"

        if inputpath.split(".")[-1] == "mp4" or inputpath.split(".")[-1] == "mov" or inputpath.split(".")[-1] == "gif":
            if "," not in message.content:
                subprocess.run(exepath+" -i "+inputpath+" -filter_complex \"[0:v] fps=10,scale=400:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse=dither=none\" "+outputpath, shell=True)
            else:
                subprocess.run(exepath+" -i "+inputpath+" -filter_complex \"[0:v] fps="+message.content.split(",")[1]+",scale="+message.content.split(",")[2]+":-1,split [a][b];[a] palettegen [p];[b][p] paletteuse=dither=none\" "+outputpath,shell=True)
        else:
            subprocess.run(exepath+" -i "+inputpath+" -filter_complex \"split [a][b];[a] palettegen [p];[b][p] paletteuse=dither=none\" "+outputpath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            await message.channel.send(file=discord.File(outputpath))
            await message.channel.send("これで満足か？ｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
        except discord.errors.HTTPException:
            await message.channel.send("サイズデカすぎンが与ｗｗｗｗｗｗ2gif,[FPS],[SIZE]")

        print(inputpath)
        subprocess.run("rm " + inputpath,shell=True)
        subprocess.run("rm " + outputpath,shell=True)

    # DOWNLOAD IMG
    if message.content.startswith('waifu2x'):

        historykun = await message.channel.history(limit=2).flatten()
        latestmessage = historykun[1]

        # user
        if message.content.split(",")[1] == "help":
            await message.channel.send("``` モード：-m <noise|scale|noise_scale>\n ノイズ除去レベル： -n <0|1|2|3>\n サイズ：-s <小数点付き数値>\nモデル： -y\n（2次元イラスト）upconv_7_anime_style_art_rgb\n（写真・アニメ）upconv_7_photo\n（2次元イラスト）anime_style_art_rgb\n（写真・アニメ）photo\n（2次元イラスト）anime_style_art_y\n（2次元イラスト）upresnet10\n（2次元イラスト）cunet```")
            return

        if latestmessage.attachments == []:
            await message.channel.send("画像じゃ無ンだワ・・・")
            return

        download_img(latestmessage.attachments[0].url, latestmessage.attachments[0].filename, "waifu2x/")
        await message.channel.send("読み込み完了ス！ｗｗｗｗｗ")

        inputpath = "waifu2x/" + latestmessage.attachments[0].filename

        # default
        if message.content.split(",")[1] == "default":
            await message.channel.send("デフォルト設定（４倍）でcui実行ス！ｗｗｗｗｗｗｗｗｗ")
            subprocess.run("D:/いろいろあるやつ/KUSOFT/waifu2x-caffe/waifu2x-caffe/waifu2x-caffe-cui.exe -i " +
                           inputpath + " -m noise_scale -y cunet -s 4.0 -o " + inputpath + "output.png", shell=True)
            await message.channel.send("４倍化完了ス！ｗｗｗｗｗｗｗｗｗｗｗｗｗ")

        # user
        if message.content.split(",")[1] != "default":
            await message.channel.send("カスタム設定でcui実行ス！ｗｗｗｗｗｗｗｗｗ")
            subprocess.run("D:/いろいろあるやつ/KUSOFT/waifu2x-caffe/waifu2x-caffe/waifu2x-caffe-cui.exe -i " +
                           inputpath + " " + message.content.split(",")[1] + " -o " + inputpath + "output.png", shell=True)
            await message.channel.send("倍化完了ス！ｗｗｗｗｗｗｗｗｗｗｗｗｗ")

        await message.channel.send(file=discord.File(inputpath + "output.png"))

        await message.channel.send("完成品ス！ｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")

    # GAY
    if "ゲイセックス" in message.content:

        url = 'https://gay-friends.club/'

        http = urllib3.PoolManager()

        instance = http.request('GET', url)
        soup = BeautifulSoup(instance.data, 'html.parser')

        bodys = soup.body.select_one('div.container-fluid + div.container-fluid + div.container-fluid > div.row > div.col-contents > div.row + div.row > div.col-xs-12 > div.post > div.panel-body > p.body')

        #> div.row + div.row > div.col-xs-12 > div.post > div.panel-body > p.body') random.randint(3, 6)

        await message.channel.send(bodys.text)

    # APEX
    if "APEXマウント" in message.content:

        name = "PKateruchan"

        if "、" in message.content:
            username = message.content.split("、")[1]
            name = username

        url = 'https://apex.tracker.gg/profile/pc/' + name

        http = urllib3.PoolManager()

        instance = http.request('GET', url)
        soup = BeautifulSoup(instance.data, 'html.parser')

        rank = soup.find("div",class_="trn-defstat__name")
        rate = soup.find("div",class_="trn-defstat__value")
        juni = "anal"
        if rank.text == "Apex Predator":
            junikun = soup.find("div",class_="trn-defstat__rank")
            juni = junikun.text

        await message.channel.send("```md\n#" + name + "のAPEX情報でぇぇ～～～すｗｗｗｗｗｗ\n\n< " + rank.text + " >\n1. RATE: "+rate.text+"\n2. RANK: " + juni + "```")

    #WEATHER
    if "の天気" in message.content:


        if str(message.author.id) == "240824814711865345":
            await message.channel.send("お前の地域は一生梅雨です＾＾ｗｗｗｗｗシメジ育ってそうｗ")
            return

        when = ""
        whenjap = ""

        if message.content.startswith("今日"):
            when = "today"
            whenjap = "きょう"
        elif message.content.startswith("明日"):
            when = "tomorrow"
            whenjap = "あした"
        else:
            await message.channel.send("明日も貼れるといいね＾＾")
            return

        #SKRAPE V1
        area = "東大和市"
        if "、" in message.content:
            area = message.content.split("、")[1]

        url = 'https://weather.yahoo.co.jp/weather/search/?p=' + area

        http = urllib3.PoolManager()

        instance = http.request('GET', url)
        soup = BeautifulSoup(instance.data, 'html.parser')

        place = soup.select_one('#main > div.yjw_main_md > div.tracked_mods > div.serch-table > table > tbody > tr > td')

        if place == None:
            await message.channel.send("オリジナル県ｗｗｗｗｗｗｗｗｗｗ地理学んで来いｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗｗ")
            return

        #GET NU URL
        url = "https:" + place.select_one("a").get("href")
        instance = http.request('GET', url)
        soup = BeautifulSoup(instance.data, 'html.parser')

        date = soup.select_one('#main > div.yjw_main_md > #yjw_pinpoint > div.yjw_clr > div.tracked_mods > p.yjw_note_h2')

        #table
        table = soup.select_one('#main > div.yjw_main_md > #yjw_pinpoint > #yjw_pinpoint_' + when +'> table.yjw_table2').find_all("tr")

        #time
        times = table[0].find_all("td")
        timestring = ""
        for timez in times:
            timestring = timestring + timez.text

        #weather
        weathers = table[1].find_all("td")
        weatherstring = ""
        for counter, weather in enumerate(weathers):
            if counter == 0:
                weatherstring = weatherstring + weather.text + " "
                continue
            weatherstring = weatherstring + weather.select_one("img").get("alt") + " "

        #temp
        temps = table[2].find_all("td")
        tempstring = ""
        for counter, temp in enumerate(temps):
            if counter == 0:
                tempstring = "気温 "
                continue
            tempstring = tempstring + temp.text + "℃ "

        #water
        waters = table[4].find_all("td")
        waterstring = ""
        for counter, water in enumerate(waters):
            if counter == 0:
                waterstring = "降水 "
                continue
            waterstring = waterstring + water.text + "㎜ "

        string = "```" + timestring.replace("\n"," ") + "\n\n" + weatherstring.replace("\n"," ") + "\n" + tempstring.replace("\n"," ") + "\n" + waterstring.replace("\n"," ") + "```"

        await message.channel.send(date.text.replace("\n","")+ "\n「" + place.text + "」の" + whenjap + "の天気はァ～～～～～～ッ？？？ｗｗｗｗｗｗｗ\n" + string)
    
    #PLAYWAV
    if "wavplay.test" in message.content:

        voich = await discord.VoiceChannel.connect(message.author.voice.channel)
        voich.play(discord.FFmpegPCMAudio('sounds\\mesu.mp3')) # , after=check_error

    #WEBSOCKET
    if message.content.startswith("SOCKET"):

        roomID = message.content.split(",")[1]
        await message.channel.send("WSSに接続します。 ID=" + str(roomID))
        ws = create_connection("wss://jp-room1.mildom.com/?roomId="+str(roomID))

        await message.channel.send("WSSにユーザ情報を送信します。 wss.send")
        ws.send(json.dumps({
        "userId": 0,
        "level": 1,
        "userName": "Yomiagebotkun",
        "guestId": "Yomiageman",
        "nonopara": "Yomiageman",
        "roomId": int(roomID),
        "cmd": "enterRoom",
        "reConnect": 0,
        "nobleLevel": 0,
        "avatarDecortaion": 0,
        "enterroomEffect": 0,
        "nobleClose": 0,
        "nobleSeatClose": 0,
        "reqId": 1}))

        await message.channel.send("過去のメッセージ一覧を取得中……（about 5 sec）")

        t_end = time.time() + 5
        while time.time() < t_end:
                ws.recv()

        #接続処理
        #await message.channel.send("ボイスチャンネルへの接続処理を行います。")

        #voich = await discord.VoiceChannel.connect(message.author.voice.channel)

        await message.channel.send("最新メッセージの受信待ちです")
        outputpath = "D:\\いろいろあるやつ\\VSCode\\workspace\\AdonillaUtilityToolz\\sounds\\output.wav"


        while(True):
            if ws.recv() != "":
                jsonkun = json.loads(str(ws.recv()))

                print(jsonkun)

                if ("cmd", "onChat") in jsonkun.items():

                    name = str(jsonkun["userName"])
                    comment = str(jsonkun["msg"])
                    await message.channel.send(name + ": " + comment)
                    subprocess.run("D:\\softalk\\SofTalk.exe /X:1 /R:" + outputpath + " /W:" + name + "からのメッセージ、" + comment, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #voich.play(discord.FFmpegPCMAudio(outputpath))
                    #subprocess.run("rm " + outputpath,shell=True)
                    
                elif ("cmd", "onAdd") in jsonkun.items():

                    name = str(jsonkun["userName"])
                    if "guest" not in name:
                        await message.channel.send(name + "さんが入室しました。")
                    #subprocess.run("D:\\softalk\\SofTalk.exe /X:1 /R:" + outputpath + " /W:" + name + "さんが入室しました。", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #voich.play(discord.FFmpegPCMAudio(outputpath))
                    #subprocess.run("rm " + outputpath,shell=True)

                elif ("cmd", "onGift") in jsonkun.items():

                    name = str(jsonkun["userName"])
                    await message.channel.send(name + "さんがあなたにギフトを送りました！")
                    #subprocess.run("D:\\softalk\\SofTalk.exe /X:1 /R:" + outputpath + " /W:" + name + "さんがあなたにギフトを送りました。", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    #voich.play(discord.FFmpegPCMAudio(outputpath))
                    #subprocess.run("rm " + outputpath,shell=True)

        #p0 = multiprocessing.Process(target=websocketreciver, args=(ws,message))
        #p0.start()
        #p0.join()


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '00:00':

        channel = client.get_channel(366193178568818688)
        num = 0
        emptyslot = 0
        path = "easy/"
        
        await channel.send("CAN WE GO BACK?")

        emojiz = await channel.guild.fetch_emojis()
        for emoji in emojiz:
            if "easy_" in emoji.name:
                if emoji.name not in "easy_desperation easy_happiness easy_nomal easy_sad":
                    await emoji.delete()

        emojiiz = await channel.guild.fetch_emojis()
        for emojiii in emojiiz:
            num+=1

        emptyslot = 50 - num

        choisedemojifiles = random.sample(os.listdir(path), emptyslot)

        for emozzie in choisedemojifiles:

            emojiname = os.path.splitext(emozzie)[0] 
        
            easyfilepath = path + emozzie
            tmpimg = Image.open(easyfilepath)

            with io.BytesIO() as output:
                tmpimg.save(output,format="PNG")
                contents = output.getvalue()#バイナリ取得
                await channel.guild.create_custom_emoji(name=emojiname, image=contents)

        await channel.send("```md\n#【本日の日替わり倖田來未は？】\n< What's Today's Daily Easy!? >```")

        easysend = ""

        emojjjiz = await channel.guild.fetch_emojis()
        for emooji in emojjjiz:
            if "easy_" in emooji.name:
                if emooji.name not in "easy_desperation easy_happiness easy_nomal easy_sad":
                    easysend += "<:" + emooji.name + ":" + str(emooji.id) + ">"
        
        await channel.send(easysend)

loop.start()

client.run('NzMzMjA5MzQ2MDc4NDA4NzU2.Xw_1tw.7HkClgr3q2Vf6u2aCx7bXGr7TN0')
