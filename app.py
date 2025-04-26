"""
Quiniela Tracker Streamlit Application

Main application for tracking and predicting soccer match results using ScraperFC.
"""

import streamlit as st
import pandas as pd
import os
from src.data_loader import QuinielaLoader
from src.prediction_handler import PredictionManager
from src.team_mappings import find_team_name
import ScraperFC as sfc  # Import ScraperFC

def match_sofascore_verification(match_df):
    """
    Verify matches using Sofascore
    
    Args:
        match_df (pd.DataFrame): Dataframe of matches
    
    Returns:
        pd.DataFrame: Updated dataframe with Sofascore match information
    """
    sofascore = sfc.Sofascore()
    
    # Add columns for Sofascore verification
    match_df['Canonical_Local'] = match_df['Local'].apply(find_team_name)
    match_df['Canonical_Visitor'] = match_df['Visitor'].apply(find_team_name)
    match_df['Sofascore_Match_Found'] = False
    match_df['Sofascore_Match_ID'] = None
    
    for index, match in match_df.iterrows():
        try:
            # Search for matching matches in Sofascore
            # Note: You might need to add a league parameter based on your specific use case
            matches = sofascore.get_match_dicts(match['Date'], 'Liga MX')  # Adjust league as needed
            
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
        
        except Exception as e:
            st.warning(f"Could not verify match {match['Local']} vs {match['Visitor']}: {e}")
    
    return match_df

def track_match_results(match_df):
    """
    Track match results using Sofascore
    
    Args:
        match_df (pd.DataFrame): Dataframe of matches with Sofascore IDs
    
    Returns:
        pd.DataFrame: Updated dataframe with match results
    """
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
            
            except Exception as e:
                st.warning(f"Could not track match {match['Local']} vs {match['Visitor']}: {e}")
    
    return match_df

def main():
    st.title("Quiniela Tracker")

    # Sidebar for navigation
    menu = ["Upload Pool", "Make Predictions", "View Results"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Initialize managers
    loader = QuinielaLoader()
    prediction_manager = PredictionManager()

    if choice == "Upload Pool":
        st.subheader("Upload Weekly Quiniela Pool")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            # Temporarily save uploaded file
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Load and display pool data
                pool_df = loader.load_weekly_pool(temp_path)
                st.dataframe(pool_df)
                
                # Option to save pool
                if st.button("Save This Pool"):
                    saved_path = loader.save_pool(pool_df, "Weekly Quiniela")
                    st.success(f"Pool saved to {saved_path}")
                
                # Sofascore verification button
                if st.button("Verify Matches on Sofascore"):
                    verified_pool = match_sofascore_verification(pool_df)
                    st.dataframe(verified_pool)
            
            except Exception as e:
                st.error(f"Error processing file: {e}")

    elif choice == "Make Predictions":
        # (Previous implementation remains the same)
        pass

    elif choice == "View Results":
        st.subheader("Quiniela Results")
        
        # Load available pools
        pool_files = [f for f in os.listdir('data/pools') if f.endswith('.csv')]
        
        if pool_files:
            selected_pool = st.selectbox("Select Pool", pool_files)
            pool_path = os.path.join('data/pools', selected_pool)
            pool_df = pd.read_csv(pool_path)
            
            if st.button("Track Match Results"):
                results_df = track_match_results(pool_df)
                st.dataframe(results_df)
        else:
            st.warning("No pools available.")

if __name__ == "__main__":
    main()