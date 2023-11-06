import pandas as pd
import tabula

# ----------------MAKE DF Reports Viewable----------------------------
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)


def run_prosfores_gresko(file):
    """
        Reads an Excel file, restructures and cleans the data.

        Args:
            file (str): The path to the Excel file.

        Returns:
            df (pd.DataFrame): A DataFrame with columns 'ΕΙΔΟΣ' and 'GRESKO', sorted by 'ΕΙΔΟΣ'.
                               Only contains rows where 'GRESKO' values are numeric.

        This function combines three dataframes, which were created from different columns
        of the same Excel file. The combined dataframe goes through several cleaning steps,
        such as removing non-numeric values from the 'GRESKO' column and unifying the character
        set in 'ΕΙΔΟΣ' column.

        Note:
            'ΕΙΔΟΣ' translates to 'type' in Greek and 'GRESKO' is a company name.
            Requires the pandas library to process Excel files.
    """
    column_names = ['ΕΙΔΟΣ', 'ΤΙΜΗ']
    df_a = pd.read_excel(file, skiprows=range(1, 6), usecols="A,B", names=column_names)
    df_b = pd.read_excel(file, skiprows=range(1, 6), usecols="C,D", names=column_names)
    df_c = pd.read_excel(file, skiprows=range(1, 6), usecols="E,F", names=column_names)

    df = pd.concat([df_a, df_b, df_c], ignore_index=True)

    greek_accent_mapping = {
        'M': 'Μ',
        'N': 'Ν',
        'A': 'Α',
        u'ά': u'α',
        u'Ά': u'α',
        u'έ': u'ε',
        u'ή': u'η',
        u'ί': u'ι',
        u'ύ': u'υ',
        u'ώ': u'ω',
        u'ό': u'ο',
        u'ϊ': u'ι',
        u'ϋ': u'υ',
        u'ΐ': u'ι',
        u'ΰ': u'υ'
    }
    df['ΕΙΔΟΣ'] = df['ΕΙΔΟΣ'].replace(greek_accent_mapping, regex=True).str.upper().str.strip()

    # Τιμές όπως "-" και τίτλοι όπως ΦΡΕΣΚΑ ΑΡΩΜΑΤΙΚΑ ΦΡΟΥΤΑ ΤΙΜΗ θα αφαιρεθούν
    # μετατρέποντας τη στήλη σε numeric, αυτές οι τιμές γίνονται ΝαΝ και με το .notna() τα αφαιρώ,
    df = df[pd.to_numeric(df['ΤΙΜΗ'], errors='coerce').notna()].sort_values(by='ΕΙΔΟΣ').reset_index(drop=True)
    columns = {'ΤΙΜΗ': 'GRESKO'}
    df = df.rename(columns=columns)
    return df


def run_prosfores_kalimera(file):
    """
        Reads a given PDF file into a pandas DataFrame, restructures and cleans the data,
        resulting in a DataFrame ready for further processing.

        Args:
            file (str): The path to the PDF file.

        Returns:
            df (pd.DataFrame): A restructured DataFrame containing only rows with
                               non-null and positive 'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ' values sorted by 'ΕΙΔΟΣ'.

        Note:
            'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ' translates to 'Good morning fruits' in Greek and likely refers to prices.
            'ΕΙΔΟΣ' translates to 'type' in Greek and likely refers to a type of product.
            The function requires the tabula library to process PDF files.
    """
    # Read the PDF file into a DataFrame
    df = tabula.read_pdf(file, pages='all')[0]

    df_a = df[['ΠΡΟΪΟΝ', '*ΤΙΜΗ (€) / Μ.Μ.']]
    columns = {'ΠΡΟΪΟΝ': 'ΕΙΔΟΣ', '*ΤΙΜΗ (€) / Μ.Μ.': 'ΚΑΛΗΜΕΡΑ'}
    df_a = df_a.rename(columns=columns)

    df_b = df[['ΠΡΟΪΟΝ.1', '*ΤΙΜΗ (€) / Μ.Μ..1']]
    columns = {'ΠΡΟΪΟΝ.1': 'ΕΙΔΟΣ', '*ΤΙΜΗ (€) / Μ.Μ..1': 'ΚΑΛΗΜΕΡΑ'}
    df_b = df_b.rename(columns=columns)

    df = pd.concat([df_a, df_b], ignore_index=True)
    df['ΚΑΛΗΜΕΡΑ'] = df['ΚΑΛΗΜΕΡΑ'].str.replace(',', '.')
    df = df[pd.to_numeric(df['ΚΑΛΗΜΕΡΑ'], errors='coerce').notna()].sort_values(by='ΕΙΔΟΣ').reset_index(drop=True)
    df['ΚΑΛΗΜΕΡΑ'] = df['ΚΑΛΗΜΕΡΑ'].astype(float)
    df = df[df['ΚΑΛΗΜΕΡΑ'] > 0]
    return df
