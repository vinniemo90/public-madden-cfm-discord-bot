from discord import app_commands


async def week_type_auto(interaction, current):
    week_types = [{'key': 'pre-season', 'value': 'pre'}, {'key': 'regular season', 'value': 'reg'}, {'key': 'playoffs', 'value': 'reg2'}]

    return [
        app_commands.Choice(name=week_type['key'], value=week_type['value'])
        for week_type in week_types if current.lower() in week_type['key'].lower()
    ]


async def week_auto(interaction, current):
    first_choice = interaction.namespace["week_type"]
    # return list of Choice based on `first_choice`
    if first_choice == "pre":
        return [
            app_commands.Choice(name="1", value="1"),
            app_commands.Choice(name="2", value="2"),
            app_commands.Choice(name="3", value="3"),
            app_commands.Choice(name="4", value="4")
        ]
    elif first_choice == "reg":
        reg_season = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
        return [
        app_commands.Choice(name=week, value=week)
        for week in reg_season if current.lower() in week.lower()
    ]
    else:
        return [
            app_commands.Choice(name="wildcard", value="19"),
            app_commands.Choice(name="divisional", value="20"),
            app_commands.Choice(name="conference", value="21"),
            app_commands.Choice(name="super bowl", value="23")
        ]