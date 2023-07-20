import os
import discord
import datetime
from discord.ext import commands

prefixes = ['заявки ', 'Заявки ', 'Заявки', 'заявки']
intents = discord.Intents.all()
intents.members = True  # If you ticked the SERVER MEMBERS INTENT

bot = commands.Bot(command_prefix=prefixes, intents=intents)  # "Import" the intents


@bot.check  # Запрет на работу в личных сообщениях
async def global_guild_only(ctx):
    if not ctx.guild:
        raise commands.NoPrivateMessage
    return True


@commands.cooldown(1, 1200, commands.BucketType.user)  # Анти-спам

@bot.command(aliases=['Подать', 'подать', ' подать', ' Подать'])                                                        # Приём заявок, основная функция
async def submit(ctx, *, arg):
    if len(ctx.message.content) > 50:                                                                                   #Сообщение меньше 50 символов не принимаются
        channel = bot.get_channel(1086492439889588276)                                                                  #Айди канала для основных сообщений("Заявка такая-то от такого-то и т.д")
        embed = discord.Embed(title="Заявка от " + str(ctx.author),
                              description=arg,
                              color=0xFF5733)
        await channel.send(embed=embed)
        # await channel.send('**Заявка от '+str(ctx.author)+'**\n'+arg)                                                 #Старый способ отправки основных сообщений. Просто текст, без эмбеда
        await ctx.reply('Заявка успешно принята')
    else:
        await ctx.reply('Заявка слишком короткая, дополни её и попробуй ещё раз')


@bot.command(aliases=['Помощь', "помощь", ' Помощь', ' помощь'])                                                        #Помощь
async def helpp(ctx):
    await ctx.reply(
        'Привет! Я бот для отправки заявок во фракции на сервере Метро:Кобальт \nДля вывода списка фракций используй команду "Заявки фракции"\nОбрати внимание, подача заявки возможна лишь раз в 20 минут\nДля подачи заявки воспользуйся шаблоном:\n>>> Заявки подать \n1. Имя персонажа \n2. Наличие микрофона \n3. Часовой пояс \n4. Фракция и отдел, в который подается заявка \n5. Текст рп заявления от лица персонажа')


@bot.command(aliases=['Фракции', 'фракции', ' Фракции', ' фракции'])                                                    #Список фракций
async def fractii(ctx):
    await ctx.reply(
        'Список фракций:\n\n**Новосибирский союз**\n   Медсанчасть\n   Вооруженные силы\n   Совет Союза\n\n**Новое Русское Государство**\n   Отдел Научных Исследований\n   Национальная армия\n   Номенклатура')


@bot.event                                                                                                              #Изменение статуса на подсказку
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Заявки помощь"))


@bot.event                                                                                                              #Сообщения об анти-спаме
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]
        await ctx.reply(f'**Ограничение приёма заявок! Новую можно будет подать через {retry_after}**')
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply('Бип-буп, буп-бип. Введи Заявки помощь, если не знаешь что делаешь')


bot.run("TOKEN")                                                                                                        #Токен дискорд-бота