"""
Quiniela Tracker Streamlit Application

Main application for tracking and predicting soccer match results using ScraperFC.
"""

pythonimport streamlit as st
import pandas as pd
import os
import sys

# Disable Botasaurus library initialization
import os
os.environ['BOTASAURUS_REQUESTS_MODULE'] = '1'

try:
    import ScraperFC as sfc
except ImportError as e:
    st.error(f"ScraperFC import error: {e}")
    st.error("Please ensure ScraperFC is installed correctly.")
    sys.exit(1)

from src.data_loader import QuinielaLoader
from src.prediction_handler import PredictionManager
from src.team_mappings import find_team_name

def match_sofascore_verification(match_df):
    """
    Verify matches using Sofascore
    """
    try:
        sofascore = sfc.Sofascore()
        
        # Add columns for Sofascore verification
        match_df['Canonical_Local'] = match_df['Local'].apply(find_team_name)
        match_df['Canonical_Visitor'] = match_df['Visitor'].apply(find_team_name)
        match_df['Sofascore_Match_Found'] = False
        match_df['Sofascore_Match_ID'] = None
        
        for index, match in match_df.iterrows():
            try:
                # Flexible league matching
                matches = sofascore.get_match_dicts(match['Date'], match['League'])
                
                # Find best match based on canonical team names
                best_match = next(
                    (m for m in matches 
                     if (match['Canonical_Local'] in m['homeTeam']['name'] or 
                         match['Canonical_Local'] in m['awayTeam']['name']) and
                        (match['Canonical_Visitor'] in m['homeTeam']['name'] or 
                         match['Canonical_Visitor'] in m['awayTeam']['name'])),
                    None
                )
                
                if best_match:
                    match_df.at[index, 'Sofascore_Match_Found'] = True
                    match_df.at[index, 'Sofascore_Match_ID'] = best_match['id']
            
            except Exception as match_error:
                st.warning(f"Could not verify match {match['Local']} vs {match['Visitor']}: {match_error}")
        
        return match_df
    
    except Exception as e:
        st.error(f"Sofascore verification failed: {e}")
        return match_df

def track_match_results(match_df):
    """
    Track match results using Sofascore
    """
    try:
        sofascore = sfc.Sofascore()
        
        # Add columns for match tracking
        match_df['Current_Score'] = None
        match_df['Match_Status'] = None
        match_df['Result'] = None
        
        for index, match in match_df.iterrows():
            if match['Sofascore_Match_Found']:
                try:
                    match_details = sofascore.get_match_dict(match['Sofascore_Match_ID'])
                    
                    # Determine match status
                    match_df.at[index, 'Match_Status'] = match_details['status']['description']
                    
                    # Get score if available
                    if 'homeScore' in match_details and 'awayScore' in match_details:
                        score = f"{match_details['homeScore']['current']}-{match_details['awayScore']['current']}"
                        match_df.at[index, 'Current_Score'] = score
                    
                    # Determine result
                    if match_details['status']['type'] == 'finished':
                        home_score = match_details['homeScore']['current']
                        away_score = match_details['awayScore']['current']
                        
                        if home_score > away_score:
                            result = 'Local Win'
                        elif home_score < away_score:
                            result = 'Visitor Win'
                        else:
                            result = 'Tie'
                        
                        match_df.at[index, 'Result'] = result
                
                except Exception as match_error:
                    st.warning(f"Could not track match {match['Local']} vs {match['Visitor']}: {match_error}")
        
        return match_df
    
    except Exception as e:
        st.error(f"Match tracking failed: {e}")
        return match_df

def main():
    # Rest of the main function remains the same
    pass

if __name__ == "__main__":
    main()