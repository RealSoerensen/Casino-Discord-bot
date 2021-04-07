import discord
from discord.ext import commands
import random
import os
from replit import db
import keep_alive
import asyncio
import time

intents = discord.Intents()
intents.members = True
intents.messages = True
prefix = "%"
bot = commands.Bot(command_prefix=(prefix), intents=intents)
loop = asyncio.get_event_loop()

@bot.event
async def on_ready():
  await bot.change_presence(activity = discord.Game('Use %comms to see all commands'))
  print ('Logged in as: {0.user}'.format(bot))
  
@bot.command()
async def comms(Commands):
  await Commands.send("The commands you can currently use is as following:\n%daily\n%bal\n%userbal {@ any user}\n%lb\n%cf {heads/tails} {bet}\n%dice {number between 1-6} {bet}\n%slots {amount of spins} {bet per spin}")

@bot.command()
async def bal(Balance):
  #Get all userIds
  allUserIds = db.keys()

  userId = Balance.author.id

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance

  userName = bot.get_user(userId)
  await Balance.send(f"{userName} current balance is {balance}$")

@bot.command()
async def userbal(bal, user: discord.User):
  #Get all userIds
  allUserIds = db.keys()
  userId = user.id

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    userName = bot.get_user(userId)
    await bal.send(f"{userName} current balance is {balance}$")
    return

  await bal.send("User doesn't exist in database")

@bot.command()
async def deletebal(deleteBal, user: discord.User):
  #Get all userIds
  userId = user.id
  owner = 217751208008351745
  print(deleteBal.author.id)

  if owner == deleteBal.author.id:
    del db[userId]
    await deleteBal.send(f"{bot.get_user(userId)}'s balance has been deleted")
    return

  await deleteBal.send("You don't have permission to use this command")
  return

@bot.command()
async def give(giveBal, user: discord.User, value):
  #Get userIds
  userId = user.id

  #Get all userIds
  allUserIds = db.keys()

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance
    
  balance = db[userId]
  owner = 217751208008351745

  if owner == giveBal.author.id:
    money = int(value)
    db[userId] = balance + money
    await giveBal.send(f"{money}$ has been added to {bot.get_user(userId)}'s balance. Their balance is now {db[userId]}")
    return

  await giveBal.send("You don't have permission to use this command")
  return

@bot.command()
async def lb(Leaderboard):
  allUserIds = db.keys()
  userAndBalance = []
  userCounter = 0

  for userId in allUserIds:
    try:
      userInfo = await bot.fetch_user(userId)
      userName = userInfo.name
      balance = db[userId]
    except:
      continue

    user = (balance, userName)
    userAndBalance.append(user)
    userCounter += 1

  userAndBalanceSet = frozenset(userAndBalance)
  userAndBalanceSet = sorted(userAndBalanceSet, reverse=True)

  userAndBalanceDict = {}
  for user in range(userCounter):
    positions = [i for i, x in enumerate(userAndBalance) if x == userAndBalanceSet[user]]
    userAndBalanceDict[userAndBalanceSet[user]] = positions

  counter = 0
  rank = 1
  whileCounter = 11
  newList = []

  while rank < whileCounter:
    userAndBalanceString = str(userAndBalanceSet[counter])
    symbolsToRemove = "()"
    for char in symbolsToRemove:
      userAndBalanceString = userAndBalanceString.replace(char,"")
    newList.append(userAndBalanceString.split(", "))

    counter += 1
    rank += 1

  await Leaderboard.send(f"There are currently {userCounter} users who have used me\n1st place: {newList[0][1]} with {newList[0][0]}$\n2nd place: {newList[1][1]} with {newList[1][0]}$\n3rd place: {newList[2][1]} with {newList[2][0]}$\n4th place: {newList[3][1]} with {newList[3][0]}$\n5th place: {newList[4][1]} with {newList[4][0]}$\n6th place: {newList[5][1]} with {newList[5][0]}$\n7th place: {newList[6][1]} with {newList[6][0]}$\n8th place: {newList[7][1]} with {newList[7][0]}$\n9th place: {newList[8][1]} with {newList[8][0]}$\n10th place: {newList[9][1]} with {newList[9][0]}$")

@bot.command()
async def rou(Roulette, bet):
  #Get all userIds
  allUserIds = db.keys()
  bet = int(bet)
  if bet <= 0:
    await Roulette.send("Please enter a valid input")
    return

  userId = Roulette.author.id

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance

  balance = db[userId]

  if balance < bet:
    await Roulette.send("Bet is too big!")
    return

  newBalance = balance - bet
  db[userId] = newBalance

@bot.command()
async def rourules(rouletteRules):
  await rouletteRules.send("Roulette rules are coming")

@bot.command()
async def cf(Coinflip, choice, bet):
  #Get all userIds
  allUserIds = db.keys()
  userId = Coinflip.author.id

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    #Set balance to 100 if balance is = 0
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance

  if bet == 'all':
    bet = balance
  
  else:
    bet = bet

  bet = int(bet)

  if balance < bet:
    await Coinflip.send("Bet is too big!")
    return

  if bet <= 0	:
    await Coinflip.send("Please enter a valid input")
    return

  db[userId] = balance - bet  

  if choice == "heads":
    if random.randint(0, 100) < 50:
      winning = bet * 2
      db[userId] = db[userId] + winning
      await Coinflip.send(f"You win: {winning}$!\nYour current balance is: {db[userId]}$")
      return

    else:
      await Coinflip.send("You lose, better luck next time!")
      return

  elif choice == "tails":
    if random.randint(0, 100) > 50:
      winning = bet * 2
      db[userId] = db[userId] + winning
      await Coinflip.send(f"You win: {winning}$!\nYour current balance is: {db[userId]}$")
      return

    else:
      await Coinflip.send("You lose, better luck next time!")
      return

  else:
    await Coinflip.send("Invalid input. Enter string like this: %cf heads/tails {bet}")
    return

@bot.command()
async def dice(Dice, choice, bet):
  #Get all userIds
  allUserIds = db.keys()
  userId = Dice.author.id

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    #Set balance to 100 if balance is = 0
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance

  if bet == 'all':
    bet = balance
  
  else:
    bet = bet

  bet = int(bet)

  if balance < bet:
    await Dice.send("Bet is too big!")
    return

  if bet <= 0	:
    await Dice.send("Please enter a valid input")
    return

  db[userId] = balance - bet
  rand_number = random.randint(1, 6)
  choice = int(choice)

  if choice == rand_number:
    winning = bet * 6
    db[userId] = db[userId] + winning
    await Dice.send(f"{rand_number} was rolled\nYou win: {winning}$!\nYour current balance is: {db[userId]}$")
    return

  else:
    await Dice.send(f"{rand_number} was rolled\nYou lose, better luck next time!")
    return

@bot.command()
async def slots(Slots, spins, bet):
  #Get all userIds
  allUserIds = db.keys()
  bet = int(bet)
  spins = int(spins)

  if bet <= 0	:
    await Slots.send("Please enter a valid input")
    return
  userId = Slots.author.id



  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance

  symbols = ["£", "€", "&", "#", "§"]
  selectedSymbols = []
  if balance < bet:
    await Slots.send("Bet is too big!")
    return
  message = await Slots.send(".")

  n = 0
  while (n < spins):
    if db[userId] < bet:
      await Slots.send("Bet is too big!")
      return

    db[userId] = db[userId] - bet

    i=0
    while (i <= 5):
      rand_number = random.randint(0, 4)
      selectedSymbols.append(symbols[rand_number])
      i += 1

    bonusNum = random.randint(1, 50)
    jackpotNum = random.randint(1, 50)

    symbol1 = selectedSymbols[0]
    symbol2 = selectedSymbols[1]
    symbol3 = selectedSymbols[2]
    symbol4 = selectedSymbols[3]
    symbol5 = selectedSymbols[4]

    winning = 0

    await message.edit(content=f"Your jackbot number is: {bonusNum}\nThe jackpot number is: ?\nThe symbols is:\n{symbol1} - {symbol2} - {symbol3} - {symbol4} - {symbol5}")

    if symbol1 == symbol2 and symbol2 == symbol3 and symbol3 == symbol4 and symbol4 == symbol5:
      winning = bet * 100
      if jackpotNum == bonusNum:
        winning += winning

      db[userId] = db[userId] + winning
      await message.edit(content=f"Your jackbot number is: {bonusNum}\nThe jackpot number is: {jackpotNum}\nThe symbols is:\n{symbol1} - {symbol2} - {symbol3} - {symbol4} - {symbol5}\nYou win: {winning}$!")
      time.sleep(3)

    elif symbol1 == symbol2 and symbol2 == symbol3 and symbol3 == symbol4:
      winning = bet * 10
      if jackpotNum == bonusNum:
        winning += winning

      db[userId] = db[userId] + winning
      await message.edit(content=f"Your jackbot number is: {bonusNum}\nThe jackpot number is: {jackpotNum}\nThe symbols is:\n{symbol1} - {symbol2} - {symbol3} - {symbol4} - {symbol5}\nYou win: {winning}$!")
      time.sleep(3)

    elif symbol1 == symbol2 and symbol2 == symbol3:
      winning = bet * 5
      if jackpotNum == bonusNum:
        winning += winning

      db[userId] = db[userId] + winning
      await message.edit(content=f"Your jackbot number is: {bonusNum}\nThe jackpot number is: {jackpotNum}\nThe symbols is:\n{symbol1} - {symbol2} - {symbol3} - {symbol4} - {symbol5}\nYou win: {winning}$!")
      time.sleep(3)

    elif symbol1 == symbol2:
      winning = bet * 2
      if jackpotNum == bonusNum:
        winning += winning

      db[userId] = db[userId] + winning
      await message.edit(content=f"Your jackbot number is: {bonusNum}\nThe jackpot number is: {jackpotNum}\nThe symbols is:\n{symbol1} - {symbol2} - {symbol3} - {symbol4} - {symbol5}\nYou win: {winning}$!")
      time.sleep(3)

    selectedSymbols.clear()
    time.sleep(0.2)
    n += 1
  
  userName = bot.get_user(userId)
  await Slots.send(f"{userName}: All spins has been completed\nYour current balance is: {db[userId]}$")
  
@bot.command(pass_context=True)
@commands.cooldown(1, 60*60*24, commands.BucketType.user)
async def daily(dailyReward):
  #Get all userIds
  allUserIds = db.keys()

  userId = dailyReward.author.id

  #Check if ID exist in db
  if allUserIds.__contains__(userId):
    #Get balance
    balance = db[userId]
    if balance <= 0:
      balance = 100
      db[userId] = balance

  #If ID doesnt exist, create new
  else:
    #Set balance
    balance = 1000
    db[userId] = balance
  
  db[userId] = balance + 100
  await dailyReward.send(f"Daily reward of 100$ claimed!\nYour current balance is: {db[userId]}$")

keep_alive.keep_alive()
bot.run(os.getenv('TOKEN'))
