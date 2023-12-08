import os
import pandas as pd
from typing import Tuple


def getData(fileNames: list) -> dict:
    """
    Get the data in DataFrames from the files in the data folder.

    Args:
        fileNames (list): List of file names.

    Returns:
        dict: Dictionary of dataframes.
    """
    dictDataframes = dict()
    for fileName in fileNames:
        df = pd.read_csv(fileName, encoding="ISO-8859-1")
        key = os.path.splitext(os.path.basename(fileName))[0]
        dictDataframes[key] = df

    return dictDataframes


def groupingByYear(df: pd.DataFrame) -> pd.Series:
    """
    Group the data by the year of release and count the occurrences.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.Series: Series with counts of occurrences for each year.
    """
    return (
        df[df.Year_of_Release < 2017]
        .Year_of_Release.groupby(df.Year_of_Release)
        .count()
    )


def groupingByYearCount(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Group the data by year and genre, counting occurrences.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to group by.

    Returns:
        pd.DataFrame: Pivot table with counts for each year and specified column combination.
    """
    return (
        df[df.Year_of_Release < 2017]
        .pivot_table(
            index="Year_of_Release", columns=column, aggfunc="size", fill_value=0
        )
        .reset_index()
    )


def groupingByYearCountPercetange(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Calculates the percentage distribution of occurrences by year and a specified column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to group by.

    Returns:
        pd.DataFrame: Pivot table with rows representing years, columns representing unique values in the specified column,
                      and values representing the percentage distribution of occurrences for each value in each year.
    """
    dfYearCount = groupingByYearCount(df, column)
    YearCountSum = dfYearCount.drop("Year_of_Release", axis=1).sum(axis=1)

    # Calculate the percentage distribution of occurrences for each value in the specified column in each year
    dfYearCountPercentage = dfYearCount.drop("Year_of_Release", axis=1).div(
        YearCountSum, axis=0
    )

    # Multiply by 100 to get percentages, concatenate with the 'Year_of_Release' column, and return the result
    dfYearCountPercentage *= 100
    dfYearCountPercentage = pd.concat(
        [dfYearCount[["Year_of_Release"]], dfYearCountPercentage], axis=1
    )

    return dfYearCountPercentage


def groupingByYearSales(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Groups the DataFrame by year and a specified column, summing global sales.

    Args:
        df (pd.DataFrame): Input DataFrame containing video game sales data.
        column (str): Column in the DataFrame by which the grouping should be done (e.g., 'Genre', 'Platform').

    Returns:
        pd.DataFrame: Pivot table with rows representing years, columns representing unique values in the specified column,
                      and values representing the sum of global sales for each value in each year.
    """
    # Filter rows where the year of release is before 2017, pivot the table, and fill missing values with 0
    return (
        df[df.Year_of_Release < 2017]
        .pivot_table(
            index="Year_of_Release",
            columns=column,
            values="Global_Sales",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )


def groupingByYearSalesPercetange(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Calculates the percentage distribution of global sales by year and a specified column.

    Args:
        df (pd.DataFrame): Input DataFrame containing video game sales data.
        column (str): Column in the DataFrame by which the grouping should be done (e.g., 'Genre', 'Platform').

    Returns:
        pd.DataFrame: Pivot table with rows representing years, columns representing unique values in the specified column,
                      and values representing the percentage distribution of global sales for each value in each year.
    """
    # Use the groupingByYearSales function to get the sum of sales by year and specified column
    dfYearSales = groupingByYearSales(df, column)

    # Calculate the sum of sales for each year
    YearSalesSum = dfYearSales.drop("Year_of_Release", axis=1).sum(axis=1)

    # Calculate the percentage distribution of sales for each value in the specified column in each year
    dfYearSalesPercentage = dfYearSales.drop("Year_of_Release", axis=1).div(
        YearSalesSum, axis=0
    )

    # Multiply by 100 to get percentages, concatenate with the 'Year_of_Release' column, and return the result
    dfYearSalesPercentage *= 100
    dfYearSalesPercentage = pd.concat(
        [dfYearSales[["Year_of_Release"]], dfYearSalesPercentage], axis=1
    )

    return dfYearSalesPercentage


def groupingSumByYear(df: pd.DataFrame) -> pd.Series:
    """
    Group the data by year and sum global sales.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.Series: Series with summed global sales for each year.
    """
    return (
        df[df.Year_of_Release < 2017]["Global_Sales"].groupby(df.Year_of_Release).sum()
    )


def getKPIs(df: pd.DataFrame, column: str) -> list:
    """
    Calculate Key Performance Indicators (KPIs) related to video game sales.

    Args:
        df (pd.DataFrame): Input DataFrame containing video game sales data.
        column (str): Column in the DataFrame for which KPIs should be calculated (e.g., 'Genre', 'Platform').

    Returns:
        list: A list of dictionaries representing KPIs, each containing 'title', 'value', 'color', 'align', and 'variant'.
    """
    # Compute total sales across all unique values in the specified column
    columnSum = (
        df[df.Year_of_Release < 2017][["Global_Sales"]]
        .groupby(df[column])
        .sum()
        .reset_index()
    )

    # Count the number of unique values in the specified column
    nColumn = columnSum.shape[0]
    nColumn = str(nColumn) + " " + column + "s"

    # Find the best-selling game across all genres
    dfBestSeller = columnSum.nlargest(1, "Global_Sales")[[column, "Global_Sales"]]
    bestSeller = str(dfBestSeller.iloc[0][column])

    # Initialize variable to store total sales
    gamesSales = dfBestSeller.iloc[0]["Global_Sales"]

    # Convert total sales to millions and create a string representation
    gamesSales = gamesSales * 100
    gamesSales = gamesSales / 100
    gamesSales_str = str(gamesSales) + " Millions USD"

    # Prepare data for KPIs
    keys = [
        "Most Successful " + column,
        bestSeller + " " + column + " Total Sales",
        "Best out of",
    ]
    values = [bestSeller, gamesSales_str, nColumn]

    # Create a list of dictionaries, each representing a KPI
    data = [
        {
            "title": key,
            "value": str(value),
            "color": "success",
            "align": "center",
            "variant": "topColor",
        }
        for key, value in zip(keys, values)
    ]

    return data


def groupingByCount(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Group the data by year and count occurrences.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column to group by.

    Returns:
        pd.Series: Series with counts of occurrences for each group.
    """
    return df[df.Year_of_Release < 2017][column].groupby(df[column]).count()


def getTopN(df: pd.DataFrame, column: str, n: int) -> pd.DataFrame:
    """
    Get the top N entries based on the sum of global sales for a specified column.

    Args:
        df (pd.DataFrame): Input DataFrame containing video game sales data.
        column (str): Column in the DataFrame by which the grouping should be done (e.g., 'Genre', 'Platform').
        n (int): Number of top entries to retrieve.

    Returns:
        pd.DataFrame: Top N entries based on the sum of global sales for the specified column.
    """
    columnSum = (
        df[df.Year_of_Release < 2017][["Global_Sales"]]
        .groupby(df[column])
        .sum()
        .reset_index()
    )
    return columnSum.nlargest(n, "Global_Sales")[[column, "Global_Sales"]]


def firstLastRelease(df: pd.DataFrame, column: str, top: str) -> Tuple[int, int]:
    """
    Finds the first and last release years for the specified item in the given column.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - column (str): The column to search for the specified item.
    - top (str): The specific item for which to find the first and last release years.

    Returns:
    - Tuple[int, int]: A tuple containing the first and last release years.
    """
    firstDate = df[(df[column] == top) & (df.Year_of_Release < 2017)][
        "Year_of_Release"
    ].min()
    LastDate = df[(df[column] == top) & (df.Year_of_Release < 2017)][
        "Year_of_Release"
    ].max()
    return firstDate, LastDate


def convert_dataframe_to_array(df: pd.DataFrame) -> list:
    """Convert a DataFrame to a list of dictionaries.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        list: List of dictionaries representing the DataFrame.
    """
    columnsToInclude = df.columns.tolist()
    newData = []
    for index, row in df.iterrows():
        newDict = {column: row[column] for column in columnsToInclude}
        newData.append(newDict)
    return newData


def convert_series_to_array(df: pd.Series, column: str, rowName: str = "Count") -> list:
    """Convert a Series to a list of dictionaries.

    Args:
        df (pd.Series): Input Series.
        column (str): Column name.
        rowName (str): Name for the row in the resulting dictionary.

    Returns:
        list: List of dictionaries representing the Series.
    """
    new_data = [{column: index, rowName: row} for index, row in df.items()]
    return new_data
