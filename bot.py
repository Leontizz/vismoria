import discord
from discord.ext import commands
from Cybernator import Paginator as pag
from discord.utils import get
import youtube_dl
import asyncio
import functools
import itertools
import math
import random
from discord import FFmpegPCMAudio
from async_timeout import timeout
import requests
import nekos
from googletrans import Translator
import datetime
from random import randint
from random import choice
import time
import pymongo
import asyncio
import os
import json
import wikipedia
import nekos
import youtube_dl
from yandex_music import Client

client = commands.Bot(command_prefix= '')
client.remove_command('help')

que = []



#Status

@client.command(hidden = True)
@commands.has_permissions( administrator = True )
async def statplay(ctx, *, arg):
	if not commands.NotOwner:
		await ctx.send(f"Отказано в доступе!")
	else:
		await client.change_presence(activity=discord.Game(name=arg))
		await ctx.send("Статус бота изменен!")

@client.command(hidden = True)
@commands.has_permissions( administrator = True )
async def statwatch(ctx, *, arg):
	if not commands.NotOwner:
		await ctx.send(f"Отказано в доступе!")
	else:
		await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.watching))
		await ctx.send("Изменяем...")
		await ctx.send("Статус бота изменен!")

@client.command(hidden = True)
@commands.has_permissions( administrator = True )
async def statlisten(ctx, *, arg):
	if not commands.NotOwner:
		await ctx.send(f"Отказано в доступе!")
	else:
		await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.listening))
		await ctx.send("Изменяем...")
		await ctx.send("Статус бота изменен!")

@client.command(hidden = True)
@commands.has_permissions( administrator = True )
async def statstream(ctx, *, arg):
	if not commands.NotOwner:
		await ctx.send(f"Отказано в доступе!")
	else:
		await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.streaming))
		await ctx.send("Изменяем...")
		await ctx.send("Статус бота изменен!")


	#Kick
@client.command( pass_cont = True, hidden = True )
@commands.has_permissions( administrator = True )
async def kick( ctx, member: discord.Member, *, reason = None ):

		await member.kick( reason = reason )
		await ctx.send(f'Игрок {member.mention} был кикнут ')

@kick.error 
async def kick_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

	#Ban
@client.command( pass_cont = True, hidden = True  )
@commands.has_permissions( administrator = True )
async def ban(ctx, member : discord.Member, time:int, arg:str, *, reason=None):
	if member == ctx.message.author:
		return await ctx.send("Ты не можешь забанить сам себя.")
	msgg =  f'Пользователь : {member}, забанен по причине : {reason}.'
	msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине : {reason}.'
	if reason == None:
		msgdm = f'Вы были забанены на сервере : {ctx.guild.name}.'
	if reason == None:
		msgg =  f'Пользователь : {member}, забанен.'
	await ctx.send(msgg)  
	await member.send(msgdm)
	await ctx.guild.ban(member, reason=reason)
	if arg == "s":
		await asyncio.sleep(time)          
	elif arg == "m":
		await asyncio.sleep(time * 60)
	elif arg == "h":
		await asyncio.sleep(time * 60 * 60)
	elif arg == "d":
		await asyncio.sleep(time * 60 * 60 * 24)
	await member.unban()
	await ctx.send(f'Пользователь : {member}, разбанен.')
	await member.send(f'Вы были разбанены на сервере : {ctx.guild.name}')

@ban.error 
async def ban_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  


#mute
@client.command( pass_context = True, hidden = True)
@commands.has_permissions( administrator = True )
async def mute(ctx, member : discord.Member, time:int, arg:str, *, reason=None):

	Переменная_размут = f'**Вы были размучены на сервере {ctx.guild.name}**'
	Переменная_мут = f'**Вы были замучены на сервере {ctx.guild.name} на {time}{arg} по причине: {reason}**'
	mute_role = discord.utils.get( ctx.message.guild.roles, id = 721049136593371216 )

	await member.add_roles(mute_role, reason=None, atomic=True)
	await ctx.send(embed = discord.Embed(description = f'**:shield:Мут пользователю {member.mention} успешно выдан на {time}{arg} по причине {reason} :shield:**', color=0x0000FF))
	await member.send(embed = discord.Embed(description = f'{Переменная_мут}', color=0x0c0c0c))

	if arg == "s":
		await asyncio.sleep(time)          
	elif arg == "m":
		await asyncio.sleep(time * 60)
	elif arg == "h":
		await asyncio.sleep(time * 60 * 60)
	elif arg == "d":
		await asyncio.sleep(time * 60 * 60 * 24)

	await member.remove_roles( mute_role )
	await ctx.send(embed = discord.Embed(description = f'**:white_check_mark:Мут у пользователя {member.mention} успешно снят!:white_check_mark:**', color=0x800080))
	await member.send(embed = discord.Embed(description = f'{Переменная_размут}', color=0x800080))

@mute.error 
async def mute_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  

#Факты
@client.command(aliases = ['факт'], description ='Узнать рандомный факт')
async def fact(ctx):
	facts = nekos.fact() # Случайный факт ( на английском языке )
	t = Translator() # Переводчик
	result = t.translate(facts, dest = 'ru') # Выбираем текст, который будем редактировать ( в нашем случае facts и переводим на русский язык ( dest = 'ru'))

	embed = discord.Embed(color = 0x46faac) # Создаем эмбед
	embed.set_author(icon_url = 'https://www.flaticon.com/premium-icon/icons/svg/1177/1177379.svg', name = 'Другое | Факты')
	embed.description = result.text # Текст, который мы перевели ( переменная result )
	embed.set_footer(text = 'Факты')
	embed.timestamp = datetime.datetime.utcnow() # Дата
	await ctx.send(embed = embed) # Выводим текст


#напоминания 
@client.command(pass_context=True, description ='Поставить напоминание')
async def remind(ctx, time: int, tm: str, *, rem):
	author = ctx.author
	emb = discord.Embed(colour=0xFFF700, title='Напоминание ⏰',
						description=f'{author.mention} Напоминание успешно поставлено ✅')
	await ctx.send(embed=emb)
	#проверка переменной tm
	if tm == 'с':
		await asyncio.sleep(time)
	elif tm == 'м':
		await asyncio.sleep(time * 60)
	elif tm == 'ч':
		await asyncio.sleep(time * 3600)
	elif tm == 'д':
		await asyncio.sleep(time * 86400)
	#что есть возникла ошибка?
	else:
		emb = discord.Embed(colour=0xE40101, title='Ошибка',
							description=f'❌ Укажите аргументы\nПример: {PREFIX}remind 6 м Скушать козявку')
		await ctx.send(embed=emb)
		return
	emb = discord.Embed(title=f'Напоминание {author.name}', colour=0xFFF700)
	emb.add_field(name='Напоминание ⏰: ', value=f'**{rem}**')
	emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
	await ctx.send(embed=emb)


@remind.error
async def remind_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		emb = discord.Embed(colour=0xE40101, title='Ошибка',
							description=f':x: Укажите аргументы\nПример: {PREFIX}remind 6 м Скушать козявку')
		await ctx.send(embed=emb)
#Тикет
@client.command(description = 'подать жалобы или решить вашу проблему')
async def ticket(stx):
	await stx.channel.purge(limit = 1)
	author = stx.message.author
	guild = stx.message.guild
	creport = discord.utils.get(stx.guild.categories, name = '》═══◈Administration◈═══《')
	await guild.create_text_channel(f'ticket {author}', overwrites = None, category = creport, reason = 'Создание нового тикета.')
	server = client.get_guild(719476940997918780)
	for channel in server.channels:
		if channel.name == f'ticket {author}':
			break
	await channel.set_permissions(author, read_messages = True, send_messages = True)
	moder = discord.utils.get(stx.guild.roles, id = 719515916710445098)
	await channel.set_permissions(moder, read_messages = True, send_messages = True, manage_channels = True)
	alluser = discord.utils.get(stx.guild.roles, id = 719551303960756277)
	await channel.set_permissions(alluser, read_messages = False, send_messages = False)
	sup = discord.utils.get(stx.guild.roles, id = 719516297234481173)
	await channel.set_permissions(sup, read_messages = True, send_messages = True, manage_channels = True)
	emb = discord.Embed(title = 'Помощь :ambulance:', colour = discord.Color.dark_red())
	emb.add_field(name = f'Здравствуйте {author} ! Для решения Вашей проблемы мы создали отдельный чат с модерациейz сервера Discord.',
	value = '\n' 'Опишите Вашу проблему полностью и развёрнуто и модерация сервера ответит Вам. Старайтесь описывать проблему доступным для понимания текстом.')

	await channel.send(embed = emb)
	return

#userinfo
@client.command(description ='Узнать информацию о игроке')
async def user(ctx, member: discord.Member):
	member = ctx.author if not member else member
	roles = [role for role in member.roles]

	embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)

	embed.set_author(name = f"Информация пользователя - {member} ")
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(text = f"Запросил : {ctx.author}", icon_url = ctx.author.avatar_url)

	embed.add_field(name = "ID", value = member.id)
	embed.add_field(name = "Name", value = member.display_name)

	embed.add_field(name = "Зарегистрирован ", value = member.created_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))
	embed.add_field(name = "Вошел на сервер", value = member.joined_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))

	embed.add_field(name = f"Роли({len(roles)})", value = "".join(role.mention for role in roles))
	embed.add_field(name = "Высшая роль", value = member.top_role.mention)

	embed.add_field(name = "Бот", value = member.bot)

	await ctx.send(embed = embed)

#вОЙС
@client.event
async def on_voice_state_update(member,before,after):
	if after.channel.id == 724291400308490361:
		for guild in client.guilds:
			if guild.id == 719476940997918780:
				mainCategory = discord.utils.get(guild.categories, id=720183089074012180)
				channel2 = await guild.create_voice_channel(name=f"Канал {member.display_name}",category=mainCategory)
				await member.move_to(channel2)
				await channel2.set_permissions(member,manage_channels=True)
				def check(a,b,c):
					return len(channel2.members) == 0
				await client.wait_for('voice_state_update', check=check)
				await channel2.delete()

#Help (прошлый)
@client.command(description ='Все команды для бота Висмория')
async def lfwefkwefkwek(ctx):
	comm_list = []
	for command in client.commands:
		if not command.hidden:
			comm_list.append(f"`<v!>{command}` — {command.description}\n")
	embed = discord.Embed(
		title = f"Список команд для {client.user.name}:",
		description = "".join(comm_list),
		color = ctx.author.colour)
	embed.set_footer(text = f"Вызвано пользователем {ctx.author}", icon_url = ctx.author.avatar_url)
	embed.set_thumbnail(url = "https://cdn.discordapp.com/emojis/600405868693028875.png?v=1")
	
	await ctx.send(embed=embed)

#Размут
@client.command( hidden = True)
@commands.has_permissions( administrator = True)
async def unmute(ctx,member: discord.Member = None):
	mute_role = discord.utils.get( ctx.message.guild.roles, id = 721049136593371216 )
	if member is None:
		await ctx.send(embed = discord.Embed(description = f'❌{ ctx.author.name }, **обязательно укажите пользователя!**', color = 0x4f4db3 ))
		await ctx.message.add_reaction( '❌' )
	else:
		await member.remove_roles( mute_role )
		await ctx.message.add_reaction( '✅' )

@unmute.error 
async def unmute_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))


#предупреждение
@client.command(hidden = True )
@commands.has_permissions(administrator= True)
async def warn( ctx, member: discord.Member = None, *, arg = None ):
	if member is None:
		await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно укажите пользователя!**', color = 0x4f4db3 ))
		await ctx.message.add_reaction( '❌' )
	else:
		if arg is None:
			await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно укажите предупреждение!**', color = 0x4f4db3 ))
			await ctx.message.add_reaction( '❌' )
		else:
			await ctx.send( f'**{member.name}: получил предупреждение, случай `{random.randint( 1, 700 )}`: {arg}**' )
			await ctx.message.add_reaction( '✅' )

#Kill
@client.command(hidden = True)
@commands.has_role( 'Пистолет' )
async def kill( ctx, member : discord.Member = None ):
	awaitin = discord.utils.get( ctx.message.guild.roles, id = 721049136593371216 )

	embed = discord.Embed(description= f'{member.mention} был убит ', color=0x6fdb9e)

	await member.add_roles( awaitin )
	await ctx.send(embed = embed)

#Говорить
@client.command(hidden = True)
@commands.has_permissions( administrator = True)
async def say(ctx, *, arg):

	await ctx.message.delete()
	await ctx.send(embed = discord.Embed(description = f'{arg}', color= 0x72029c ))

#ping
@client.command(description = 'Узнать свой пинг')
async def ping(ctx):
	try:
		await ctx.message.delete()
	except:
		pass
	emb = discord.Embed(
		title= 'Текущий пинг',
		description= f'{client.ws.latency * 1000:.0f} ms'
	)
	await ctx.send(embed=emb)

#server info
@client.command( description = 'Узнать информацию о сервере' )
async def serverinfo(ctx):
	members = ctx.guild.members
	online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
	offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
	idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
	dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
	embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
	embed.description=(
		f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
		f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **=Leo=#7193**\n\n"
		f":tools:  Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
		f":green_circle:  Онлайн: **{online}**\n\n"
		f":black_circle:  Оффлайн: **{offline}**\n\n"
		f":yellow_circle:  Отошли: **{idle}**\n\n"
		f":red_circle:  Не трогать: **{dnd}**\n\n"
		f":detective: Людей на сервере **{ctx.guild.member_count}\n\n"
	)

	embed.set_thumbnail(url=ctx.guild.icon_url)
	embed.set_footer(text=f"ID: {ctx.guild.id}")
	embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
	await ctx.send(embed=embed)
	
#Clear 
@client.command( hidden = True )
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
	
	channel_log = client.get_channel(731238565467390022) #Айди канала логов

	await ctx.channel.purge( limit = amount )
	await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))
	await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0x0c0c0c))

@clear.error 
async def clear_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

	if isinstance( error, commands.MissingRequiredArgument  ): 
		await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0x0c0c0c))    

#on_ready

@client.event
async def on_ready():
	print('BOT connected')
	
	act = f'?help'
	await client.change_presence(activity=discord.Streaming(name=str(act), url='https://www.twitch.tv/leontizzz'))

#Help for administrator 
@client.command(description = 'Команды для админов' )

async def admin( ctx ):

	emb1 = discord.Embed( title = 'Команды для модераторов', colour = 0x2ecc71)

	emb1.add_field(name = '{}mute'.format(ctx.prefix), value = 'Временный мут   ',)
	emb1.add_field(name = '{}ban'.format(ctx.prefix), value = 'Бан пользователя   ',)
	emb1.add_field(name = '{}clear'.format(ctx.prefix), value = 'Очистка чата   ',)
	emb1.add_field(name = '{}kick '.format(ctx.prefix), value = 'Кик пользователя   ',)
	emb1.add_field(name = '{}unmute '.format(ctx.prefix), value = 'Снятие мута   ',)
	emb1.add_field(name = '{}say '.format(ctx.prefix), value = 'Говорить от имени бота   ',)
	emb1.add_field(name = '{}warn '.format(ctx.prefix), value = 'Выдать предупреждение  ',)
	emb1.add_field(name = '{}statstream '.format(ctx.prefix), value = 'Статус бота "Стримит"  ',)
	emb1.add_field(name = '{}statlisten '.format(ctx.prefix), value = 'Статус бота "Слушает"  ',)
	emb1.add_field(name = '{}statwatch'.format(ctx.prefix), value = 'Статус бота "Смотрит"  ',)
	emb1.add_field(name = '{}statplay '.format(ctx.prefix), value = 'Статус бота "Играет в"  ',)

	await ctx.send( embed = emb1)


#Аватар 
@client.command(description = 'Посмотреть аватар пользователя или свой')

async def avatar(ctx, member : discord.Member = None):
	await ctx.message.delete()
	user = ctx.message.author if (member == None) else member
	embed = discord.Embed(title=f'Аватар пользователя {member}', color = 0xFFC0CB)

	embed.set_image(url = user.avatar_url)
	embed.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
	await ctx.send(embed=embed)

#Админская предложка
@client.command( pass_context = True, hidden = True ) 
async def suggestadmin( ctx , * , agr ):
	suggest_chanell = client.get_channel(732262355089621052)
	embed = discord.Embed(title=f"{ctx.author.name} предложил :", description= f" {agr} \n\n")

	embed.set_thumbnail(url=ctx.guild.icon_url)

	message = await suggest_chanell.send(embed=embed)
	await message.add_reaction('✅')
	await message.add_reaction('❎')

#Преды для стажёров
@client.command(hidden = True )
@commands.has_role( 'Helper『📌』' )
async def пред( ctx, member: discord.Member = None, *, arg = None ):
	if member is None:
		await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно укажите пользователя!**', color = 0x4f4db3 ))
		await ctx.message.add_reaction( '❌' )
	else:
		if arg is None:
			await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно укажите предупреждение!**', color = 0x4f4db3 ))
			await ctx.message.add_reaction( '❌' )
		else:
			await ctx.send( f'**{member.name}: получил предупреждение, случай `{random.randint( 1, 700 )}`: {arg}**' )
			await ctx.message.add_reaction( '✅' )

#Мут для стажёров
@client.command( pass_context = True, hidden = True)
@commands.has_role( 'Helper『📌』' )
async def мут(ctx, member : discord.Member, time:int, arg:str, *, reason=None):

	Переменная_размут = f'**Вы были размучены на сервере {ctx.guild.name}**'
	Переменная_мут = f'**Вы были замучены на сервере {ctx.guild.name} на {time}{arg} по причине: {reason}**'
	mute_role = discord.utils.get( ctx.message.guild.roles, id = 721049136593371216 )

	await member.add_roles(mute_role, reason=None, atomic=True)
	await ctx.send(embed = discord.Embed(description = f'**:shield:Мут пользователю {member.mention} успешно выдан на {time}{arg} по причине {reason} :shield:**', color=0x0000FF))
	await member.send(embed = discord.Embed(description = f'{Переменная_мут}', color=0x0c0c0c))

	if arg == "s":
		await asyncio.sleep(time)          
	elif arg == "m":
		await asyncio.sleep(time * 60)
	elif arg == "h":
		await asyncio.sleep(time * 60 * 60)
	elif arg == "d":
		await asyncio.sleep(time * 60 * 60 * 24)

	await member.remove_roles( mute_role )
	await ctx.send(embed = discord.Embed(description = f'**:white_check_mark:Мут у пользователя {member.mention} успешно снят!:white_check_mark:**', color=0x800080))
	await member.send(embed = discord.Embed(description = f'{Переменная_размут}', color=0x800080))

@mute.error 
async def mute_error(ctx, error):

	if isinstance( error, commands.MissingPermissions ):
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))  

#Размут для стажёров
@client.command( hidden = True)
@commands.has_role( 'Helper『📌』' )
async def размут(ctx,member: discord.Member = None):
	mute_role = discord.utils.get( ctx.message.guild.roles, id = 721049136593371216 )
	if member is None:
		await ctx.send(embed = discord.Embed(description = f'❌{ ctx.author.name }, **обязательно укажите пользователя!**', color = 0x4f4db3 ))
		await ctx.message.add_reaction( '❌' )
	else:
		await member.remove_roles( mute_role )
		await ctx.message.add_reaction( '✅' )


#knb
@client.command(description = 'КНБ с ботом')
async def knb(ctx, move: str = None):
	solutions = ["`ножницы`", "`камень`", "`бумага`"]
	winner = "**НИЧЬЯ**"
	p1 = solutions.index(f"`{move.lower()}`")
	p2 = randint(0, 2)
	if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
		winner = f"{ctx.message.author.mention} ты **Проиграл**"
	elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
		winner = f"{ctx.message.author.mention} ты **Выиграл**"
	await ctx.send(    
		f"{ctx.message.author.mention} **=>** {solutions[p1]}\n"
		f"{client.user.mention} **=>** {solutions[p2]}\n"
		f"{winner}")

#Роль на время
@client.command(hidden = True )
@commands.has_permissions(administrator = True)
async def temp_add_role(ctx, amount : int, member: discord.Member = None, role: discord.Role = None):

	try:

		if member is None:

			await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

		elif role is None:

			await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: роль!**'))

		else:

			await discord.Member.add_roles(member, role)
			await ctx.send(embed = discord.Embed(description = f'**Роль успешна выдана на {amount} секунд!**'))
			await asyncio.sleep(amount)
			await discord.Member.remove_roles(member, role)

	except:
		
		await ctx.send(embed = discord.Embed(description = f'**:exclamation: Не удалось выдать роль.**', color=0x0c0c0c))


#Саппорт
@client.command(hidden = True)
@commands.has_permissions ( administrator = True )
async def accept( ctx, member : discord.Member ):
	accepted = discord.utils.get( ctx.message.guild.roles, id = 719516297234481173 ) # Айди роли принятого
	awaiting = discord.utils.get( ctx.message.guild.roles, id = 729314153314910240 ) # Айди роли ожидающего

	await member.add_roles(accepted, reason=None, atomic=True) # Добавление роли принятого
	await member.remove_roles( awaiting ) # Снимание роли ожидающего

	await ctx.send ( embed = discord.Embed(description = f'**:shield:{member.name} Принят! **', color=0x0000FF) )

#Свергнуть 
@client.command(hidden = True)
@commands.has_permissions ( administrator = True )
async def свергнуть( ctx, member : discord.Member ):
	awaiting = discord.utils.get( ctx.message.guild.roles, id = 719515758635253852 )

	await member.remove_roles( awaiting )


#Шар
@client.command(name = "8ball", description = 'Шар предсказаний ' )
async def ball(ctx, *, arg):

	message = ['Нет','Да','Возможно','Опредленно нет'] 
	s = random.choice( message )
	await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0x0c0c0c))
	return

@ball.error 
async def ball_error(ctx, error):

	if isinstance( error, commands.MissingRequiredArgument ): 
		await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите сообщение.', color=0x0c0c0c)) 



#Логи

#Вики
@client.command(description = 'Википедия ')
async def wiki(ctx, *, text):
	wikipedia.set_lang("ru")
	new_page = wikipedia.page(text)
	summ = wikipedia.summary(text)
	emb = discord.Embed(
		title= new_page.title,
		description= summ,
		color = 0x00ffff
	)
	emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

	await ctx.send(embed=emb)

#Обои
@client.command()
async def wallpapers(ctx):
	img_url = nekos.img('wallpaper')
		
	emb = discord.Embed(description= f'**Вот подобраные Вам обои.\n[Ссылка]({img_url})**')
	emb.set_image(url= img_url)
	await ctx.send(embed=emb)

#Аватарка 
@client.command()
async def ran_avatar(ctx):
	emb = discord.Embed(description= 'Вот подобраная Вам аватарка.', color=0x6fdb9e)
	emb.set_image(url=nekos.img('avatar'))
	await ctx.send(embed=emb)

#Help
@client.command(name = 'v!help')
async def __help(ctx):
	embed1 = discord.Embed(title = 'Команды для Висмория',
		description = '`v!wallpapers` —— Случайные аниме обои\n\n`v!fact` —— Узнать рандомный факт\n\n`v!8ball` —— Шар предсказаний\n\n`v!remind` —— Поставить напоминание\n\n`v!ticket` —— Подать жалобы , решить вашу проблему или отправить предложение\n\n`v!wiki` —— Википедия\n\n`v!user` —— Узнать информацию о игроке')
	embed2 = discord.Embed(title = 'Команды для Висмория',
		description = '`v!ran_avatar` —— Рандомная аниме аватарка\n\n`v!help` —— Все команды для бота Висмория\n\n`v!ping` —— Узнать пинг бота\n\n`v!serverinfo` —— Узнать информацию о сервере\n\n`v!admin` —— Команды для админов\n\n`v!avatar` —— Посмотреть аватар пользователя или свой\n\n`v!knb` —— КНБ с ботом')
	embed3 = discord.Embed(title = 'Команды для Висмория',
		description = '`v!hug` —— Будь лапочкой, обними кого-нибудь\n\n`v!lick` —— Лизни кого-нибудь сладенького\n\n`v!drink` —— Выпей с кем-то за здоровье бота\n\n`v!punch`  ——НЫАААА\n\n`v!pat` —— Сделай кому-нибудь приятно, погладь его\n\n`v!poke` —— Тык :3\n\n`v!cry` —— Всплакни, если тебе стало грустно :c')
	embed4 = discord.Embed(title ='Команды для Висмория',
		description = '`v!battle` —— Начать бой\n\n`v!hentai` —— Тут всё понятно\n\n`v!choose` —— Выбрать из перечисленного\n\n`v!slots` —— Выбей 777 и получи роль\n\n`v!game` —— Орёл и Решка')
	embeds = [embed1, embed2, embed3, embed4]
	exit_reaction = ["❌"]

	message = await ctx.send(embed = embed1)
	page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, timeout = 60, use_exit = True, exit_reaction = exit_reaction)
	await page.start()

#Лео
@client.command(hidden = True)
@commands.has_permissions ( administrator = True )
async def принять( ctx, member : discord.Member ):
	awaiting = discord.utils.get( ctx.message.guild.roles, id = 735477732485365771 )

	embed = discord.Embed(description= f'LeoClub принимает нового участника - {member.mention}', color=0x6fdb9e)
	embed.set_image(url= 'https://cdn.discordapp.com/attachments/495581976120655874/593450061573259265/unknown.png')

	await member.add_roles( awaiting )
	await ctx.send(embed = embed)


#Кутсубес
@client.command(hidden = True)
async def kutsubes( ctx, member : discord.Member ):

	embed = discord.Embed(description= f'{ctx.author.mention} закутсубесил {member.mention}', color=0x6fdb9e)
	embed.set_image(url= 'https://media.discordapp.net/attachments/468433368820744232/735266984329216020/Screenshot_30.png')

	await ctx.send(embed = embed)

#Лео 2
@client.command(hidden = True)
@commands.has_permissions ( administrator = True )
async def выгнать( ctx, member : discord.Member ):
	awaiting = discord.utils.get( ctx.message.guild.roles, id = 735477732485365771 )

	embed = discord.Embed(description= f'LeoClub исключает участника - {member.mention}', color=0x6fdb9e)

	await member.remove_roles( awaiting )
	await ctx.send(embed = embed)


#lick
@client.command(hidden = True)
async def лизнуть( ctx, member : discord.Member ):

	embed = discord.Embed(description= f'**{ctx.author.mention} облизывает {member.mention}**, он такой мокрый!', color=0x6fdb9e)
	embed.set_image(url= 'https://data.whicdn.com/images/182507095/original.gif')

	await ctx.send(embed = embed)

#Drink
@client.command(hidden = True)
async def ебнуть( ctx, member : discord.Member ):

	embed = discord.Embed(description= f'**{ctx.author.mention} выпивает с {member.mention}**, алкоголь - это **жизнь**', color=0x6fdb9e)
	embed.set_image(url= 'https://data.whicdn.com/images/247827296/original.gif')

	await ctx.send(embed = embed)

#hug 
@client.command(hidden = True)
async def обнять( ctx, member : discord.Member ):


	embed = discord.Embed(description= f'**{ctx.author.mention} обнимает {member.mention}**, обнимашки!!!', color=0x6fdb9e)
	embed.set_image(url= 'https://i.imgur.com/ZQivdm1.gif')

	await ctx.send(embed = embed)

#punch
@client.command(hidden = True)
async def ударить( ctx, member : discord.Member ):

	embed = discord.Embed(description= f'**{ctx.author.mention} бьет {member.mention}**, НЫААА', color=0x6fdb9e)
	embed.set_image(url= 'https://data.whicdn.com/images/286895006/original.gif')

	await ctx.send(embed = embed)

#pat
@client.command(hidden = True)
async def гладить( ctx, member : discord.Member ):

	embed = discord.Embed(description= f'**{ctx.author.mention} гладит {member.mention}**', color=0x6fdb9e)
	embed.set_image(url= 'https://data.whicdn.com/images/297126289/original.gif')

	await ctx.send(embed = embed)
#poke
@client.command(hidden = True)
async def тыкнуть( ctx, member : discord.Member ):

	embed = discord.Embed(description= f'**{ctx.author.mention} тыкает {member.mention}**, тык', color=0x6fdb9e)
	embed.set_image(url= 'https://gifimage.net/wp-content/uploads/2017/09/anime-poke-gif-11.gif')

	await ctx.send(embed = embed)

#cry
@client.command(hidden = True)
async def плакать( ctx ):

	embed = discord.Embed(description= f'**{ctx.author.mention} плачет из-за фальшивых друзей**', color=0x6fdb9e)
	embed.set_image(url= 'https://media3.giphy.com/media/mvRwcoCJ9kGTS/source.gif')

	await ctx.send(embed = embed)

#suicjeqfjqe
@client.command(hidden = True)
async def суицид( ctx ):

	embed = discord.Embed(description= f'**{ctx.author.mention} совершил самоубийство!**', color=0x6fdb9e)
	embed.set_image(url= 'https://cdn.discordapp.com/attachments/573577159063502848/579922653356228619/tumblr_na1x87xfqE1twpohao1_500.gif')

	await ctx.send(embed = embed)

#battle
@client.command()
async def battle( ctx, member: discord.Member = None ):
	if member is None:
		await ctx.send('С кем ты хочешь перестреляться !')
	else:
		a = random.randint(1,2)
		if a == 1:
			emb = discord.Embed( title = f"Победитель - {ctx.author}", color = 0x8b00ff)
			await ctx.send( embed = emb )

			emb = discord.Embed( title = f"Проигравший - {member}", color = 0x8b00ff)
			await ctx.send( embed = emb )
		elif member.id == ctx.author.id:
			emb = discord.Embed( title = f"Вы не можете с собой сражаться !", color = 0x8b00ff)
			await ctx.send( embed = emb )
		else:
			emb = discord.Embed( title = f"Победитель - {member}", color = 0x8b00ff)
			await ctx.send( embed = emb )

			emb = discord.Embed( title = f"Проигравший - {ctx.author}", color = 0x8b00ff)
			await ctx.send( embed = emb )

#Hentai
@client.command()
async def hentai(ctx, endpoint = 'nekolewd'):
	if not ctx.message.channel.is_nsfw():
		emb = discord.Embed(title = 'Не бузи!', description = f':x: {ctx.author.mention}, эту **команду** можно писать только в **NSFW канале** :x:', colour = 0xFF0000)
		emb.set_author(icon_url = 'https://www.flaticon.com/premium-icon/icons/svg/1828/1828665.svg', name = 'Бот | Ошибка')
		emb.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
		await ctx.send(embed = emb)
		return
	r = requests.get("https://neko-love.xyz/api/v1/" + endpoint)
	if r.status_code != 200:
		pass
	else:
		emb = discord.Embed(color = 0x00FF00)
		emb.set_footer(text = f'{client.user.name} © 2020 | Все права защищены', icon_url = client.user.avatar_url)
		emb.set_image(url = r.json()["url"])
		await ctx.send(embed=emb)

#slots
@client.command()
async def slots(ctx):
	responses = ["🍋" , "🍊", "🍉", ":seven:", ]
	embed=discord.Embed(title="🎰 Slot Machine 🎰", description=random.choice(responses) + random.choice(responses) + random.choice(responses), color=0x176cd5)
	embed.set_footer(text = f"Вызвано пользователем {ctx.author}", icon_url = ctx.author.avatar_url)
	await ctx.send(embed=embed)

#choose
@client.command()
async def choose(ctx, *choices : str):
	embed=discord.Embed(title=' Я выбираю :', description = random.choice(choices),  value=random.choice(choices), inline=True, color=0x176cd5)
	await ctx.send(embed=embed)

#Орёл решка
@client.command()
async def game(ctx):
	a = random.randint(1, 2)
	if a == 1:
		emb = discord.Embed(title = '__**Орёл и решка**__', color = discord.Colour.blue())
		emb.add_field(name = 'Что выпало:', value = '*Вам выпал* __**орёл**__')       
		emb.set_thumbnail(url = 'https://i.gifer.com/ZXv0.gif')
		await ctx.send(embed = emb)
		emb.set_footer(text=f"Запросил: {ctx.author}", icon_url=ctx.author.avatar_url)
	else:
		emb = discord.Embed(title = '__**Орёл и решка**__', color = discord.Colour.red())
		emb.add_field(name = 'Что выпало:', value = '*Вам выпала* __**решка**__')        
		emb.set_thumbnail(url = 'https://i.gifer.com/ZXv0.gif')
		await ctx.send(embed = emb)
		emb.set_footer(text=f"Запросил: {ctx.author}", icon_url=ctx.author.avatar_url)

#
@client.command()
async def meme(self, ctx):
  await ctx.message.add_reaction("✅")
  emb = discord.Embed(description= 'Вот подобраный мем.', color=0x00ffff)
  emb.set_image(url= random_meme())
  await ctx.send(embed=emb)

#
@client.command()
async def google(self, ctx, *, question):
  await ctx.message.add_reaction("✅")  # погуглить
  # сам сайт
  url = 'https://google.gik-team.com/?q=' + str(question).replace(' ', '+')
  await ctx.send(f'Так как кое кто не умеет гуглить , я сделал это за него.\n{url}')

#Участники 
@client.command()
async def members_info(ctx):
	server_members = ctx.guild.members
	data = "\n".join([i.name for i in server_members])
	embed = discord.Embed(title=f'Все участники сервера:', description = f"{data}" , color= 0x0c0c0c)

	await ctx.send(embed = embed)

#Роли
@client.command()
async def roleinfo(ctx, Role: discord.Role ):
	await ctx.message.add_reaction("✅")
	guild = ctx.guild
	emb = discord.Embed(title='Информация о роли .'.format(Role.name), description=f"Роль создали {Role.created_at.strftime('%b %#d, %Y')}\n\n"
																				   f"Название роли: {Role.name}\n\nЦвет: {Role.colour}\n\n"
																				   f"Позиция: {Role.position}\n\n",colour= Role.colour, timestamp=ctx.message.created_at)

	emb.set_footer(text=f"ID Пользователя: {ctx.author.id}", icon_url=ctx.author.avatar_url)
	await ctx.send(embed=emb)

#
@client.command(aliases=['коронавирус', 'ковид'])
async def covid(ctx, country):
		for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
			if item['country'] == country: 
				embed = discord.Embed(title=f'Статистика Коронавируса | {country}')
				embed.add_field(name='Выздоровело:',          value=f'{item["recovered"]} человек')
				embed.add_field(name='Заболеваний:',          value=f'{item["cases"]} человек')
				embed.add_field(name='Погибло:',              value=f'{item["deaths"]} человек')
				embed.add_field(name='Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
				embed.add_field(name='Погибло за сутки:',     value=f'+{item["todayDeaths"]} человек')
				embed.add_field(name='Проведено тестов:',     value=f'{item["tests"]} человек')
				embed.add_field(name='Активные зараженные:',  value=f'{item["active"]} человек')
				embed.add_field(name='В тяжелом состоянии:',  value=f'{item["critical"]} человек')
				embed.set_thumbnail(url=item["countryInfo"]['flag'])
				embed.set_footer(text="© Copyright 2020 хто я#0000 | Все права съедены")

				return await ctx.send(embed=embed)



token = os.environ.get('BOT_TOKEN')