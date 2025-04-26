"""
Team Name Mapping Database

Provides consistent team name mappings across different leagues and sources.
"""

TEAM_MAPPINGS = {
    # Liga MX
    'Liga MX': {
        'Monterrey': ['Rayados', 'CF Monterrey', 'MONTERREY'],
        'América': ['Club América', 'America', 'AMERICA'],
        'Pachuca': ['Tuzos', 'Club Pachuca', 'PACHUCA'],
        'Guadalajara': ['Chivas', 'Club Deportivo Guadalajara', 'CHIVAS'],
        'Cruz Azul': ['Cruz Azul FC', 'CRUZ AZUL'],
        'Tigres UANL': ['Tigres', 'UANL', 'TIGRES'],
        'Santos': ['Santos Laguna', 'SANTOS'],
        'León': ['Club León', 'LEON'],
        'Toluca': ['Diablos Rojos', 'Toluca FC', 'TOLUCA'],
        'Puebla': ['Club Puebla', 'PUEBLA']
    },
    
    # Liga Expansion MX
    'Liga Expansion MX': {
        'Atlético San Luis': ['San Luis', 'SAN LUIS'],
        'Tampico Madero': ['Tampico', 'TAMPICO'],
        'Cancún FC': ['Cancun', 'CANCUN']
    },
    
    # Liga Femenil MX
    'Liga Femenil MX': {
        'Tigres Femenil': ['Tigres UANL Femenil', 'TIGRES FEMENIL'],
        'América Femenil': ['Club América Femenil', 'AMERICA FEMENIL'],
        'Guadalajara Femenil': ['Chivas Femenil', 'CHIVAS FEMENIL']
    },
    
    # La Liga (Spain)
    'La Liga': {
        'Real Madrid': ['Madrid', 'Real', 'REAL MADRID'],
        'Barcelona': ['Barça', 'Barca', 'FC Barcelona', 'BARCELONA'],
        'Atlético Madrid': ['Atletico', 'Atleti', 'ATLETICO MADRID'],
        'Sevilla': ['Sevilla FC', 'SEVILLA']
    },
    
    # Other Leagues (partial list for brevity)
    'Premier League': {
        'Manchester City': ['Man City', 'City', 'MANCHESTER CITY'],
        'Manchester United': ['Man Utd', 'United', 'MANCHESTER UNITED'],
        'Liverpool': ['LFC', 'LIVERPOOL'],
        'Arsenal': ['ARSENAL']
    },
    
    # Brasileirão
    'Brasileirão': {
        'Flamengo': ['Mengão', 'FLAMENGO'],
        'Palmeiras': ['Verdão', 'PALMEIRAS'],
        'São Paulo': ['SPFC', 'SAO PAULO'],
        'Corinthians': ['CORINTHIANS']
    }
}

def find_team_name(team_name: str, league: str = None) -> str:
    """
    Find the canonical team name across different variations
    
    Args:
        team_name (str): Team name to match
        league (str, optional): Specific league to search
    
    Returns:
        str: Canonical team name or original input if no match found
    """
    # Normalize input
    normalized_name = team_name.strip().upper()
    
    # If league is specified, search that league first
    if league and league in TEAM_MAPPINGS:
        for canonical_name, variations in TEAM_MAPPINGS[league].items():
            if normalized_name in [v.upper() for v in variations] or \
               normalized_name == canonical_name.upper():
                return canonical_name
    
    # Search across all leagues if no league specified or no match found
    for league_teams in TEAM_MAPPINGS.values():
        for canonical_name, variations in league_teams.items():
            if normalized_name in [v.upper() for v in variations] or \
               normalized_name == canonical_name.upper():
                return canonical_name
    
    # Return original name if no match found
    return team_name