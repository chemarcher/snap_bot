import os
import discord
from urllib.parse import quote
# from dotenv import load_dotenv
import requests, time

def recorder(msgs, name, price, snapend, snapbuyers):
    name = name.replace('<', '**<')
    name = name.replace('>', '>**')
    msgs.append(name)
    msgs.append('Price: %s' %(price))
    msgs.append('#Bidders: %s' %(snapbuyers))
    msgs.append('Snap End (EDT): %s' %("{:02d}:{:02d}".format(snapend.tm_hour, snapend.tm_min)))
    msgs.append('---------')

    return msgs

# poring.world api request
url = 'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory='
req = requests.get(url)
results = req.json()
msgs = []
msgs.append("What's on poring.world now:")
for result in results:
    name, lastrec = result['name'], result['lastRecord']
    price, snapend, snapbuyers = lastrec['price'], lastrec['snapEnd'], lastrec['snapBuyers']
    price = '{:,}'.format(price)
    if snapend > time.time():
        if ('<' in name and '>' in name) or \
        ('card' in name.lower() and snapbuyers > 15) or \
        ('blueprint' in name.lower() and snapbuyers > 15) or \
        (snapbuyers > 100):
            recorder(msgs, name, price, time.localtime(snapend), snapbuyers)
msg = '\n'.join(msgs)

# dms
time.sleep(5)

url_api = 'https://poring.world/api'
matches = ['+3 monocle (broken)']
matches += ['+4 monocle (broken)']
matches += ['+3 Dragon Glow (broken)']
matches += ['+4 Dragon Glow (broken)']
matches += ['+3 Mystery Bow [1] (broken)']
matches += ['+4 Mystery Bow [1] (broken)']
matches += ['+3 Malang Snow Crab [1] (broken)']
matches += ['+4 Malang Snow Crab [1] (broken)']
matches += ['+3 Ranger Clothes (broken)']
matches += ['+4 Ranger Clothes (broken)']
msgs2 = []
for match in matches:
# url = 'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory=&q=%2B3%20monocle%20%28broken%29'
    search = 'popularity&rarity=&inStock=1&modified=&category=&endCategory=&q=' + quote(match)
    url = url_api + '/search?order=' + search
    req = requests.get(url)
    results = req.json()
    if len(results) > 0:
        for i, result in enumerate(results):
            name, lastrec = result['name'], result['lastRecord']
            price, snapend, snapbuyers = lastrec['price'], lastrec['snapEnd'], lastrec['snapBuyers']
            price = '{:,}'.format(price)
            if snapend > time.time():
                if i == 0:
                    msgs2.append("Your search on poring.world now:")
                recorder(msgs2, name, price, time.localtime(snapend), snapbuyers)
    time.sleep(5)

msg2 = '\n'.join(msgs2)

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN='Njk5MTYzNDAyMjk1MDUwMjYx.XpTGow.QhojjOnoEqc31qU2TTJ3ML2hs18'
GUILD='無雙RO團'
# GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

# @client.event
# async def on_ready():
#     # print(f'{client.user.name} has connected to Discord!')
#     print([member for guild in client.guilds for member in guild.members if 'chemarcher' in member.name])
@client.event
async def on_ready():
    # user = client.get_user(587469380372135960) # chemarcher
    # await user.send(msg)
    # channel = client.get_channel(699169724797419530) # test
    channel = client.get_channel(679428120989663245) # snap
    await channel.send(msg)
    channel = client.get_channel(699786590951571456) # archangel
    await channel.send(msg)
    channel = client.get_channel(700435689405153370) #snowland
    await channel.send(msg)
    if len(msgs2) > 0:
        user = client.get_user(587469380372135960) # chemarcher
        await user.send(msg2)
    # channel = client.get_channel(700330164881457155)
    # await channel.send(msg)
    # print([guild.channels for guild in client.guilds])
    await client.close()

client.run(TOKEN)
