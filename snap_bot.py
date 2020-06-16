import os, time, json
import discord
import html
from urllib.parse import quote
# from dotenv import load_dotenv
import requests 
import pandas as pd

def messenger(record_dict, csvf): # msgs, name, price, snapend, snapbuyers):
    msg = ''
    msgs = []
    if not os.path.exists(csvf):
        old_ids = []
    else:
        df = pd.read_csv(csvf)
        old_ids = df.id.values
    for id_ in record_dict.keys():
        if id_ not in old_ids:
            result_dict = record_dict[id_]
            price = result_dict['price']
            snapbuyers = result_dict['snapbuyers']
            snapend = time.localtime(result_dict['snapend'])
            name = result_dict['name']
            name = name.replace('<', '**<')
            name = name.replace('>', '>**')
            msgs.append(name)
            msgs.append('Price: %s' %(price))
            msgs.append('#Bidders: %s' %(snapbuyers))
            msgs.append('Snap End (EDT): %s' %("{:02d}:{:02d}".format(snapend.tm_hour, snapend.tm_min)))
            msgs.append('---------')
    msg = '\n'.join(msgs)

    return msg

def recorder(record_dict, csvf):
    data = [[id_, result_dict['snapend']] for id_, result_dict in record_dict.items()]
    df = pd.DataFrame(data)
    df.columns = ['id', 'snapend']
    if os.path.exists(csvf):
        df_old = pd.read_csv(csvf)
        df = pd.concat([df, df_old])
        # df = df.merge(df_old, on='id', how='outer')
        df = df.drop_duplicates(keep='first')
    df = df[df.iloc[:,1] > time.time()]
    df.to_csv(csvf, index=False)

def query():
    # poring.world api request
    rarities = [1,2,3,4,5]
    record_dict = {}
    for rarity in rarities:
        url = 'https://poring.world/api/search?order=popularity&rarity=%s&inStock=1&modified=&category=&endCategory=' %(rarity)
        req = requests.get(url)
        results = req.json()
        ids = []
        # msgs.append("What's on poring.world now:")
        for result in results:
            name, lastrec, id_ = html.unescape(result['name']), result['lastRecord'], result['id']
            price, snapend, snapbuyers = lastrec['price'], lastrec['snapEnd'], lastrec['snapBuyers']
            price = '{:,}'.format(price)
            if snapend > time.time():
                if ('<' in name and '>' in name and (('3' in name.split('<')[1] or '4' in name.split('<')[1]) or snapbuyers > 15)) or \
                ('card' in name.lower() and snapbuyers > 15) or \
                ('blueprint' in name.lower() and snapbuyers > 15) or \
                ('fenril' in name.lower()) or \
                (snapbuyers > 100) or \
                ('+12 Rosa Bracelet' in name) or \
                ('+12 Rune Boots' in name) or \
                ('Survival Ring' in name and '<' in name and '>' in name) or \
                ('+15' in name and snapbuyers > 2):
                    if name.split(' ')[0].lower() not in ['harpy', 'familiar', 'munak', 'andre'] and 'andre' not in name.lower():
                        if id_ not in ids:
                            record_dict[id_] = {'name': name, #.decode('ascii'), 
                                                'price': price,
                                                'snapend': snapend,
                                                'snapbuyers': snapbuyers}
                    # msgs = messenger(msgs, name, price, time.localtime(snapend), snapbuyers)
                    # records = recorder(records, snapend, id_)
        time.sleep(5)
        # if len(msgs) > 0:
        #     msg = '\n'.join(msgs)  
        #     df2 = pd.DataFrame(records)
        #     df2.columns = ['snapend', 'id']
        #     # print(df2)
        #     # df = df.merge(df2, on='id', how='inner')
        #     df = pd.concat([df, df2], keys=df.columns)
        #     df = df.drop_duplicates()
        #     # df = df[df2.columns]
        #     try:
        #         df = df[df['snapend'] > time.time()]
        #     except:
        #         pass
        #     # print(df)
        #     df.to_csv(frec, index=False)

# msg = query()

# # dms

    # url_api = 'https://poring.world/api'
    # matches = ['+3 Legion Plate Armor (broken)']
    # # matches = ['+3 monocle (broken)']
    # # matches += ['+4 monocle (broken)']
    # # matches += ['+3 Dragon Glow (broken)']
    # # matches += ['+4 Dragon Glow (broken)']
    # # matches += ['+3 Mystery Bow [1] (broken)']
    # # matches += ['+4 Mystery Bow [1] (broken)']
    # # matches += ['+3 Malang Snow Crab [1] (broken)']
    # # matches += ['+4 Malang Snow Crab [1] (broken)']
    # # matches += ['+3 Ranger Clothes (broken)']
    # # matches += ['+4 Ranger Clothes (broken)']
    # for match in matches:
    # # url = 'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory=&q=%2B3%20monocle%20%28broken%29'
    #     search = 'popularity&rarity=&inStock=1&modified=&category=&endCategory=&q=' + quote(match)
    #     url = url_api + '/search?order=' + search
    #     req = requests.get(url)
    #     results = req.json()
    #     if len(results) > 0:
    #         for i, result in enumerate(results):
    #             name, lastrec, id_ = result['name'].encode('utf-8').decode('utf-8'), result['lastRecord'], result['id']
    #             price, snapend, snapbuyers = lastrec['price'], lastrec['snapEnd'], lastrec['snapBuyers']
    #             price = '{:,}'.format(price)
    #             if snapend > time.time():
    #                 # if i == 0:
    #                     # msgs2.append("Your search on poring.world now:")
    #                 msgs2 = messenger(msgs2, name, price, time.localtime(snapend), snapbuyers)
    #     time.sleep(5)

    # msg2 = '\n'.join(msgs2)

    return record_dict


if __name__ == '__main__':
    # time interval between searches
    t = 5 # minutes

    # load_dotenv()
    with open('token.json', 'r') as f:
        tokens = json.load(f)
    TOKEN = tokens['bot_token']
    id_keys = ['ro', 'arch', 'snow', 'bbx', 'doppel']
    # id_keys = ['chemarcher']

    client = discord.Client()

    # @client.event
    # async def on_ready():
    #     # print(f'{client.user.name} has connected to Discord!')
    #     print([member for guild in client.guilds for member in guild.members if 'chemarcher' in member.name])
    @client.event
    async def on_ready():
        for i in range(99999999999999999999):
            t0 = time.time()
            # msg2 = ''
            try:
                record_dict = query()
            except Exception as e:
                user = client.get_user(tokens['chemarcher']) # chemarcher
                await user.send(e)
                time.sleep(10*60)
                pass
            if record_dict:
                try:
                    # write_dict(msg)
                    #user = client.get_user(587469380372135960) # chemarcher
                    #await user.send(msg)
                    for id_key in id_keys:
                        csvf = 'records_' + id_key + '.csv'
                        msg = messenger(record_dict, csvf)
                        if msg != '':
                            id_ = tokens[id_key]
                            await client.wait_until_ready()
                            channel = client.get_channel(id_)
                            await channel.send(msg)
                            recorder(record_dict, csvf)
                except Exception as e:
                    await client.wait_until_ready()
                    user = client.get_user(tokens['chemarcher']) # chemarcher
                    await user.send(e)
                    pass
            # if msg2 != '':
            #     await client.wait_until_ready()
            #     user = client.get_user(chem_id) # chemarcher
            #     await user.send(msg2)
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
