import discord
import numpy_financial as np
from babel.numbers import format_currency
import requests
from bs4 import BeautifulSoup

client = discord.Client()
URL = "https://money.rediff.com/indices/nse/nifty-50?src=indticker"
helpString = """
There are two commands(.rd and .sip)

.goal <goal_amount> <year> <interest> <goal_name>
.sip <sip_amount> <year> <returns>
.lumpsum <initial_amount> <year> <returns>
.present <future_value> <year> <inflation>
.nifty
year is optional with default value as 3 years
interest/returns is optional with default value as 5.5% pa
goal_Name is optional but please fill all 4 arguments if you want to add goalName

Hosted on AWS Bitches!!!!!
"""


async def sipCalculation(message):
    years = 3
    interest = 5.5
    messagaData = message.content.split(" ")
    sipAmount = messagaData[1]
    if(len(messagaData) >= 3):
        years = messagaData[2]
    if(len(messagaData) >= 4):
        interest = float(messagaData[3])
    if(float(sipAmount) < 0 or float(years) < 0 or float(interest) < 0):
        await message.channel.send("Arguments cannot be negative")
        return
    print(message.author)
    futureAmount = np.fv(interest / 1200, float(years)
                         * 12, -float(sipAmount), -float(sipAmount))
    capitalInvested = int(sipAmount)*float(years) * 12
    return "Hello {4.mention},\nIf you invest {0} per month for {1} years at {2}% CAGR then the accumulated corpus will be {3} where the capital invested would be {5}".format(
        format_currency(sipAmount, 'INR', locale='en_IN'), years, interest, format_currency(futureAmount, 'INR', locale='en_IN'), message.author, format_currency(capitalInvested, 'INR', locale='en_IN'))


async def recurringDepositCalculation(message):
    years = 3
    interest = 5.5
    goal = ""
    messagaData = message.content.split(" ")
    amount = messagaData[1]
    if(len(messagaData) >= 3):
        years = messagaData[2]
    if(len(messagaData) >= 4):
        interest = float(messagaData[3])
    if(len(messagaData) >= 5):
        goal = messagaData[4]
    if(float(amount) < 0 or float(years) < 0 or float(interest) < 0):
        await message.channel.send("Arguments cannot be negative")
        return
    sip = np.ppmt(interest / 1200, 1, float(years) * 12, float(amount))
    goal_message = "reach your goal"
    if(goal != ""):
        goal_message = "get your {0}".format(goal)
    capitalInvested = int(sip)*float(years) * 12
    return "Hello {4.mention},\nYou need to contribute {0} per month to {5} of {1}  in {2} year(s) assuming interest rate of {3}% pa  where the capital invested would be {6}".format(
        format_currency(-sip, 'INR', locale='en_IN'), format_currency(amount, 'INR', locale='en_IN'), years, interest, message.author, goal_message, format_currency(-capitalInvested, 'INR', locale='en_IN'))


async def futureValueCalculation(message):
    years = 3
    interest = 5.5
    messagaData = message.content.split(" ")
    amount = messagaData[1]
    if(len(messagaData) >= 3):
        years = float(messagaData[2])
    if(len(messagaData) >= 4):
        interest = float(messagaData[3])
    if(float(amount) < 0 or float(years) < 0 or float(interest) < 0):
        await message.channel.send("Arguments cannot be negative")
        return
    futureAmount = np.fv(interest / 100, float(years), 0, -float(amount))
    return "Hello {4.mention},\nYour lumpsum amount of {0} invested at CAGR of {1}% pa will become {3} in {2} year(s)".format(
        format_currency(amount, 'INR', locale='en_IN'), interest, int(years), format_currency(futureAmount, 'INR', locale='en_IN'), message.author)


async def presentValueCalculation(message):
    years = 3
    interest = 5.5
    messagaData = message.content.split(" ")
    amount = messagaData[1]
    if(len(messagaData) >= 3):
        years = float(messagaData[2])
    if(len(messagaData) >= 4):
        interest = float(messagaData[3])
    if(float(amount) < 0 or float(years) < 0 or float(interest) < 0):
        await message.channel.send("Arguments cannot be negative")
        return
    presentAmount = np.pv(interest / 100, float(years), 0, -float(amount))
    return "Hello {4.mention},\nYour future value of {0} {1}years from now considering inflation rate at {2} is really just {3} in present value".format(
        format_currency(amount, 'INR', locale='en_IN'), int(years), interest, format_currency(presentAmount, 'INR', locale='en_IN'), message.author)


async def getLiveIndexPrice():
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
    price=soup.find("span", id="ltpid").text
    change=soup.find("span", class_="change-pts").text
    percentChange = float(change)*100/float(price)
    if(change.startswith("-")):
        change = ":chart_with_downwards_trend: {0}".format(change)
    else:
        change = ":chart_with_upwards_trend: {0}".format(change)
    return "**NIFTY50**\n_Price_ {0} ({2:.2f}%)\n_Change_ {1}".format(format_currency(float(price), 'INR', locale='en_IN'), change, percentChange)

async def annoyPerson():
    return ""

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("type .help"))


@client.event
async def on_message(message):
    try:
        if(message.content.startswith(".help")):
            await message.channel.send(helpString)
        if(message.content.startswith(".sip")):
            await message.channel.send(await sipCalculation(message))
        if(message.content.startswith(".goal")):
            await message.channel.send(await recurringDepositCalculation(message))
        if(message.content.startswith(".lumpsum")):
            await message.channel.send(await futureValueCalculation(message))
        if(message.content.startswith(".present")):
            await message.channel.send(await presentValueCalculation(message))
        if(message.content.startswith(".nifty")):
            await message.channel.send(await getLiveIndexPrice())
        if(message.author.equals("namasteOriginally#4013")):
            await message.channe.send(await annoyPerson())
    except Exception as inst:
        print(inst)
        await message.channel.send("Something went wrong. Please use .help for details")


client.run("ODM1MDA0MDYxMjYyMjgyNzYz.YIJIIQ.rSmy0HGZIP8YOuuOvMqiVA4EMdU")

