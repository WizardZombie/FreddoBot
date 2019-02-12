import discord
from discord.ext import commands
import asyncio
import logging
import aiohttp
import io
import json
import math
from datetime import datetime, date, time, timedelta
import utils.config as config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='£', description="ModMail Bot. DM with concerns.")

token = config.get_token()
originalFreddo = config.get_original()
freddoPrice = config.get_freddo()
rates = None
lastUpdate = None

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------') 
	global rates 
	await load_rates()
	await bot.change_presence(game=discord.Game(name='£convert to Freddoise your currency.'))
	


@bot.event
async def on_command_error(error, ctx):
	print(error)

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	else:
		await bot.process_commands(message)

@bot.command()
async def convert(value, currency = 'USD'):
	"""Converts the value of the currency given into Freddos. Currency must be provided in standard 3 letter format (ex: USD, AUD, GBP, EUR). Defaults to USD, Freddo prices accurate as of 2019-02-07"""
	await check_rates()
	excRates = rates['rates']
	sterlingValue = float(value)/float(excRatesexcRates[currency.upper()])
	freddoAmount = math.floor(sterlingValue/freddoPrice)
	originalAmount = math.floor(sterlingValue/originalFreddo)
	em = discord.Embed(title="**__Freddo Value__**", description= value + ' ' + currency + ' is currently worth:', colour=0x52ff38)
	em.add_field(name='**Todays Freddo:**', value=str(freddoAmount) + ' Freddos', inline=True)
	em.add_field(name='**Original Freddo:**', value=str(originalAmount) + ' Freddos', inline=True)
	em.set_footer(text=value + ' ' + currency + ' = ' + str(sterlingValue) + ' GBP. Exchange Rates correct as of ' + lastUpdate.isoformat() + '. Exchange Rates courtesy of https://exchangeratesapi.io')
	await bot.say(embed=em)

@bot.command()
async def currentrates():
	await check_rates()
	em = discord.Embed(title='**__Current Exchange Rates__**', description='*As compared to GBP*')
	excRates = rates['rates']
	for rate in excRates:
		if rate == 'GBP':
			pass
		else:
			em.add_field(name='**' + rate + ':**', value=str(excRates[rate]), inline=True)
	em.add_field(name='**Current Freddo**', value='£' + str(freddoPrice), inline=True)
	em.add_field(name='**Original Freddo**', value='£' + str(originalFreddo), inline=True)
	em.set_footer(text='Exchange Rates correct as of ' + lastUpdate.isoformat() + '. Exchange Rates courtesy of https://exchangeratesapi.io. Freddo Price correct as of 2019-02-07.')
	await bot.say(embed=em)

async def load_rates():
	global rates, lastUpdate
	try:
		with open('utils/rates.txt') as data_file:
			rates = json.load(data_file)
		lastUpdated = rates['last_updated']
		lastUpdate = datetime(lastUpdated['year'], lastUpdated['month'], lastUpdated['day'], lastUpdated['hour'], lastUpdated['minute'], lastUpdated['second'])
		await check_rates()
	except FileNotFoundError:
		await update_rates()

async def check_rates():
	updateDelta = datetime.utcnow() - lastUpdate
	if updateDelta.days >= 1:
			await update_rates()
	else:
		return

async def update_rates():
	global lastUpdate, rates
	apiResp = None
	async with aiohttp.ClientSession() as session:
		async with session.get('https://api.exchangeratesapi.io/latest?base=GBP') as resp:
			apiResp = await resp.json()
			await session.close()
		rates = apiResp
		lastUpdate = datetime.utcnow()
		rates['last_updated'] = {'year':lastUpdate.year, 'month':lastUpdate.month, 'day':lastUpdate.day, 'hour':lastUpdate.hour, 'minute':lastUpdate.minute, 'second':lastUpdate.second}
		with io.open('utils/rates.txt', 'w', encoding='utf-8') as f:
			f.write(json.dumps(rates, sort_keys=True, indent=4, ensure_ascii=False))
	

bot.run(token)
