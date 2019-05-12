from discord.ext import commands
import discord
from permissions import valid_users
from settings import token, prefix
import pymysql.cursors
from secret_db import *

# https://discordapp.com/oauth2/authorize?client_id=548004481552613378&scope=bot&permissions=76864

# Connect to database

print(f'\n------------------------\n[*] Starting up the bot')

def connect_db():
    connection = pymysql.connect(host=DB_HOST,
                                user=DB_USER,
                                password=DB_PASS,
                                db=DB_NAME,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    print(f'[*] Connected to {DB_NAME}')
    return connection

class Helena:
    def __init__(self, token):
        self.db = connect_db()
        self.client = commands.Bot(command_prefix=prefix)
        self.token = token
        self.prepare_client()

    def run(self):
        self.client.run(self.token)

    def prepare_client(self):
        no_permission = 'You do not have permission to use this command!'


        @self.client.event
        async def on_ready():
            await self.client.change_presence(activity = discord.Game(name="with the Mahatma"))
            print(f'[*] {self.client.user.name} is now running')
            print('------------------------\n')


        """
            Add a new show to the database
        """
        @self.client.command(name='add',
                            description='Adds a new project to the database',
                            brief='Add a new project',
                            aliases=['new', 'create'])
        async def add(ctx, name, total_episodes):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        sql = "INSERT INTO shows (name, total_episodes) VALUES (%s, %s)"
                        cursor.execute(sql, (name, total_episodes))
                        await ctx.channel.send(f"*{name}* ({total_episodes} episodes) has been added to the database")
                    self.db.commit()
                except:
                    await ctx.channel.send(f"Failed to add {name} to the database")
            else:
                await ctx.channel.send('You do not have permission to add new projects!')


        """
            Delete a show from the database
        """
        @self.client.command(name='delete',
                            description='Removes a project from the database',
                            brief='Delete a project',
                            aliases=['del', 'remove'])
        async def delete(ctx, name):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        sql = "DELETE FROM shows WHERE name = %s"
                        cursor.execute(sql, (name))
                        await ctx.channel.send(f"*{name}* was removed from the database")
                    self.db.commit()
                except:
                    await ctx.channel.send(f"Failed to remove {name} from the database")
            else:
                await ctx.channel.send('You do not have permission to delete a project!')

        """
            Add an alternative name to a show
        """
        @self.client.command(name='alt',
                            description='Adds an alternative name to a show',
                            brief='Add an alt name')
        async def alt(ctx, alt_name, name):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        sql = "INSERT INTO shows (alt_name) VALUES (%s) WHERE (name) = %s"
                        cursor.execute(sql, (name))
                        await ctx.channel.send(f"*{alt_name}* has been added to {name}")
                    self.db.commit()
                except:
                    await ctx.channel.send(f"Failed to add {alt_name} to the database")
            else:
                await ctx.channel.send('You do not have permission to add alternative names!')


        """
            Update a project
        """
        # @self.client.command(name='update',
        #                     description='Update the current state of a given project',
        #                     brief='Update current state of show',
        #                     aliases=['done'])
        # async def update(ctx, role, name):
        #     if f'{str(ctx.author.id)}' in valid_users:
        #         try:
        #             with self.db.cursor() as cursor:
        #                 sql = "UPDATE status SET %s = 1 WHERE show_id = %s" # This won't work unless I can get it to grab the `show_id` from `shows` first
        #                 cursor.execute(sql, (name))
        #                 await ctx.channel.send(f"*{alt_name}* has been added to {name}")
        #             self.db.commit()
        #         except:
        #             await ctx.channel.send(f"{name} has been updated!")
        #     else:
        #         await ctx.channel.send('You do not have permission to update this show!')
        # # TO-DO: !update [show name] [role]
        # # Updates the state of a certain project


        """
            Lists all projects
        """
        # @self.client.command(name='list',
        #                     description='Lists all projects in the database',
        #                     brief='List of all projects')
        # async def list(ctx):
        #     try:
        #         with self.db.cursor() as cursor:
        #             sql = "SELECT * FROM shows"
        #             cursor.execute(sql)

        #             rows = cursor.fetchall()
        #             for row in rows:
        #                 await ctx.channel.send(f"{row[1]}")
        #         self.db.commit()
        #     except:
        #         await ctx.channel.send("Could not print a list")


        """
            Kill switch
        """
        @self.client.command(name='kill',
                            description='Command to kill the bot, since it sometimes takes a long time to respond when forcibly stopping it from the terminal.' +\
                                'You can use this to instantly kill it instead. If she lets you, that is!',
                            brief='Murder the bot',
                            aliases=['murder', 'die', 'slay', 'execute', 'cease_living'])
        async def kill(ctx):
            if f'{str(ctx.author.id)}' in valid_users:
                await ctx.channel.send(f'*{self.client.user.name} was slain by {str(ctx.author)[:-5]}*')
                print(f'\n{self.client.user.name} was terminated by {str(ctx.author)}.')
                await self.client.close()
            else:
                await ctx.channel.send('Nice try, buddy')


        # Kaleido project status commands

        """
            Check current progress on a given project
        """
        @self.client.command(name='progress',
                            description='Shows the current state of a given project',
                            brief='Show progress of a show',
                            aliases=['blame'])
        async def progress(show_name):
            # Note: make sure that if it returns multiple names, the user can choose one of them
            return

        """
            Update the progress of a given project
        """
        @self.client.command(name='update',
                            description='Update the current state of a given project',
                            brief='Update current state of show',
                            aliases=['done'])
        async def update(show_name, role):
            return
        # TO-DO: !update [show name] [role]
        # Updates the state of a certain project




if __name__ == '__main__':
    client = Helena(token)
    client.run()
