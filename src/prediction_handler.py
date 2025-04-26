"""
Prediction Handler Module

This module manages user predictions for quiniela matches.
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any

class PredictionManager:
    """
    Handles saving, loading, and managing user predictions
    """
    
    def __init__(self, data_dir: str = 'data/predictions'):
        """
        Initialize PredictionManager
        
        Args:
            data_dir (str): Directory to store prediction files
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_prediction(self, pool_name: str, user_predictions: Dict[str, str]) -> str:
        """
        Save user's predictions for a specific pool
        
        Args:
            pool_name (str): Name of the pool
            user_predictions (Dict[str, str]): Predictions for matches
        
        Returns:
            str: Path to saved prediction file
        """
        # Validate predictions
        if not user_predictions:
            raise ValueError("No predictions provided")

        # Create prediction metadata
        prediction_data = {
            'pool_name': pool_name,
            'timestamp': datetime.now().isoformat(),
            'predictions': user_predictions
        }

        # Generate filename
        filename = f"{pool_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.data_dir, filename)

        # Save prediction
        with open(filepath, 'w') as f:
            json.dump(prediction_data, f, indent=4)

        return filepath

    def load_latest_prediction(self, pool_name: str) -> Dict[str, Any]:
        """
        Load the most recent prediction for a given pool
        
        Args:
            pool_name (str): Name of the pool
        
        Returns:
            Dict[str, Any]: Most recent prediction data
        """
        # Find all prediction files for the pool
        prediction_files = [
            f for f in os.listdir(self.data_dir) 
            if f.startswith(pool_name) and f.endswith('.json')
        ]

        if not prediction_files:
            raise FileNotFoundError(f"No predictions found for pool: {pool_name}")

        # Get most recent file
        latest_file = max(prediction_files, key=lambda f: 
            datetime.strptime(f.split('_')[1], '%Y%m%d'))

        # Load prediction
        filepath = os.path.join(self.data_dir, latest_file)
        with open(filepath, 'r') as f:
            prediction_data = json.load(f)

        return prediction_data

    def validate_complete_prediction(self, predictions: Dict[str, str], total_matches: int) -> bool:
        """
        Validate that all matches have been predicted
        
        Args:
            predictions (Dict[str, str]): User predictions
            total_matches (int): Total number of matches in the pool
        
        Returns:
            bool: Whether prediction is complete
        """
        return len(predictions) == total_matches