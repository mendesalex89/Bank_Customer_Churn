"""
Module for creating visualizations for exploratory data analysis.
"""
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET


class EDAVisualizer:
    """Class for creating EDA visualizations."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the visualizer with a dataset.
        
        Args:
            df (pd.DataFrame): Input dataset
        """
        self.df = df
        self.setup_style()
    
    @staticmethod
    def setup_style():
        """Set up the plotting style."""
        plt.style.use('seaborn')
        sns.set_palette('Set2')
    
    def plot_target_distribution(self, figsize: tuple = (10, 6)) -> None:
        """
        Plot the distribution of the target variable.
        
        Args:
            figsize (tuple): Figure size (width, height)
        """
        plt.figure(figsize=figsize)
        sns.countplot(data=self.df, x=TARGET)
        plt.title('Target (Churn) Distribution')
        
        # Add percentage labels
        total = len(self.df)
        for p in plt.gca().patches:
            percentage = f'{100 * p.get_height() / total:.1f}%'
            plt.gca().annotate(
                percentage,
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center',
                va='bottom'
            )
        
        plt.show()
    
    def plot_numeric_distributions(
        self,
        columns: List[str] = None,
        figsize: tuple = (15, 10)
    ) -> None:
        """
        Plot distributions of numeric features.
        
        Args:
            columns (List[str]): List of columns to plot. If None, uses all numeric features
            figsize (tuple): Figure size (width, height)
        """
        columns = columns or NUMERIC_FEATURES
        n_cols = 3
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig = plt.figure(figsize=figsize)
        for i, col in enumerate(columns, 1):
            plt.subplot(n_rows, n_cols, i)
            sns.histplot(
                data=self.df,
                x=col,
                hue=TARGET,
                multiple="stack",
                bins=30
            )
            plt.title(f'Distribution of {col}')
        
        plt.tight_layout()
        plt.show()
    
    def plot_categorical_distributions(
        self,
        columns: List[str] = None,
        figsize: tuple = (15, 5)
    ) -> None:
        """
        Plot distributions of categorical features.
        
        Args:
            columns (List[str]): List of columns to plot. If None, uses all categorical features
            figsize (tuple): Figure size (width, height)
        """
        columns = columns or CATEGORICAL_FEATURES
        n_cols = len(columns)
        
        fig = plt.figure(figsize=figsize)
        for i, col in enumerate(columns, 1):
            plt.subplot(1, n_cols, i)
            sns.countplot(
                data=self.df,
                x=col,
                hue=TARGET
            )
            plt.title(f'Distribution of {col}')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def plot_correlation_matrix(self, figsize: tuple = (12, 8)) -> None:
        """
        Plot correlation matrix for numeric features.
        
        Args:
            figsize (tuple): Figure size (width, height)
        """
        numeric_df = self.df[NUMERIC_FEATURES + [TARGET]]
        correlation_matrix = numeric_df.corr()
        
        plt.figure(figsize=figsize)
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='coolwarm',
            center=0,
            fmt='.2f'
        )
        plt.title('Feature Correlation Matrix')
        plt.show()
    
    def plot_boxplots(
        self,
        columns: List[str] = None,
        figsize: tuple = (15, 10)
    ) -> None:
        """
        Plot boxplots for numeric features by target.
        
        Args:
            columns (List[str]): List of columns to plot. If None, uses all numeric features
            figsize (tuple): Figure size (width, height)
        """
        columns = columns or NUMERIC_FEATURES
        n_cols = 3
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig = plt.figure(figsize=figsize)
        for i, col in enumerate(columns, 1):
            plt.subplot(n_rows, n_cols, i)
            sns.boxplot(
                data=self.df,
                x=TARGET,
                y=col
            )
            plt.title(f'Distribution of {col} by Target')
        
        plt.tight_layout()
        plt.show() 