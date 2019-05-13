from discord.ext import commands
import discord
from permissions import valid_users
from settings import token, prefix
import pymysql.cursors
from secret_db import *
import datetime

# https://discordapp.com/oauth2/authorize?client_id=548004481552613378&scope=bot&permissions=76864

# Connect to database

print(f'\n----------------------------+\n[*] Starting up the bot')

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
            print('----------------------------+\n')


                # DATABASE COMMANDS


        def get_show_id(name: str) -> int:
            with self.db.cursor() as cursor:
                sql = "SELECT show_id FROM shows WHERE name = %s"
                cursor.execute(sql, (name))
                show_id = str(cursor.fetchall())
                return show_id[13:-2]


        @self.client.command(name='add',
                            description='Adds a new project to the database',
                            brief='Add a new project',
                            aliases=['new', 'create'])
        async def add(ctx, name: str, total_episodes: int):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        sql = "INSERT INTO shows (name, total_episodes) VALUES (%s, %s)"
                        cursor.execute(sql, (name, total_episodes))
                        print(f"[+] Added {name} to kaleido_db.shows")
                        sql = "SELECT show_id FROM shows"
                        cursor.execute(sql)
                        show_id = get_show_id(name)
                        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

                        add_to_status_sql = "INSERT INTO status (show_id, last_update) VALUES (%s, %s)"
                        cursor.execute(add_to_status_sql, (show_id, current_date))
                        print(f"[+] Added {name} to kaleido_db.status\n")
                        await ctx.channel.send(f'*"{name}"* ({total_episodes} episodes) has been added to the database')
                    self.db.commit()
                except Exception as e:
                    print(f"[-] Failed to add {name} to the database.\n[-] {e}\n")
                    await ctx.channel.send(f'Error adding *"{name}"* to the database.\n{e}')
            else:
                await ctx.channel.send('You do not have permission to add new projects!')


        @self.client.command(name='update',
                            description='Update the current state of a given project',
                            brief='Update current state of show',
                            aliases=['done'])
        async def update(ctx, name: str, role: str):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        show_id = int(get_show_id(name))
                        cursor.execute(f"UPDATE status SET {role} = 1 WHERE show_id = {show_id}")
                        print(f"[+] {role} for {name} has been updated\n")
                        await ctx.channel.send(f"*{name}* has been updated with {role}")
                    self.db.commit()
                except Exception as e:
                    print(f"[-] Failed to update '{name}' with '{role}' in the database.\n[-] {e}\n")
                    await ctx.channel.send(f'Error updating *{name}* in the database.\n{e}')
            else:
                await ctx.channel.send('You do not have permission to update this show!')


        @self.client.command(name='delete',
                            description='Removes a project from the database',
                            brief='Delete a project',
                            aliases=['del', 'remove'])
        async def delete(ctx, name: str):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        show_id = get_show_id(name)
                        sql = "DELETE FROM status WHERE show_id = %s"
                        cursor.execute(sql, (name))
                        print(f"[-] Removed {name} from kaleido_db.status")
                        sql = "DELETE FROM shows WHERE show_id = %s"
                        cursor.execute(sql, (name))
                        print(f"[-] Removed {name} from kaleido_db.shows\n")
                        await ctx.channel.send(f"*{name}* was removed from the database")
                    self.db.commit()
                except Exception as e:
                    print(f"[-] Failed to remove {name} from the database.\n[-] {e}\n")
                    await ctx.channel.send(f'Error removing *"{name}"* from the database.\n{e}')
            else:
                await ctx.channel.send('You do not have permission to delete a project!')


        @self.client.command(name='alt',
                            description='Adds an alternative name to a show',
                            brief='Add an alt name')
        async def alt(ctx, alt_name: str, name: str):
            if f'{str(ctx.author.id)}' in valid_users:
                try:
                    with self.db.cursor() as cursor:
                        sql = "INSERT INTO shows (alt_name) VALUES (%s) WHERE (name) = %s" % alt_name, name
                        cursor.execute(sql, (name))
                        await ctx.channel.send(f"*{alt_name}* has been added to {name}")
                    self.db.commit()
                except Exception as e:
                    print(f"[-] Failed to add {alt_name} to {name} in the database.\n[-] {e}\n")
                    await ctx.channel.send(f'Error adding *"{alt_name}"* to {name} in the database.\n{e}')
            else:
                await ctx.channel.send('You do not have permission to add alternative names!')


        @self.client.command(name='progress',
                            description='Shows the current state of a given project',
                            brief='Show progress of a show',
                            aliases=['blame'])
        async def progress(ctx, show_name: str):
            return

        @self.client.command(name='list',
                            description='Lists all projects in the database',
                            brief='List of all projects',
                            aliases=['anime', 'all'])
        async def list(ctx):
            try:
                with self.db.cursor() as cursor:
                    sql = "SELECT name FROM shows"
                    cursor.execute(sql)
                    shows = cursor.fetchall()
                    rows = ', '.join(show['name'] for show in shows)
                    await ctx.channel.send(f"{rows}")
                self.db.commit()
            except Exception as e:
                print(f"[-] Failed to print a list.\n{e}")
                await ctx.channel.send(f'Failed to print a list.\n{e}')


                # MISCELLANEOUS COMMANDS
        @self.client.command(name='kill',
                            description='Command to kill the bot, since sometimes it takes too long to respond when forcibly stopping it from the terminal.' +\
                                'You can use this to instantly kill it instead. If she lets you, that is!',
                            brief='Murder the bot',
                            aliases=['murder', 'die', 'slay', 'execute', 'cease_living'])
        async def kill(ctx):
            if f'{str(ctx.author.id)}' in valid_users:
                await ctx.channel.send(f'*{self.client.user.name} was slain by {str(ctx.author)[:-5]}*')
                print(f'\n{self.client.user.name} was terminated by {str(ctx.author)}.')
                await self.client.close()
            else:
                await ctx.channel.send(f'Nice try, {str(ctx.author)[:-5]}')


if __name__ == '__main__':
    client = Helena(token)
    client.run()
