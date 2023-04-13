"""Import and clean the cases dataset"""

import pandas as pd
import numpy as np

# Define path to cases dataset
path = "10_data/cases_2020_2022.csv"

# Define path to output csv
output_path = "10_data/cases_by_month_year.csv"

# Define function to return dataset to state-by-month-year
def transform_df(df):
    """Find cases of a state/territory for each month-year combination"""
    # Change the date column to pandas datetime type
    df["date"] = pd.to_datetime(df["submission_date"])
    # Create an extra column of month-year combination
    df["week-year"] = df["date"].apply(lambda x: x.strftime("%U-%Y"))
    # Create extra column for year
    df["year"] = df["date"].apply(lambda x: x.strftime("%Y"))
    # Subset for data between 2021-2022
    df_subset = df.copy()
    df_subset = df_subset.loc[df_subset["year"].isin(["2021", "2022"])]
    # Groupby to get number of new cases in each month
    cases_by_month = df_subset.groupby(["week-year", "state"])["new_case"].sum()
    # Reset the index to get dataframe instead of multi-index
    final_df = cases_by_month.reset_index()
    return final_df


if __name__ == "__main__":
    # Read in the cases dataset
    cases = pd.read_csv(path)
    # Return the cleaned dataframe
    cleaned_df = transform_df(cases)
    # Return csv to data folder
    cleaned_df.to_csv(output_path)
