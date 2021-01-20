import discord
from discord.ext import commands
import os
import random
import asyncio
import json
import requests
import urllib.request

client = commands.Bot(command_prefix='.')
activating_inside_joke = False
inside_jokes = []


def contains_words(words, text):
    for word in words:
        if (word in text):
            return True
    return False


def get_inside_jokes():
    f = open('inside_jokes.txt')
    jokes = []
    jokes = f.read().split('\n')
    return (jokes)


def add_inside_joke(joke):
    f = open('inside_jokes.txt', 'a')
    f.write('\n' + joke)
    inside_jokes.append(joke)


def get_yt_query(message):
    query = ''
    if "yt" in message.content:
        query = message.content.replace("yt ", "")
    elif "youtube" in message.content:
        query = message.content.replace("youtube ", "")
    query_formatted = query.replace(" ", "+")
    output_query = "https://www.youtube.com/results?search_query=" + query_formatted
    return output_query


def get_seconds(message):
    splitted = []
    splitted = message.content.split(' ')
    i = 0
    hours = 0
    minutes = 0
    seconds = 0
    for element in splitted:
        if element == 'h' or element == 'hours' or element == 'godzin' or element == 'godziny':
            if (i > 0):
                if (splitted[i - 1].isdigit()):
                    hours = int(splitted[i - 1])

        if element == 'm' or element == 'min' or element == 'minutes' or element == 'minut' or element == 'minuty':
            if (i > 0):
                if (splitted[i - 1].isdigit()):
                    minutes = int(splitted[i - 1])

        if element == 's' or element == 'sec' or element == 'seconds' or element == 'sekund' or element == 'sekundy':
            if (i > 0):
                if (splitted[i - 1].isdigit()):
                    seconds = int(splitted[i - 1])
        i += 1

    seconds += minutes * 60
    seconds += hours * 3600
    return seconds


def get_random(message):
    splitted = message.content.split(' ')
    x = -1
    y = -1
    for element in splitted:
        if element.isdigit():
            if x == -1:
                x = int(element)
            else:
                y = int(element)
    max = -1
    min = -1
    if x < y:
        min = x
        max = y
    else:
        min = y
        max = x

    return random.randint(min, max)


def get_panda_fact():
    panda_url = 'https://some-random-api.ml/facts/panda'
    fact = json.loads(requests.get(panda_url).content)["fact"]
    return fact


def get_artist():
    f = open('music.txt')
    artists = []
    artists = f.read().split('\n')
    return (artists[random.randint(0, len(artists))])


def get_joke(message):
    return (message.content.replace("inside joke ", ""))


async def timer(seconds, message):
    counter = seconds
    while True:
        counter -= 1
        if (counter == 0):
            break
        await asyncio.sleep(1)
    await message.channel.send("TIME HAS PASSED")


async def send_meme(ctx):
    f = random.choice(os.listdir("memes"))
    await ctx.send(file=discord.File("memes/" + f))


async def split_the_bill(message):
    msg = []
    msg = message.content.split(':')
    ppl = []
    ppl = msg[1].split(',')
    sum = 0
    for element in ppl:
        name, money = element.split(" - ")
        sum += float(money)

    part = sum / len(ppl)
    output = ''
    for element in ppl:
        name, money = element.split(" - ")
        if (element != ppl[0]):
            output += ", " + name
        else:
            output = name

        diff = abs(part - float(money))
        if (part < float(money)):
            output += " should get " + str(round(diff, 2))
        elif (part == float(money)):
            output += " paid their share"
        else:
            output += " should pay " + str(round(diff, 2))

    await message.channel.send(output)


@client.event
async def on_ready():
    global inside_jokes
    inside_jokes = get_inside_jokes()
    print('Lil B is readyy')


@client.event
async def on_member_join(member):
    await member.send('Nice to see you here')


@client.event
async def on_member_remove(member):
    server = member.server
    channel = [
        channel for channel in client.get_all_channels()
        if channel.name == 'ogólny'
    ][0]
    message = 'bye {}! hope they come back'.format(member.mention)
    await client.send_message(channel, message)


@client.event
async def on_message(message):
    MSG = message.content.lower()
    activating_inside_joke = False
    if message.author == client.user:
        return

    hi_words = [
        'yo', 'cześć', 'hej', 'hey', 'hi', 'dzień dobry', 'dzien dobry'
    ]
    if contains_words(hi_words, MSG):
        await message.channel.send('Yo')

    bye_words = [
        'bye', 'do widzenia', 'żegnam', 'goodbye', 'see you later', 'peace'
    ]
    if contains_words(bye_words, MSG):
        await message.channel.send("Byee")

    bill_words = ['podziel rachunek', 'split bill', 'split the bill']
    if contains_words(bill_words, MSG):
        await split_the_bill(message)

    timer_words = ['timer']
    if contains_words(timer_words, MSG):
        seconds = get_seconds(message)
        await timer(seconds, message)

    random_words = ['random']
    if contains_words(random_words, MSG):
        random_n = get_random(message)
        await message.channel.send('Your random number is ' + str(random_n))

    panda_words = ['panda', 'pandy']
    if contains_words(panda_words, MSG):
        await message.channel.send(get_panda_fact())

    music_words = [
        'recommend some music', 'recommend music', 'poleć muzykę',
        'polec muzyke'
    ]
    if contains_words(music_words, MSG):
        artist = get_artist()
        await message.channel.send("Personally i love " + artist)

    youtube_words = ["yt", "youtube"]
    if contains_words(youtube_words, MSG):
        query = get_yt_query(message)
        await message.channel.send(query)

    inside_joke_activate_words = ['inside joke']
    if contains_words(inside_joke_activate_words, MSG):
        joke = get_joke(message)
        add_inside_joke(joke)
        activating_inside_joke = True

    count_members_words = [
        'count members', 'policz uzytkownikow', 'policz użytkowników'
    ]
    if contains_words(count_members_words, MSG):
        await message.channel.send("There's " +
                                   str(message.guild.member_count) +
                                   " people and bots on this channel")

    how_are_you_words = [
        'how are you', 'jak się masz', 'jak sie masz', 'co tam',
        'how\'s it going'
    ]
    if contains_words(how_are_you_words, MSG):
        await message.channel.send("Oh you know it's going")

    if contains_words(inside_jokes, MSG) and not activating_inside_joke:
        await message.channel.send("LOL that's so funny")

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send('Pong')


@client.command()
async def meme(ctx):
    await send_meme(ctx)


@client.command()
async def mem(ctx):
    await send_meme(ctx)


@client.command()
async def lil_b(ctx):
    info_file = open('lil_b_info.txt')
    info = info_file.read()
    await ctx.send(info)


@client.command()
async def lil_b_get_specific(ctx):
    info_file = open('lil_b_info_specific.txt')
    info = info_file.read()
    await ctx.send(info)


def get_token():
    f = open("token.txt")
    return f.read()


token = get_token()
client.run(token)
