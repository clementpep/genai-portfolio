"""
Portfolio data loading module.

This module handles loading and caching of portfolio data from the YAML configuration file.
"""

import yaml
from typing import Dict
from config.settings import PORTFOLIO_DATA_PATH


class PortfolioDataLoader:
    """
    Singleton class to load and cache portfolio data.
    """

    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> Dict:
        """
        Load portfolio data from YAML file. Uses caching to avoid repeated file reads.

        Returns:
            Dict: Portfolio configuration including experiences, skills, certifications, education

        Raises:
            FileNotFoundError: If the portfolio data file doesn't exist
            yaml.YAMLError: If the YAML file is malformed
        """
        if self._data is None:
            try:
                with open(PORTFOLIO_DATA_PATH, "r", encoding="utf-8") as f:
                    self._data = yaml.safe_load(f)
                print(f"Portfolio data loaded successfully from {PORTFOLIO_DATA_PATH}")
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Portfolio data file not found at {PORTFOLIO_DATA_PATH}"
                )
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Error parsing portfolio YAML file: {e}")

        return self._data

    def get_experiences(self) -> list:
        """Get all professional experiences."""
        return self.load().get("experiences", [])

    def get_skills(self) -> list:
        """Get all skill categories."""
        return self.load().get("skills", [])

    def get_certifications(self) -> list:
        """Get all certifications."""
        return self.load().get("certifications", [])

    def get_education(self) -> list:
        """Get educational background."""
        return self.load().get("education", [])


# Create a global instance for easy access
portfolio_loader = PortfolioDataLoader()
