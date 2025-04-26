"""
Quiniela Data Loader Module

This module handles loading and processing quiniela match data from CSV files.
"""

import os
import pandas as pd
from typing import List, Dict
from src.team_mappings import find_team_name

class QuinielaLoader:
    """
    Handles loading and processing of quiniela match data
    """
    
    def __init__(self, data_dir: str = 'data/pools'):
        """
        Initialize the QuinielaLoader
        
        Args:
            data_dir (str): Directory to store and load pool data
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def load_weekly_pool(self, file_path: str) -> pd.DataFrame:
        """
        Load quiniela pool from CSV file
        
        Args:
            file_path (str): Path to the CSV file
        
        Returns:
            pd.DataFrame: Processed dataframe of matches
        """
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read CSV
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")

        # Required columns validation
        required_columns = ['Local', 'Visitor', 'Date', 'Time', 'League']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Normalize team names
        df['Canonical_Local'] = df['Local'].apply(find_team_name)
        df['Canonical_Visitor'] = df['Visitor'].apply(find_team_name)

        # Generate unique match ID
        df['Match_ID'] = df.apply(
            lambda row: f"{row['Canonical_Local']}_{row['Canonical_Visitor']}_{row['Date']}_{row['Time']}", 
            axis=1
        )

        # Add status column
        df['Status'] = 'Pending'

        return df

    def save_pool(self, df: pd.DataFrame, pool_name: str):
        """
        Save pool data to a file
        
        Args:
            df (pd.DataFrame): Dataframe to save
            pool_name (str): Name of the pool
        """
        filename = f"{pool_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        df.to_csv(filepath, index=False)
        return filepath