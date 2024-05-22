import constants


def update_gamertag(db_root, user_id, gamertag) -> str:
    print(f"Setting gamertag for {user_id}")

    try:
        teams_snapshot = db_root.child('teams').get()
        discord_members_ref = db_root.child('discordMembers')

        print('Find user teams')
        username = [ team['userName'] for team_id, team in teams_snapshot.items() if team['userName'].lower() == gamertag.lower()]

        if username:
            discord_members_ref.update({username[0]: user_id})
            return f'Successfully associated {gamertag} with discord user.'
        
        else:
            return f"Sorry, I couldn't find the gamertag {gamertag}. Please double check spellng or export the latest data from companion app before trying again."

    except Exception as e:
        print(e)
        return constants.UNEXPECTED_ERR_MSG
