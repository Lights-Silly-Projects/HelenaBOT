import discord
from discord.ext import commands
from settings import token, prefix
import fgo
from permissions import valid_users
import random

# https://discordapp.com/oauth2/authorize?client_id=548004481552613378&scope=bot&permissions=76864

client = commands.Bot(command_prefix=prefix)

no_permission = 'You do not have permission to use this command!'

@client.event
async def on_ready():
    print(f'{client.user.name} is now running.')

@client.command()
async def kill(ctx):
    if f'{str(ctx.author)}' in valid_users:
        await ctx.channel.send(f'{client.user.name} is now shutting down.')
        await client.close()
    else:
        await ctx.channel.send(no_permission)


@client.command()
async def fgo_damagecalculator(ctx, servant=None, NP=1, buffed="Max", class_bonus=True, random=True, grailed=False):
    """
    NP Damage calculator for Fate/Grand Order. 
    By default it assumes max fous and max level.
    Only accepts Servant IDs, and only NA Servants (for now).

    "NP" indicates Noble Phantasm level, 
    "Random" adds/removes the random modifier 
    "class bonus" assumes advantage.
    "grailed" assumes max Grailed (lvl 100).

    There are three modes for "buffed":
        None    - Assume no active skills are active
        Medium  - Assume lvl 6  active skills are active
        Max     - Assume lvl 10 active skills are active 

    Original calculation:
    [servantAtk * npDamageMultiplier * (firstCardBonus + (cardDamageValue * (1 + cardMod))) * classAtkBonus * triangleModifier * 
    attributeModifier * randomModifier * 0.23 * (1 + atkMod - defMod) * criticalModifier * extraCardModifier * (1 - specialDefMod) 
    * {1 + powerMod + selfDamageMod + (critDamageMod * isCrit) + (npDamageMod * isNP)} * {1 + ((superEffectiveModifier - 1) * 
    isSuperEffective)}] + dmgPlusAdd + selfDmgCutAdd + (servantAtk * busterChainMod)

    Due to the nature of this calculator, some parts are removed. For simplification, attributes and Super Effective are also ignored.

    """
    if servant == None:
        await ctx.channel.send('This command requires a servant id! For a list of servants, type "!fgo_servants"')
    elif servant in fgo.servants:
            with open(f'servants/{servant}.txt') as f:
                stats = f.read().splitlines()
                print(stats)

                fgo.calc_dmg(name, atk, maxAtk, atkMod, defMod, cardMod, npDamageMod, atkModLow, defModLow, cardModLow, npDamageModLow, atkModMax, defModMax, cardModMax, npDamageModMax)
    else:
        await ctx.channel.send('This is not a valid servant id! For a list of servants, type "!fgo_servants"')

      

client.run(token)
