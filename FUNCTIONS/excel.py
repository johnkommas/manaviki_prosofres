#  Copyright (c) Ioannis E. Kommas 2023. All Rights Reserved
import pandas as pd


def export(path_to_file, df_a, df_b, df_c = None, df_d = None):
    """
        Writes data from Pandas dataframes to an Excel file, and format the created Excel file.

        Args:
            path_to_file (str): Path to the output Excel file.
            df_a, df_b, df_c, df_d (pd.DataFrame): Dataframes containing the data to be exported to Excel.

        Function creates an ExcelWriter object, then exports each dataframe to a specific
        location in the 'TODAY' sheet of the Excel file. Once data is written, formats (as in
        fonts, alignment, cell width etc.) are applied to specific columns of the table.

        Greek letters 'Α' to 'Ω' (Alpha to Omega) are used to filter rows in the source dataframes
        df_a and df_b, then each filtered dataframe is written in the same Excel sheet.

        Cells in spreadsheet are formatted according to their content (currency, percentage,
        plain text etc.).

        Note:
            'Α' to 'Ω' are uppercase Greek letters Alpha to Omega.
            The df_a and df_b source dataframes must contain a column 'ΕΙΔΟΣ'.
    """
    data = [chr(i) for i in range(ord('Α'), ord('Ω') + 1)]
    with pd.ExcelWriter(path_to_file, engine='xlsxwriter') as writer:
        df_c.to_excel(writer, sheet_name='CHANGES', startcol=0, startrow=1, index=None)
        df_d.to_excel(writer, sheet_name='CHANGES', startcol=5, startrow=1, index=None)
        row = 0
        for letter in data:
            df_gresco = df_a[df_a['ΕΙΔΟΣ'].str.startswith(letter)]
            df_kalimera = df_b[df_b['ΕΙΔΟΣ'].str.startswith(letter)]
            df_gresco.to_excel(writer, sheet_name='TODAY', startcol=0, startrow=row, index=None)
            df_kalimera.to_excel(writer, sheet_name='TODAY', startcol=4, startrow=row, index=None)
            df_length = [len(df_gresco), len(df_kalimera)]
            row = row + max(df_length) + 2 if max(df_length) > 0 else row
        # Φτιάχνω το EXCEL για να είναι ευανάγνωστο
        workbook = writer.book
        worksheet = writer.sheets['TODAY']
        worksheet_2 = writer.sheets['CHANGES']
        number = workbook.add_format({
            'num_format': '€#,##0.00',
            'align': 'left',
            'bold': False,
            "font_name": "Avenir Next"})
        normal = workbook.add_format({
            'align': 'left',
            'bold': False,
            "font_name": "Avenir Next"})

        percent = workbook.add_format({
            'num_format': '%#,##0.00',
            'align': 'left',
            'bold': False,
            "font_name": "Avenir Next"})

        normal_bold = workbook.add_format({
            'align': 'center',
            "valign": "vcenter",
            "font_size": 10,
            "text_wrap": True,
            "bg_color": "#6b9080",
            'bold': True,
            "font_name": "Avenir Next"})

        worksheet.set_column('A:A', 41, normal)
        worksheet.set_column('B:B', 8, number)
        worksheet.set_column('C:C', 1, normal)
        worksheet.set_column('D:D', 1, normal)
        worksheet.set_column('E:E', 45, normal)
        worksheet.set_column('F:F', 9, number)

        # ΟΙ ΠΤΩΣΕΙΣ ΤΙΜΩΝ
        worksheet_2.set_column('A:A', 1, normal)
        worksheet_2.set_column('B:B', 1, number)
        worksheet_2.set_column('C:C', 1, number)
        worksheet_2.set_column('D:D', 1, percent)
        worksheet_2.set_column('F:F', 1, normal)
        worksheet_2.set_column('G:G', 1, number)
        worksheet_2.set_column('H:H', 1, number)
        worksheet_2.set_column('I:I', 1, percent)

        # ΟΙ ΠΤΩΣΕΙΣ ΤΙΜΩΝ
        worksheet_2.merge_range(f"A1:D1", 'GRESCO ΠΤΩΣΗ ΤΙΜΩΝ', normal_bold)
        worksheet_2.merge_range(f"F1:I1", 'ΚΑΛΗΜΕΡΑ ΦΡΟΥΤΑ ΠΤΩΣΗ ΤΙΜΩΝ', normal_bold)

        # Autofit the worksheet.
        worksheet_2.autofit()
        # worksheet.set_column('C:C', 1, normal)
        # worksheet.set_column('D:D', 1, normal)