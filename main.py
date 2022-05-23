from dotenv import load_dotenv
import os
from discord.ext import commands
import pygsheets

# Retrieving Discord token

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Authorizing service account

gc = pygsheets.authorize(service_file='creds.json')
sh = gc.open('1466 SCRUM')  # Using the service account to open the sheet

# Setting up bot

bot = commands.Bot(command_prefix='?')

# Defining the sheet and shortcut vars

shortcuts_dict = {'mech': 'Mechanical', 'elec': 'Electrical', 'b/o': 'Business/Outreach', 'web': 'Website',
                  's': 'Strategy/Scouting', 'med': 'Media'}

shortcuts = ['mech', 'elec', 'b/o', 'web', 's', 'med']

sheet_order = {'CAD': 0, 'Mechanical': 1, 'Electrical': 2, 'Code': 3, 'Business/Outreach': 4,
               'Strategy/Scouting': 5, 'Media': 6, 'Website': 7}

sheets = ['CAD', 'Mechanical', 'Electrical', 'Code', 'Business/Outreach', 'Strategy/Scouting', 'Media', 'Website']
lower_sheets = ['cad', 'mechanical', 'electrical', 'code', 'business/outreach', 'strategy/scouting', 'media', 'website']
l_u_sheet = {'cad': 'CAD', 'mechanical': 'Mechanical', 'code': 'Code', 'business/outreach': 'Business/Outreach',
             'strategy/scouting': 'Strategy/Scouting', 'media': 'Media', 'website': 'Website'}

status_order = {'TODO': 1, 'In progress': 2, 'Done': 3}
status_orders = ['TODO', 'In progress', 'Done']
status_orders_low = [val.lower() for val in status_orders]

# Commands


@bot.command(name='view_tasks', help='Views in progress, done, or TODO tasks in categories')
async def view_tasks(ctx, demand: str, category: str):
    cat = category
    if category.lower() not in lower_sheets:
        if category.lower() in shortcuts:
            cat = shortcuts_dict[category]
        else:
            await ctx.send('This category or shortcut to a category does not exist')
    if cat not in sheets:
        sheet = sh[sheet_order[l_u_sheet[cat.lower()]]]
    else:
        sheet = sh[sheet_order[cat]]
    if demand.lower() in status_orders_low:
        tasks = sheet.get_col(status_order[demand])
    elif demand.lower() == 'active':
        tasks = sheet.get_col(1)
        for val in sheet.get_col(2)[1:]:
            if val != '':
                tasks.append(val)
    else:
        await ctx.send('This status does not exist. The four statuses are ToDo, In Progress, Done, and Active (which is both todo and in progress tasks)')
    msg = ''
    for task in tasks[1:]:
        if task != '':
            msg += task
            msg += '\n'
    if msg == '':
        await ctx.send('There are no tasks in this certain category with the requested status for you to view')
    else:
        await ctx.send(msg)


@bot.command(name='change-shortcut', help="(Doesn't work yet) Changes a shortcut for an already existing category. First argument is the category, 2nd is the shortcut")
async def change_shortcut(ctx, category: str, shortcut: str):
    await ctx.send('Working on this still.')


@bot.command(name='display-shortcuts', help="Displays every shortcut for categories (Mechanical, Code, etc.)")
async def display_shortcuts(ctx):
    msg = ''
    for shortcut in shortcuts:
        msg += shortcut
        msg += ': '
        msg += shortcuts_dict[shortcut]
        msg += '\n'
    await ctx.send(msg)


# Error correction code so bot doesn't hard crash


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for your command")

# Runs the bot

bot.run(TOKEN)
