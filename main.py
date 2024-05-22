import logging
import os

import discord
import firebase_admin
from discord import app_commands
from dotenv import load_dotenv
from firebase_admin import credentials, db

import cfm_rosters
import cfm_schedule
import cfm_standings
import cfm_team
import cfm_users
import discord_autocomplete

load_dotenv()

firebase_creds = {
  "type": os.getenv('TYPE'),
  "project_id": os.getenv('PROJECT_ID'),
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
  "client_email": os.getenv('CLIENT_EMAIL'),
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": os.getenv('AUTH_URI'),
  "token_uri": os.getenv('TOKEN_URI'),
  "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER'),
  "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL'),
}

cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred, {
    'databaseURL' : os.getenv('DATABASE_URL')
})

# Root db reference
cfm = db.reference()

intents = discord.Intents.default()
print(intents)
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    # tree.clear_commands(guild=discord.Object(id=""))
    await tree.sync()
    print(f'We have logged in as {client.user}')

async def teams_auto(interaction, current):
    team_snapshot = cfm.child('teams').get()
    teams = [ {'key': f"{team.get('cityName')} {team.get('displayName')}", 'value': team.get('displayName')} for id, team in team_snapshot.items() ]

    return [
        app_commands.Choice(name=team['key'], value=team['value'])
        for team in teams if current.lower() in team['key'].lower()
    ]

############### TEAM COMMANDS START ###############

@tree.command(name= "team", description= "Get team info")
@app_commands.autocomplete(team=teams_auto)
@app_commands.describe(team="The team to get info for")
async def teams(interaction: discord.Interaction, team: str):
    response = cfm_team.get_team_info(cfm, team)
    await interaction.response.send_message(response)

@tree.command(name= "stats", description= "Get season stats")
@app_commands.describe(team="The team to get stats for")
@app_commands.autocomplete(team=teams_auto)
async def teams(interaction: discord.Interaction, team: str):
    response = cfm_team.get_team_season_stats(cfm, team)
    await interaction.response.send_message(response)

@tree.command(name= "record", description= "Get season record")
@app_commands.describe(team="The team to get record for")
@app_commands.autocomplete(team=teams_auto)
async def teams(interaction: discord.Interaction, team: str):
    response = cfm_team.get_team_record(cfm, team)
    await interaction.response.send_message(response)

@tree.command(name= "cap", description= "Get team cap")
@app_commands.describe(team="The team to get cap info for")
@app_commands.autocomplete(team=teams_auto)
async def teams(interaction: discord.Interaction, team: str):
    response = cfm_team.get_team_cap(cfm, team)
    await interaction.response.send_message(response)

@tree.command(name= "injuries", description= "Get team injury report")
@app_commands.describe(team="The team to get injuries for")
@app_commands.autocomplete(team=teams_auto)
async def teams(interaction: discord.Interaction, team: str):
    response = cfm_team.get_injured_players(cfm, team)
    await interaction.response.send_message(response)

@tree.command(name= "resign", description= "Get players with expiring contracts")
@app_commands.describe(team="The team to get expiring contracts for")
@app_commands.autocomplete(team=teams_auto)
async def teams(interaction: discord.Interaction, team: str):
    response = cfm_team.get_expiring_contracts(cfm, team)
    await interaction.response.send_message(response)


############### STANDINGS COMMANDS START ###############
@tree.command(name= "conf-standings", description= "Get conference standings")
@app_commands.describe(conference="Conference to get standings for")
@app_commands.choices(conference=[
        app_commands.Choice(name="AFC", value="afc"),
        app_commands.Choice(name="NFC", value="nfc"),
        ])
async def teams(interaction: discord.Interaction, conference: app_commands.Choice[str]):
    response = cfm_standings.get_conf_standings(cfm, conference.value)
    await interaction.response.send_message(response)

@tree.command(name= "nfl-standings", description= "Get nfl standings")
async def teams(interaction: discord.Interaction):
    response = cfm_standings.get_nfl_standings(cfm)
    await interaction.response.send_message(response)


############### SCHEDULE COMMANDS START ###############
@tree.command(name= "weekly-schedule", description= "Get user vs. user games")
@app_commands.autocomplete(week_type=discord_autocomplete.week_type_auto, week=discord_autocomplete.week_auto)
async def teams(interaction: discord.Interaction, week_type: str, week: str):
    response = cfm_schedule.get_weekly_schedule(cfm, week_type, week)
    await interaction.response.send_message(response)


@tree.command(name= "weekly-stats", description= "Get top performers for the week")
@app_commands.autocomplete(week_type=discord_autocomplete.week_type_auto, week=discord_autocomplete.week_auto)
async def teams(interaction: discord.Interaction, week_type: str, week: str):
    response = cfm_schedule.get_weekly_top_performers(cfm, week_type, week)
    await interaction.response.send_message(response)


@tree.command(name= "team-schedule", description= "Get team schedule")
@app_commands.describe(team="Team to get schedule for", week_type="pre-season or regular season")
@app_commands.choices(week_type=[
        app_commands.Choice(name="pre-season", value="pre"),
        app_commands.Choice(name="regular season", value="reg"),
        ])
async def teams(interaction: discord.Interaction, team: str, week_type: app_commands.Choice[str]):
    response = cfm_schedule.get_season_schedule(cfm, team, week_type.value)
    await interaction.response.send_message(response)


@tree.command(name= "scores", description= "Get user vs. user scores")
@app_commands.autocomplete(week_type=discord_autocomplete.week_type_auto, week=discord_autocomplete.week_auto)
async def teams(interaction: discord.Interaction, week_type: str, week: str):
    response = cfm_schedule.get_user_weekly_scores(cfm, week_type, week)
    await interaction.response.send_message(response)

# @tree.command(name= "open-teams", description= "Get available teams", guild=discord.Object(id=""))
@tree.command(name= "open-teams", description= "Get available teams")
async def teams(interaction: discord.Interaction):
    response = cfm_team.get_available_teams(cfm)
    await interaction.response.send_message(response)


############### ROSTER COMMANDS START ###############
# @tree.command(name= "scores", description= "Get user vs. user scores", guild=discord.Object(id=""))
# @app_commands.describe(week_type="pre or reg", week="Week number")
# async def teams(interaction: discord.Interaction, week_type: str, week: str):
#     response = cfm_schedule.get_user_weekly_scores(cfm, week_type, week)
#     await interaction.response.send_message(response)



############### USER COMMANDS START ###############
@tree.command(name= "gamertag", description= "Attach gamertag to a username")
@app_commands.describe(member="User to assign gamertag to", gamertag="The gamertag used in this league")
async def teams(interaction: discord.Interaction, member: discord.Member, gamertag: str):
    response = cfm_users.update_gamertag(cfm, member.id, gamertag)
    await interaction.response.send_message(response)


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

client.run(os.getenv('DISCORD_TOKEN'), log_level=os.getenv('LOG_LEVEL'))