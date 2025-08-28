# Utility functions

# Imports
import pandas as pd


def shorten_team_name(name: str) -> str:
    """
    Get the three-letter abbreviation from FBRef's A-League team name.

    Args:
        name (str): Opta/FBRef's name of the A-League team.

    Returns:
        (str): The three-letter abbreviation of the team.
    """
    team_name_map = {
        "Adelaide Utd": "ADL",
        "Brisbane Roar": "BRR",
        "Canberra Utd": "CAN",
        "Central Coast Mariners": "CCM",
        "Melb City": "MCY",
        "Melb Victory": "VIC",
        "Newcastle Jets": "NEW",
        "Perth Glory": "PER",
        "Sydney FC": "SYD",
        "Wellington Phoenix": "WEL",
        "Western United": "WUN",
        "W Sydney": "WSW",
    }

    return team_name_map.get(name, name)
