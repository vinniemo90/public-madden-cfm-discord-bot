UNEXPECTED_ERR_MSG = 'Sorry, an error occurred processing your request.'
MISSING_TEAM_NAME_ERR_MSG = ("Sorry, I couldn't find a team name associated with your request."
                                " Use '/help' to get a list of commands.")
MISSING_WK_NUM_ERR_MSG = ("Sorry, I couldn't find a week associated with your request."
                            " Use '/help' to get a list of commands.")
MISSING_GAMERTAG_ERR_MSG = "Sorry, I couldn't find the gamertag provided. Please double check spellng or export the latest data from companion app before trying again."
GAMERTAG_SUCCESS_MESSAGE = 'Successfully associated gamertag with discord user.'
USER_GAME_ERROR = 'Sorry, an error occurred retrieving user games.'
TOP_PERFORMERS_ERROR = 'Sorry, an error occurred retrieving top performers.'
INVALID_WEEK_TYPE_ERR_MSG = 'Invalid week type. Only __pre__ or __reg__ are accepted.'
WEEK_TYPE_MAP = {
    'pre': 'pre-season',
    'reg': 'regular season',
    'reg2': 'playoffs'
}
PLAYOFS_MAP = {
    '19': 'wildcard',
    '20': 'divisional',
    '21': 'conference',
    '22': 'super bowl'
}
TP_STATS_CATEGORIES = ['passing', 'rushing', 'receiving', 'defense']