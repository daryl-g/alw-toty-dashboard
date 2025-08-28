# Team colours and app colour palettes


def get_team_colours(
    team: str,
) -> dict | dict[str, str]:
    """
    Get the primary and secondary colours for a given A-League team.

    Args:
        team (str): The three-letter name of the A-League team, or 'all' for all teams.

    Returns:
        (dict[str, str]): A dictionary containing the primary and secondary colours.
    """
    team_colours = {
        "ADL": {"primary": "#d71920", "secondary": "#000000"},
        "BRR": {"primary": "#ff6600", "secondary": "#000000"},
        "CAN": {"primary": "#008000", "secondary": "#ffffff"},
        "CCM": {"primary": "#ffcc00", "secondary": "#0033a0"},
        "MCY": {"primary": "#6cb4ee", "secondary": "#ffffff"},
        "VIC": {"primary": "#1e3d7b", "secondary": "#ffffff"},
        "NEW": {"primary": "#0033a0", "secondary": "#ffcc00"},
        "PER": {"primary": "#5c2d91", "secondary": "#ffcc00"},
        "SYD": {"primary": "#87ceeb", "secondary": "#002f6c"},
        "WEL": {"primary": "#fdb913", "secondary": "#000000"},
        "WUN": {"primary": "#000000", "secondary": "#00ff00"},
        "WSW": {"primary": "#ff0000", "secondary": "#000000"},
    }

    # Check if team is valid
    if team not in team_colours.keys() and team != "all":
        raise ValueError(f"Invalid team name: {team}")

    if team == "all":
        return team_colours
    else:
        return team_colours.get(team, {"primary": "#808080", "secondary": "#ffffff"})
