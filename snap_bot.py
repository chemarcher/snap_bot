import os, time, json
import discord
from urllib.parse import quote
# from dotenv import load_dotenv
import requests 
import pandas as pd

def messenger(msgs, name, price, snapend, snapbuyers):
    name = name.replace('<', '**<')
    name = name.replace('>', '>**')
    msgs.append(name)
    msgs.append('Price: %s' %(price))
    msgs.append('#Bidders: %s' %(snapbuyers))
    msgs.append('Snap End (EDT): %s' %("{:02d}:{:02d}".format(snapend.tm_hour, snapend.tm_min)))
    msgs.append('---------')

    return msgs

def recorder(records, snapend, id_):
    records.append([snapend, id_])

    return records

def query():
    frec = 'records.csv'
    df = pd.read_csv(frec)
    # poring.world api request
    url = 'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory='
    req = requests.get(url)
    results = req.json()
    records = []
    msg = ''
    msg2 = ''
    msgs = []
    msgs2 = []
    # msgs.append("What's on poring.world now:")
    for result in results:
        name, lastrec, id_ = str(result['name'].encode('utf-8')), result['lastRecord'], result['id']
        price, snapend, snapbuyers = lastrec['price'], lastrec['snapEnd'], lastrec['snapBuyers']
        price = '{:,}'.format(price)
        if snapend > time.time() and (id_ not in df['id'].values.tolist()):
            if ('<' in name and '>' in name ) or \
            ('card' in name.lower() and snapbuyers > 15) or \
            ('blueprint' in name.lower() and snapbuyers > 15) or \
            (snapbuyers > 100) or \
            ('fenril' in name.lower()):
                msgs = messenger(msgs, name, price, time.localtime(snapend), snapbuyers)
                records = recorder(records, snapend, id_)
    if len(msgs) > 0:
        msg = '\n'.join(msgs)  
        df2 = pd.DataFrame(records)
        df2.columns = ['snapend', 'id']
        # print(df2)
        # df = df.merge(df2, on='id', how='inner')
        df = pd.concat([df, df2], keys=df.columns)
        df = df.drop_duplicates()
        # df = df[df2.columns]
        try:
            df = df[df['snapend'] > time.time()]
        except:
            pass
        # print(df)
        df.to_csv(frec, index=False)

# msg = query()

# # dms
    time.sleep(30)

    url_api = 'https://poring.world/api'
    matches = ['+3 Legion Plate Armor (broken)']
    # matches = ['+3 monocle (broken)']
    # matches += ['+4 monocle (broken)']
    # matches += ['+3 Dragon Glow (broken)']
    # matches += ['+4 Dragon Glow (broken)']
    # matches += ['+3 Mystery Bow [1] (broken)']
    # matches += ['+4 Mystery Bow [1] (broken)']
    # matches += ['+3 Malang Snow Crab [1] (broken)']
    # matches += ['+4 Malang Snow Crab [1] (broken)']
    # matches += ['+3 Ranger Clothes (broken)']
    # matches += ['+4 Ranger Clothes (broken)']
    for match in matches:
    # url = 'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory=&q=%2B3%20monocle%20%28broken%29'
        search = 'popularity&rarity=&inStock=1&modified=&category=&endCategory=&q=' + quote(match)
        url = url_api + '/search?order=' + search
        req = requests.get(url)
        results = req.json()
        if len(results) > 0:
            for i, result in enumerate(results):
                name, lastrec, id_ = result['name'].encode('utf-8').decode('utf-8'), result['lastRecord'], result['id']
                price, snapend, snapbuyers = lastrec['price'], lastrec['snapEnd'], lastrec['snapBuyers']
                price = '{:,}'.format(price)
                if snapend > time.time():
                    # if i == 0:
                        # msgs2.append("Your search on poring.world now:")
                    msgs2 = messenger(msgs2, name, price, time.localtime(snapend), snapbuyers)
        time.sleep(5)

    msg2 = '\n'.join(msgs2)

    return msg, msg2


if __name__ == '__main__':
    # time interval between searches
    t = 5 # minutes

    # load_dotenv()
    with open('token.json', 'r') as f:
        tokens = json.load(f)
    TOKEN = tokens['bot_token']
    ro_id = tokens['ro']
    arch_id = tokens['arch']
    snow_id = tokens['snow']
    bbx_id = tokens['bbx']
    doppel_id = tokens['doppel']
    chem_id = tokens['chemarcher']
    # GUILD = tokens['guild_name']
    # print(GUILD)

    client = discord.Client()

    # @client.event
    # async def on_ready():
    #     # print(f'{client.user.name} has connected to Discord!')
    #     print([member for guild in client.guilds for member in guild.members if 'chemarcher' in member.name])
    @client.event
    async def on_ready():
        for i in range(999999999999999999):
            t0 = time.time()
            msg = ''
            msg2 = ''
            try:
                msg, msg2 = query()
            except Exception as e:
                user = client.get_user(chem_id) # chemarcher
                await user.send(e)
                time.sleep(10*60)
                pass
            sent = False
            if msg != '':
                try:
                    # write_dict(msg)
                    #user = client.get_user(587469380372135960) # chemarcher
                    #await user.send(msg)
                    await client.wait_until_ready()
                    channel = client.get_channel(ro_id) # snap
                    await channel.send(msg)
                    await client.wait_until_ready()
                    channel = client.get_channel(arch_id) # archangel
                    await channel.send(msg)
                    await client.wait_until_ready()
                    channel = client.get_channel(snow_id) #snowland
                    await channel.send(msg)
                    await client.wait_until_ready()
                    channel = client.get_channel(bbx_id) #bbx
                    await channel.send(msg)
                    await client.wait_until_ready()
                    channel = client.get_channel(doppel_id) #vendoppel
                    await channel.send(msg)
                except Exception as e:
                    await client.wait_until_ready()
                    user = client.get_user(chem_id) # chemarcher
                    await user.send(e)
                    pass
            if msg2 != '':
                await client.wait_until_ready()
                user = client.get_user(chem_id) # chemarcher
                await user.send(msg2)
            # channel = client.get_channel(700330164881457155)
            # await channel.send(msg)
            # print([guild.channels for guild in client.guilds])
            # await client.close()
            t1 = time.time()
            dt = t * 60 - (t1 - t0)
            time.sleep(dt)
            # print('%s / %s finished.' %(i+1, 999999999))
        await client.close()

    client.run(TOKEN)
