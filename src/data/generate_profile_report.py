"""
Generate a comprehensive profiling report for the Bank Customer Churn dataset.
"""
import pandas as pd
from ydata_profiling import ProfileReport

def generate_profile_report():
    """
    Load the data and generate a detailed profiling report.
    """
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv('Bank Customer Churn Prediction.csv')
    
    # Generate report
    print("Generating profiling report...")
    profile = ProfileReport(df, 
                          title="Bank Customer Churn Dataset Profiling Report",
                          explorative=True,
                          dark_mode=True)
    
    # Save report
    print("Saving report...")
    profile.to_file("reports/churn_profile_report.html")
    print("Report saved to reports/churn_profile_report.html")

if __name__ == "__main__":
    generate_profile_report() 