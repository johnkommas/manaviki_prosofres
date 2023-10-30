import pandas as pd


def run_gresko(new, old):
    """
        Compares two DataFrames, 'new' and 'old', on the 'ΕΙΔΟΣ' column, and calculates the percent change
        in price where there has been a decrease. Only rows where there has been a decrease are preserved.

        Args:
        new (pd.DataFrame): DataFrame with an 'ΕΙΔΟΣ' and 'GRESKO' column representing the current state of data.
        old (pd.DataFrame): DataFrame with an 'ΕΙΔΟΣ' and 'GRESKO' column representing the previous state of data.

        Returns:
        df (pd.DataFrame): A DataFrame sorted in ascending order of the Percent Change value
        where Percent Change represents a decrease in price.

        Note:
            'ΕΙΔΟΣ' translates to 'type' in Greek and 'GRESKO' is a company name.
            The merge operation on 'ΕΙΔΟΣ' column signifies it should be used as a key to match rows between the two dataframes.
    """
    df = pd.merge(new, old, how='left', on='ΕΙΔΟΣ')
    rename = {'GRESKO_x': 'NEW PRICE', 'GRESKO_y': 'OLD PRICE'}
    df.rename(columns=rename, inplace=True)
    df['Percent Change'] = ((df['NEW PRICE'] - df['OLD PRICE']) / df['OLD PRICE'])
    df = df[df['Percent Change'] < 0]
    df = df.sort_values(by='Percent Change').reset_index(drop=True)
    return df


def run_kalimera(new, old):
    """
        Compares two DataFrames, 'new' and 'old', on the 'ΕΙΔΟΣ' column, and calculates the percent change
        in price where there has been a decrease. Only rows where there has been a decrease are preserved.

        Args:
        new (pd.DataFrame): DataFrame with an 'ΕΙΔΟΣ' and 'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ' column representing the current state of data.
        old (pd.DataFrame): DataFrame with an 'ΕΙΔΟΣ' and 'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ' column representing the previous state of data.

        Returns:
        df (pd.DataFrame): A DataFrame sorted in ascending order of the Percent Change value
        where Percent Change represents a decrease in price.

        Note:
            'ΕΙΔΟΣ' translates to 'type' in Greek and 'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ' is a company name.
            The merge operation on 'ΕΙΔΟΣ' column signifies it should be used as a key to match rows between the two dataframes.
    """
    df = pd.merge(new, old, how='left', on='ΕΙΔΟΣ')
    rename = {'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ_x': 'NEW PRICE', 'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ_y': 'OLD PRICE'}
    df.rename(columns=rename, inplace=True)
    df['Percent Change'] = ((df['NEW PRICE'] - df['OLD PRICE']) / df['OLD PRICE'])
    df = df[df['Percent Change'] < 0]
    df = df.sort_values(by='Percent Change').reset_index(drop=True)
    return df
